import os, urllib.request, json, re
from tkinter import *
from tkinter import messagebox
from labels import *
from manager import SwitchManger


class App(Frame):

    server_address = None
    add_server_win = None
    list_box = None
    thread = None

    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.server_address = StringVar()
        self.parent = parent
        self.parent.geometry('640x480')
        self.parent.attributes('-topmost', False)
        self.generate_gui()

    def generate_gui(self):
        # Main window and title
        self.parent.title(window_title_label)

        # Menu bar and drop down ADD
        menu = Menu(self.parent, tearoff=0)
        menu.add_command(label=add_server_label, command=self.add_server)
        menu.add_command(label=close_program_label, command=self.parent.destroy)
        self.parent.config(menu=menu)

        # Server list
        self.load_server_list()

    def load_server_list(self):
        self.list_box = Listbox(self.parent, width=60, height=4)
        self.list_box.pack(side='left', fill='y')

        scrollbar = Scrollbar(self.parent, orient="vertical", command=self.list_box.yview)
        scrollbar.pack(side="right", fill="y")

        self.list_box.config(yscrollcommand=scrollbar.set)

        # Load all server register
        self.refresh_server_list()

        # Launch button
        launch_button = Button(self.parent, text=launch_client_label, font=(24), command=self.launch_server)
        launch_button.pack(expand="yes", anchor="center")

        # Delete button
        delete_button = Button(self.parent, text=delete_server_label, font=(24), command=self.delete_server)
        delete_button.pack(expand="yes", anchor="center")

        # Refresh clients online button
        refresh_clients_button = Button(self.parent, text=refresh_clients_label, font=(24),
                                        command=self.refresh_server_list)
        refresh_clients_button.pack(expand="yes", anchor="center")

    def launch_server(self):
        if self.check_selected_server():
            server_selected = self.check_selected_server()
            if self.check_server_status(server_selected, True):
                command = "start /B start cmd.exe @cmd /k bin\lan-play.exe --relay-server-addr %s" % server_selected
                os.system(command)

    def delete_server(self):
        if self.check_selected_server():
            server_selected = self.check_selected_server()
            manager = SwitchManger()
            manager.delete_server(server_selected)
            manager.close_connection()
            self.list_box.delete(self.list_box.curselection())
            messagebox.showinfo(opps_label, server_deleted_label)

    def check_server_status(self, server_address, show_message):
        """
        Check the server status and returns players online
        :param show_message:
        :param server_address:
        :return:
        """
        try:
            url = "http://%s/info" % server_address
            response = urllib.request.urlopen(url).read()
            data = json.loads(response)
            if 'online' in data:
                return data['online']
        except Exception:
            try:
                url = "http://%s" % server_address
                response = urllib.request.urlopen(url).read()
                data = json.loads(response)
                if 'clientCount' in data:
                    return data['clientCount']
            except Exception:
                pass
        if show_message:
            messagebox.showinfo(opps_label, server_no_reponse_label)
        return ""

    def check_selected_server(self):
        try:
            server_selected = self.list_box.get(self.list_box.curselection())
            server_selected = server_selected.split("[")[0].strip()
        except Exception:
            server_selected = None

        if server_selected:
            return server_selected

        messagebox.showinfo(opps_label, select_server_label)

    def do_popup(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def add_server(self):
        self.add_server_win = Toplevel(self.parent)
        self.add_server_win.title(add_server_label)
        self.add_server_win.geometry("320x240")
        self.add_server_elements()

    def add_server_elements(self):
        input_server = Entry(self.add_server_win, width=40, textvariable=self.server_address)
        input_server.pack(expand="yes", anchor="center")

        enter_button = Button(self.add_server_win, text=save_label, font=(24), command=self.save_server)
        enter_button.pack(expand="yes", anchor="center")

    def save_server(self):
        if not self.server_address.get():
            messagebox.showinfo(opps_label, sever_address_value_label, parent=self.add_server_win)
        else:
            server_address = self.server_address.get()
            pattern = re.compile("^(?!http:|https:|www.)([-a-zA-Z0-9@:%._]{1,256}):([0-9]{1,5})$")

            if pattern.match(server_address):
                port_server = int(server_address.split(":")[1])

                if port_server < 0 or port_server > 65535:
                    messagebox.showinfo(great_label, server_port_values_label)
                elif self.check_server_status(server_address, True):
                    clients_online = self.check_server_status(server_address, False)
                    # Object manager
                    manager = SwitchManger()
                    # Check if already exists
                    rows = manager.select_server(server_address)
                    if rows:
                        messagebox.showinfo(great_label, server_already_exists_label)
                    else:
                        manager.insert_server(server_address)
                        self.list_box.insert(END, self.generate_list_register(server_address, clients_online))
                        messagebox.showinfo(great_label, server_added_label)
                        self.add_server_win.destroy()
                    manager.close_connection()
            else:
                messagebox.showinfo(great_label, server_address_example_label)

    def generate_list_register(self, address, clients_number):
        aux = list_register_label % (address.ljust(50), clients_number)

        return aux

    def refresh_server_list(self):
        self.list_box.delete(0, END)

        manager = SwitchManger()
        rows = manager.select_server('')
        manager.close_connection()

        for row in rows:
            server_address = str(row[1])
            clients_online = self.check_server_status(server_address, False)
            self.list_box.insert(END, self.generate_list_register(server_address, clients_online))


def main():
    # Object manager
    manager = SwitchManger()
    manager.close_connection()

    # Window instance
    win = Tk()
    App(win)
    # Main loop
    win.mainloop()


if __name__ == '__main__':
    main()
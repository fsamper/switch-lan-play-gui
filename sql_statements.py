sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS servers (
                                        id integer PRIMARY KEY AUTOINCREMENT ,
                                        url text NOT NULL
                                    ); """
sql_insert_server = """ INSERT INTO servers (url) VALUES (?); """
sql_delete_server = """ DELETE FROM servers WHERE url = (?)"""
sql_select_server = """ SELECT * FROM servers; """
sql_select_server_by_name = """ SELECT * FROM servers WHERE url = (?)"""


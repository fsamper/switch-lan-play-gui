from django import forms


class SaveServerForm(forms.Form):
    server_address = forms.CharField(label='Server Address', max_length=255, required=True)
    notification_type = forms.IntegerField(label="Notification type", required=False)

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Server
from .forms import SaveServerForm


def servers(request):
    """
    Servers template
    """
    template = loader.get_template('servers.html')
    servers_list = Server.objects.all().order_by('order')
    notication_type = int(request.GET.get('notification_type', 0))
    last_inserted = servers_list.last()
    context = {
        'servers_list': servers_list,
        'notification_type': notication_type,
        'last_inserted': last_inserted
    }
    return HttpResponse(template.render(context, request))

@csrf_exempt
def save_server(request):
    """
    View for handle the save server form
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SaveServerForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            Server.objects.create(url=form.data['server_address'], name="prueba")
            # redirect to a new URL:
            return HttpResponseRedirect('/servers?notification_type=1')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SaveServerForm()

    return render(request, 'servers.html', {'form': form})

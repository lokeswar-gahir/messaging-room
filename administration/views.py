from django.shortcuts import render, redirect
from main.models import RoomLink, Messages
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib import messages
from os import getenv

# Create your views here.
def verifyCadmin(request):
    return render(request, 'verifyAdminEntry.html')

class CadminDashboard(TemplateView):
    template_name = 'cadmin_dashboard.html'

    def post(self, request, *args, **kwargs):
        admin_pass = self.request.POST.get('adminKey')
        if admin_pass == getenv('ADMIN_PASS_KEY'):
            context = self.get_context_data(**kwargs)
            return self.render_to_response(context)
        else:
            messages.info(self.request, 'Invalid Password for Admin !!!')
            return redirect(reverse('cadmin:verifyAdmin'))
            

    def get(self, request, *args, **kwargs):
        return redirect(reverse('cadmin:verifyAdmin'))

    def get_context_data(self, **kwargs):
        kwargs.setdefault("view", self)
        room_data = RoomLink.objects.all()
        messages_data = Messages.objects.all()
        self.extra_context = {'room_data': room_data, 'messages_data': messages_data}
        if self.extra_context is not None:
            kwargs.update(self.extra_context)
        return kwargs
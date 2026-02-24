from django.shortcuts import redirect, render, HttpResponse
from django.views.generic import CreateView
from .models import *
from django.urls import reverse_lazy
from django.utils.crypto import get_random_string
from .utils import get_ip
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.

class Index(CreateView):
    template_name = "index.html"
    model = RoomLink
    fields=['first_message', 'link_password']

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.ip_address = get_ip(self.request)
        self.object.link = get_random_string(6)
        self.object.verified_ips = self.object.ip_address

        self.object.save()
        self.success_url = self.object.get_absolute_url()
        return super().form_valid(form)
   
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["link"] = self.object.link
        return context
    

class Room(CreateView):
    template_name = 'room.html'
    model = Messages
    fields=['message']

    def dispatch(self, request, *args, **kwargs):
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
            self.current_link = self.kwargs.get('link')
            room_obj = RoomLink.objects.filter(link=self.current_link)
            if room_obj:
                verified_ips = room_obj.first().verified_ips
            else:
                return HttpResponse('Room does not exist !!!')

            if get_ip(self.request) not in verified_ips.split(' '):
                messages.info(request, 'you are not verified')
                print(get_ip(self.request), "IP is not registered.")
                return redirect(reverse('main:verifyRoomEntry', kwargs={'link': self.current_link}))

            self.success_url = reverse('main:room', kwargs={'link': self.current_link})
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self.current_room = RoomLink.objects.filter(link = self.current_link).first()
        room_messages = Messages.objects.filter(room_link = self.current_room)
        context["fetched_messages"] = room_messages
        context['link'] = self.current_link
        context['client_ip'] = get_ip(self.request)
        if self.current_room.ip_address == context['client_ip']:
            context['room_creater'] = True
        else:
            context['room_creater'] = False
        context['open_status'] = self.current_room.is_open
        context['total_users'] = len(self.current_room.verified_ips.split(" "))
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.current_room = RoomLink.objects.filter(link = self.current_link).first()
        if self.current_room.is_open:
            self.object.room_link = self.current_room
            self.object.ip_address = get_ip(self.request)
            self.object.save()
            return super().form_valid(form)
        else:
            return HttpResponse(f'This Room({self.current_link}) is already closed by the creater.')

def closeRoom(request, link):
    room_obj = RoomLink.objects.filter(link = link).first()
    if room_obj:
        room_ip = room_obj.ip_address
        if room_ip==get_ip(request):
            room_obj.is_open = False
            room_obj.save()
            return redirect(reverse('main:room', kwargs={'link': link}))
        else:
            print(room_ip, get_ip(request=request))
            return HttpResponse("Not allowed")
        


def verifyRoomEntry(request, link):
    room_obj = RoomLink.objects.filter(link=link)
    if room_obj:
        # verified_ips = room_obj.first().verified_ips
        return render(request, 'verifyRoomEntry.html', {'roomId': link})
    else:
        return HttpResponse('Room does not exist !!!')

def verifiedRoomEntry(request, link):
    room_id = link
    room_pass = request.POST.get('roomKey')
    room_obj = RoomLink.objects.filter(link = room_id)
    if room_obj:
        if room_obj[0].link_password == room_pass:
            verified_ips = room_obj[0].verified_ips
            if get_ip(request) not in verified_ips.split(' '):
                room_obj[0].verified_ips = str.strip(room_obj[0].verified_ips+' '+str(get_ip(request)))
                room_obj[0].save()
                print(room_obj[0].verified_ips, 'added new verified IP address')
            return redirect(reverse('main:room', kwargs={'link': link}))
        else:
            messages.info(request, 'Incorrect Password !!!')
            return redirect(reverse('main:verifyRoomEntry', kwargs={'link': link}))
    else:
        return HttpResponse('Room does not exist !!!')

def updateMessage(request, link):
    update_msg_id = request.POST.get('messageId')
    if update_msg_id:
        updated_msg = request.POST.get('updatedMessage')

        msg_obj = Messages.objects.filter(id= update_msg_id).first()
        requester_ip=get_ip(request)
        if msg_obj.message != updated_msg and msg_obj.ip_address==requester_ip:
            msg_obj.message = updated_msg
            msg_obj.save()
            print(f'Message updated successfully.({msg_obj.id})')

        return redirect(reverse_lazy('main:room', kwargs={'link': link}))
    else:
        return HttpResponse('Method not allowed !!!')
    
def deleteRoom(request):
    delete_request_sender = request.POST.get('sender')
    if delete_request_sender=='byAdmin007':
        delete_room_id = request.POST.get('deleteRoomId')
        room_obj = RoomLink.objects.filter(id=delete_room_id)
        if room_obj:
            room_obj[0].delete()
            messages.info(request, f'Room({delete_room_id}, {room_obj[0].link}) deleted successfully.')
            return redirect(reverse('cadmin:cadmin_dashboard'))
        else:
            return HttpResponse('Room does not exist !!!')
    else:
        return HttpResponse('Access Denied !!!')

def deleteMessage(request):
    delete_request_sender = request.POST.get('sender')
    if delete_request_sender=='byAdmin007':
        delete_message_id = request.POST.get('deleteMessageId')
        message_obj = Messages.objects.filter(id=delete_message_id)
        if message_obj:
            message_obj[0].delete()
            messages.info(request, f'Message({delete_message_id}, \'{message_obj[0].message})\' deleted successfully.')
            return redirect(reverse('cadmin:cadmin_dashboard'))
        else:
            return HttpResponse('Message does not exist !!!') 
    else:
        return HttpResponse('Access Denied !!!')
def getVerifiedIps(request, link):
    # print(get_ip(request))
    room_obj = RoomLink.objects.filter(link=link).first()
    if room_obj.ip_address == get_ip(request):
        return JsonResponse({"verifiedIps": room_obj.verified_ips.split(" ")})
    else:
        return JsonResponse({"error": "permission denied", "description": 'you are not the owner of this room'})
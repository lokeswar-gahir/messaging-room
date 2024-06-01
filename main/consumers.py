import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproj.settings")
django.setup()

from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer
from json import dumps, loads
from .models import *
from channels.db import database_sync_to_async

# class RoomSocket(SyncConsumer):
#     def websocket_connect(self, event):
#         print('Roomsocket Connected...', event)
#         self.send({
#             'type': 'websocket.accept'
#         })
    
#     def websocket_receive(self, event):
#         print('\nRecieved text:', event)
#         self.send({
#             'type': 'websocket.send',
#             'text': event['text'],
#         })
    
#     def websocket_disconnect(self, event):
#         print('Roomsocket Disconnected...', event)
#         raise StopConsumer()


class AsyncRoomSocket(AsyncConsumer):
    async def websocket_connect(self, event):
        # print('Channel Layer:', self.channel_layer)
        # print('Channel Name:', self.channel_name)
        self.group_name = self.scope.get('url_route').get('kwargs').get('link')
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.send({
            'type': 'websocket.accept'
        })

    async def websocket_receive(self, event):
        msgBundle = loads(event['text'])
        sender_ip = msgBundle['sender_ip']
        message = msgBundle['msg']
        room_link = await database_sync_to_async(RoomLink.objects.get)(link = self.group_name)
        total_users = len(room_link.verified_ips.split(' '))
        msg_obj = Messages(room_link = room_link, ip_address=sender_ip, message=message)
        await database_sync_to_async(msg_obj.save)()
        self.message_id = msg_obj.id
        await self.channel_layer.group_send(self.group_name, {
            'type': 'chat.message',
            'text': dumps({'sender_ip': msgBundle['sender_ip'], 'msg': msgBundle['msg'], 'message_id': self.message_id, 'total_users':total_users}),
        })
    
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })
        
    async def websocket_disconnect(self, event):
        print('Roomsocket Disconnected.(Async)', event)
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()

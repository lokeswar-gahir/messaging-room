from channels.consumer import SyncConsumer, AsyncConsumer
from channels.exceptions import StopConsumer


class RoomSocket(SyncConsumer):
    def websocket_connect(self, event):
        print('Roomsocket Connected...', event)
        self.send({
            'type': 'websocket.accept'
        })
    
    def websocket_receive(self, event):
        print('\nRecieved text:', event)
        self.send({
            'type': 'websocket.send',
            'text': event['text'],
        })
    
    def websocket_disconnect(self, event):
        print('Roomsocket Disconnected...', event)
        raise StopConsumer()


class AsyncRoomSocket(AsyncConsumer):
    async def websocket_connect(self, event):
        print('Roomsocket Connected.(Async)', event)
        await self.send({
            'type': 'websocket.accept'
        })
    
    async def websocket_receive(self, event):
        print('\nRecieved text:', event)
        
    async def websocket_disconnect(self, event):
        print('Roomsocket Disconnected.(Async)', event)
        raise StopConsumer()

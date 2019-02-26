from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from chat.models import Message
from financial_chat.settings import MAX_MESSAGES
import json


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print ('Receive =========> %s'%message)
        username = text_data_json['user']
        timestamp = datetime.now().strftime('%H:%M:%S')
        user = User.objects.get(username=username)
        try:
            Message.objects.create(message=message,user=user)
        except Error as e:
            print('%s'%e)
        new_message = Message.objects.order_by('-timestamp').first()
        print('New message: %s'%new_message)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'timestamp': timestamp,
                'user': username
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        print('Event ===========> %s' %event)
        message = ''
        recent_messages = Message.objects.order_by('-timestamp')[0:MAX_MESSAGES]
        for m in reversed(recent_messages):
            message += '[' + str(m.timestamp.strftime('%H:%M:%S')) + ']' + '[' + m.user.username + '] ' + m.message + '\n'
#        message = event['message']
#        username = event['user']
#        timestamp = event['timestamp']
        # Send message to WebSocket
        text_data=json.dumps({
            'message': message,
            #            'timestamp': timestamp,
            #            'user': username
        })
        print ('Send ==========> %s' %text_data)
        self.send(text_data)

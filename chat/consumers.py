from django.contrib.auth.models import User
from asgiref.sync import async_to_sync
from channels.consumer import SyncConsumer
from channels.generic.websocket import WebsocketConsumer
from datetime import datetime
from chat.models import Message
from financial_chat.settings import MAX_MESSAGES
import json
import requests


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
        username = text_data_json['user']
        timestamp = datetime.now().strftime('%H:%M:%S')
        if message.startswith('/stock='):
            print ('Stock message')
            company = message.strip('/stock=')
            print('Company: %s' %(company))
            async_to_sync(self.channel_layer.send)(
                'stockbot',
                {
                    'type': 'test_print',
                    'company': company,
                    'timestamp': timestamp,
                    'user': 'bot',
                    'channel_name': self.room_group_name
                },
            )
            
        else:
            print ('Receive =========> %s'%message)
            user = User.objects.get(username=username)
            try:
                Message.objects.create(
                    message=message,
                    user=user,
                    room=self.room_group_name
                )
            except Error as e:
                print('%s'%e)
            new_message = Message.objects\
                .filter(room=self.room_group_name)\
                .order_by('-timestamp')\
                .first()
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
        recent_messages = Message.objects\
            .filter(room=self.room_group_name)\
            .order_by('-timestamp')\
            [0:MAX_MESSAGES]
        for m in reversed(recent_messages):
            message +=\
                '[' + str(m.timestamp.strftime('%H:%M:%S')) + ']'\
                + '[' + m.user.username + '] '\
                + m.message\
                + '\n'
        # Send message to WebSocket
        text_data=json.dumps({
            'message': message,
            #            'timestamp': timestamp,
            #            'user': username
        })
        print ('Send ==========> %s' %text_data)
        self.send(text_data)

    def bot_message(self, event):
        print('Event ===========> %s' %event)
        message = ''
        recent_messages = Message.objects\
            .filter(room=self.room_group_name)\
            .order_by('-timestamp')\
            [0:MAX_MESSAGES]
        for m in reversed(recent_messages):
            message +=\
                '[' + str(m.timestamp.strftime('%H:%M:%S')) + ']'\
                + '[' + m.user.username + '] '\
                + m.message\
                + '\n'
        message +=\
            '[' + event['timestamp'] + ']'\
            + '[' + event['user'] + '] '\
            + event['message']\
            + '\n'

        text_data=json.dumps({
            'message': message,
        })
        print ('Send ==========> %s' %text_data)
        self.send(text_data)


class StockConsumer(SyncConsumer):

    def test_print(self, message):
        response = ''
        company = message['company']
        print('Message company: %s' %company)
        channel_name = message['channel_name']
        print('Channel Name: %s' %channel_name)
        timestamp = datetime.now().strftime('%H:%M:%S')
        if len(company) == 4:
            if company.isalpha():
                stock = requests.get(
                    'https://stooq.com/q/l/?s=%s.us&f=sd2t2ohlcv&h&e=csv'
                    %(company)
                )
                try:
                    close_value = float(
                        stock.text.split('\r\n')[1].split(',')[-2]
                    )
                    response = '%s quote is $%s per share.'\
                        %(company.upper(), close_value)
                except ValueError:
                    response = 'Could not obtain a value for company %s'\
                        %company.upper()
            else:
                print('Value must be alpha')
                response = 'Value must be alpha'
        else:
            print('Length of the company name should be 4')
            response = 'Length of the company name should be 4'

        async_to_sync(self.channel_layer.group_send)(
        message['channel_name'],
            {
                'type': 'bot_message',
                'message': response,
                'timestamp': timestamp,
                'user': 'bot'
            }
        )

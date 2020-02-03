from django.test import TestCase

from chat.models import Message
from django.contrib.auth.models import User

from datetime import datetime

class MessageTestCase(TestCase):

    def setUp(self):
        self.test_user = User()
        self.test_user.email = 'email@mail.com'
        self.test_user.save()


    def test_saving_and_retrieving_messages(self):
        first_message = Message()
        first_message.user = self.test_user
        first_message.message = 'My first message'
        first_message.save()

        second_message = Message()
        second_message.user = self.test_user
        second_message.message = 'My second message'
        second_message.save()

        saved_messages = Message.objects.all()
        self.assertEqual(saved_messages.count(), 2)

        first_saved_message = saved_messages[0]
        second_saved_message = saved_messages[1]

        self.assertEqual('My first message', first_saved_message.message)
        self.assertEqual('My second message', second_saved_message.message)


    def test_saving_a_full_message(self):
        first_message = Message()
        first_message.user = self.test_user
        first_message.message = 'My first message'
        first_message.room = 'Room1'
        first_message.save()

        saved_message = Message.objects.first()

        self.assertEqual('My first message', saved_message.message)
        self.assertEqual('Room1', saved_message.room)

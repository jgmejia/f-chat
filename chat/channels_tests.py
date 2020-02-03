import pytest
from channels.testing import WebsocketCommunicator
from chat.consumers import ChatConsumer
from channels.routing import URLRouter
from django.conf.urls import url


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_consumer(capsys):
    application = URLRouter([
        url(r'^ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer),
    ])
    communicator = WebsocketCommunicator(application, 'ws/chat/test1/')
    connected, subprotocol = await communicator.connect()
    assert connected
    await communicator.send_json_to({
        'type': 'websocket.send',
        'message': 'Hola mundo!',
        'timestamp': '12:12:12',
        'user': 'test_user'
    })
    event = await communicator.receive_json_from(timeout=10)
    assert event['message'] == 'Hola mundo!'
    assert event['type'] == 'websocket.send'
    assert event['timestamp'] == '12:12:13'
    await communicator.disconnect()

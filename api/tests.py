from django.test import TestCase
from rest_framework.test import APIClient
from .models import Book

from django.test import TestCase
from rest_framework.test import APIClient, force_authenticate
from django.contrib.auth.models import User
from .models import Book

class BookAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Book.objects.create(title="Test Book", author="Test Author", published_date="2023-01-01")

    def test_get_books_authenticated(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get('/api/v1/books/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)
        
        
import json
from channels.testing import WebsocketCommunicator
from django.test import TestCase
from .consumers import ChatConsumer

class ChatConsumerTests(TestCase):
    async def test_websocket_connection(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Получаем первое сообщение (приветственное)
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertEqual(response_data["message"], "Connected to WebSocket!")

        # Отправляем сообщение и проверяем ответ
        message = "Hello, server!"
        await communicator.send_to(text_data=json.dumps({"message": message}))
        response = await communicator.receive_from()
        response_data = json.loads(response)
        self.assertEqual(response_data["message"], f"You said: {message}")

        await communicator.disconnect()

    async def test_websocket_disconnection(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "/ws/chat/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Закрываем соединение
        await communicator.disconnect()

        # Проверяем, что соединение закрыто
        self.assertTrue(await communicator.is_closed())  # Проверяем, что соединение закрыто

        # Попытка получить сообщение должна вызвать исключение
        with self.assertRaises(RuntimeError):
            await communicator.receive_from()
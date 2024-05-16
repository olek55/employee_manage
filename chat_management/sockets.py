import socketio
from django.conf import settings
import json
from users.models import UserAccount
from .models import Chat, ChatMessage
from .serializers import MessageSerializer
from asgiref.sync import sync_to_async
from rest_framework.response import Response
from rest_framework import status
import threading
import asyncio

mgr = socketio.AsyncRedisManager(settings.CHAT_REDIS_URL)
sio = socketio.AsyncServer(
    async_mode="asgi",
    client_manager=mgr,
    cors_allowed_origins="*",
    logger=True,
)
chat_id = (
    "7ce6aa6a-208a-4c1e-8f96-ebeb8eb16996"  # this id is used for webhook for esignature
)


# establishes a connection with the client
@sio.on("connect")
async def connect(sid, env, auth):
    print("SocketIO connect")
    await sio.enter_room(sid, chat_id)
    # if auth:
    #     chat_id = auth["chat_id"]
    #     print("SocketIO connect")
    #     sio.enter_room(sid, chat_id)
    #     await sio.emit("connect", f"Connected as {sid}")
    # else:
    #     raise ConnectionRefusedError("No auth")


# communication with orm
def store_and_return_message(data):
    print(data)
    data = json.loads(data)
    sender_id = data["sender_id"]
    chat_id = data["chat_id"]
    text = data["text"]
    try:
        sender = UserAccount.objects.get(id=sender_id)
    except UserAccount.DoesNotExist:
        return Response("Sender does not exist!", status=status.HTTP_404_NOT_FOUND)
    try:
        chat = Chat.objects.get(short_id=chat_id)
    except Chat.DoesNotExist:
        chat = Chat.objects.create(short_id=chat_id)
    # sender = get_object_or_404(UserAccount, id=sender_id)
    # chat = get_object_or_404(Chat, short_id=chat_id)

    instance = ChatMessage.objects.create(sender=sender, chat=chat, text=text)
    instance.save()
    message = MessageSerializer(instance).data
    message["chat"] = chat_id
    message["sender"] = str(message["sender"])
    return message


# listening to a 'message' event from the client
@sio.on("message")
async def print_message(sid, data):
    print("Socket ID", sid)
    message = await sync_to_async(store_and_return_message, thread_sensitive=True)(
        data
    )  # communicating with orm
    # await sio.emit("new_message", message, room=message["chat"])


@sio.on("disconnect")
async def disconnect(sid):
    print("SocketIO disconnect")


def send_contract_sign_confirmation_message(data):
    print(data)
    print("CHATID=", chat_id)

    # sio.emit("new_message", data, room=chat_id)
    async def emit():
        print("EMITTING")
        await sio.emit("contract_signed", data, room=chat_id)
        asyncio.sleep(1)

    def run_event_loop():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(emit())
        loop.close()

    thread = threading.Thread(target=run_event_loop)
    thread.start()
    thread.join()

from django.urls import path
from .views import GetChat

urlpatterns = [
    path("all", GetChat.as_view(), name="get-chats"),
]

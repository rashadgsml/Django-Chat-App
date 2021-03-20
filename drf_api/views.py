from django.shortcuts import render
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from .serializers import ChatSerializer, ProfileSerializer
from chat.models import Chat, Profile
from rest_framework.mixins import (ListModelMixin, CreateModelMixin, RetrieveModelMixin,
                                                    UpdateModelMixin, DestroyModelMixin)
from rest_framework import status, permissions
from rest_framework.generics import ListCreateAPIView

class ChatList(ListModelMixin,
                CreateModelMixin,
                GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ChatDetail(RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

class ProfileList(ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProfileDetail(RetrieveModelMixin,
                    UpdateModelMixin,
                    DestroyModelMixin,
                    GenericAPIView,
                    ):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
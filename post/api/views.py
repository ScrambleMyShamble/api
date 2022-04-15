from rest_framework import status
from rest_framework.decorators import api_view
from notes.models import Note
from .serializers import NoteSerializer, NoteThinSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework import views, mixins
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model


class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )


# ModelViewSet наследуется от mixins
class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    # http_method_names = ['get', 'post'] # выбираем список доступных методов

    def list(self, request, *args, **kwargs):
        note = Note.objects.all() #(author=request.user.id) авторы будут видеть только свои note
        context = {'request': request}
        serializer = NoteThinSerializer(note, many=True, context=context)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # привязывем создаваемые note к юзерам
        serializer.save(author=self.request.user)



#                                    представления на основе generic
# class NoteListView(ListCreateAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def list(self, request, *args, **kwags):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = NoteThinSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#
# class NoteDetailView(RetrieveUpdateDestroyAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer


#                                    представления на основе mixin
# class NoteListView(mixins.ListModelMixin, mixins.CreateModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         self.serializer_class = NoteThinSerializer
#         return self.list(request, *args, **kwargs)
#
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)
#
#
# class NoteDetailView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, GenericAPIView):
#     queryset = Note.objects.all()
#     serializer_class = NoteSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


#                                              Представления на основе классов
# class NoteListView(views.APIView):
#     def get(self, request, format=None):
#         notes = Note.objects.all()
#         context = {'request': request}
#         serializer = NoteSerializer(notes, many=True, context=context)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
#
#
# class NoteDetailView(views.APIView):
#     def get_object(self, pk):
#         try:
#             return Note.objects.get(pk=pk)
#         except Note.DoesNotExists:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def get(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         note = self.get_object(pk)
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, pk, format=None):
#         note = self.get_object(pk)
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


#                                                Представления на основе функций
# @api_view(['GET', 'POST']) - в api_view прописывается какой функционал может предоставить декарированный метод
# def notes_list(request, format=None):
#     if request.method == 'GET':
#         note = Note.objects.all()
#         serializer = NoteSerializer(note, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = NoteSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def notes_detail(request, pk, format=None):
#     try:
#         note = Note.objects.get(pk=pk)
#     except Note.DoesNotExist:
#         return Response(status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = NoteSerializer(note)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = NoteSerializer(note, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         note.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

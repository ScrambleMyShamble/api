from django.urls import path
# from .views import notes_detail, notes_list - функции
from .views import NoteViewSet, UserViewSet #NoteListView, NoteDetailView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


# на основе ModelViewSet с помощью DefaultRouter. Роутер сам генерирует ссылки
router = DefaultRouter()
router.register('notes', NoteViewSet, basename='notes')
router.register('users', UserViewSet, basename='users')
urlpatterns = router.urls

# на основе ModelViewSet. Необходимо явно прописать соответствия между http методами(get, put, post, patch, delete)
# и методами ModelViewSet в ручную или с помощью DefaultRouter
# notes_list = NoteViewSet.as_view({
#     'get': 'list',
#     'post': 'create'
# })
# notes_detail = NoteViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })
# urlpatterns = [
#     path('notes/', notes_list, name='notes-list'),
#     path('notes<int:pk>/', notes_detail, name='notes-detail'),
# ]

# url на основе функций
# urlpatterns = [
#     path('notes', notes_list),
#     path('notes/<int:pk>/', notes_detail),
# ]


# на основе классов, generic, mixin, ко всем можно применить as_view()
# urlpatterns = [
#     path('notes/', NoteListView.as_view()),
#     path('notes/<int:pk>/', NoteDetailView.as_view(), name='notes-detail')
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)

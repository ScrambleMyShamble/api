from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField, SerializerMethodField
from notes.models import Note
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ('id', 'email', 'password', 'name', 'admin')
        extra_kwargs = {'password': {'write_only': True}} # в этой переменной поля только для записи.

    def create(self, validated_data):
        password = validated_data.pop('password', '')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)


# сериализатор через model, похожу на ModelForm, на основании модели создается сериализатор.
class NoteSerializer(serializers.ModelSerializer):
    author = SerializerMethodField(read_only=True) # делаем поле author неизменяемым + нужно написать
    # метод get_имяполя.

    def get_author(self, obj):
        return str(obj.author.email)

    class Meta:
        model = Note
        fields = '__all__'


class NoteThinSerializer(serializers.ModelSerializer):
    url = HyperlinkedIdentityField(view_name='notes-detail') # ссылка на notedetail в notelistview

    class Meta:
        model = Note
        fields = ('id', 'title', 'text', 'url')


# самописный сериализатор с полями, которые есть в модели, для сериализации каждого поля в ручную
# class NoteSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(required=True, max_length=200)
#     text = serializers.CharField(required=False, allow_blank=True)
#
#     def create(self, validated_data):
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title', instance.title)
#         instance.text = validated_data.get('text', instance.text)
#         instance.save()
#         return instance

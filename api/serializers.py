from rest_framework import serializers
from django.contrib.auth.models import User
from items.models import Item, FavoriteItem


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'first_name', 'last_name']
	def create(self, validated_data):
		username = validated_data['username']
		password = validated_data['password']
		first_name = validated_data['first_name']
		last_name = validated_data['last_name']
		new_user = User(username=username)
		new_user.set_password(password)
		new_user.first_name=first_name
		new_user.last_name=last_name
		new_user.save()
		return validated_data




class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name' , 'last_name']


class ItemListSerializer(serializers.ModelSerializer):
	added_by=UserSerializer()
	favourited = serializers.SerializerMethodField()
	detail = serializers.HyperlinkedIdentityField(
		view_name = "api-detail",
		lookup_field = "id",
		lookup_url_kwarg = "item_id"
		)
	class Meta:
		model = Item
		fields = ['id', 'name', 'added_by','detail', 'favourited',]
	def get_favourited(self,obj):
		favorites = FavoriteItem.objects.filter(user=obj.added_by)
		count = 0
		for fav in favorites:
			count += 1
		return count


class ItemDetailsSerializer(serializers.ModelSerializer):
	favourited_by = serializers.SerializerMethodField()

	class Meta:
		model = Item
		fields = ['image', 'added_by', 'name', 'favourited_by']

	def get_favourited_by(self,obj):
		favorites = FavoriteItem.objects.filter(user=obj.added_by)
		return favorites

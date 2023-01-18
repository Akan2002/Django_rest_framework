from rest_framework import serializers, exceptions
from mainapp.models import (
    Category, Product,Comment,
)
from mainapp.models import (
    Category, Product,Comment,
)
class ProductSerializer(serializers.ModelSerializer):
    # category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = Product
        fields = (
            'id','category', 'name', 'price', 'description', 'image',
            # 'category.name',
        )
        read_only_fields = (
            'category', 
        )
class CommentSerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Comment
        fields = (
            'id', 'raiting', 'user', 'comment_text', 'created_at', 'product',
        )
        read_only_fields = (
            'created_at', 'user', 'product',
        )


class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = (
            'id', 'name', 'image',
            'products',
        )






class RegistrationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.CharField()

    def validate_password(self, value):
        if len(value) < 8:
            raise exceptions.ValidationError('Password is too short')
        elif len(value) > 8:
            raise exceptions.ValidationError('Password is too long')
        return value
class AuthorizationSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()    


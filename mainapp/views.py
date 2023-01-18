from rest_framework.viewsets import ModelViewSet
from mainapp.serializers import (
    CategorySerializer, ProductSerializer, CommentSerializer, RegistrationSerializer,AuthorizationSerializer,
)

from mainapp.models import (
    Category, Product , Comment,
)
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from mainapp.send_gmail import send_msg

class CategoryView(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(methods=[ 'post', ], detail=True, serializer_class= ProductSerializer,     permission_classes = (permissions.IsAuthenticatedOrReadOnly,))
    def add_product(self, requst, *args, **kwargs):
        category = self.get_object()
        # user = requst.user
        serializer = ProductSerializer(data=requst.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        product = Product.objects.create(
            # user = user,
            category = category,
            description = data.get ('description'),
            name = data.get ('name'),
            price = data.get ('price'),
            image = data.get ('image'),
        )
        return Response(ProductSerializer(product).data)
    # @action(methods=['post'], detail=True, serializer_class = ProductSerializer)

class ProductView(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter,
        filters.OrderingFilter,
    )

    filterset_fields = (
        'name', 'category__name',
    )
    search_fields = (
        'name', 'category__name',
    )
    ordering_fields = (
        'price', 'id',
    )

    @action(methods=[ 'post', ], detail=True, serializer_class= CommentSerializer)
    def add_comment(self, requst, *args, **kwargs):
        product = self.get_object()
        user = requst.user
        serializer = CommentSerializer(data=requst.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        comment = Comment.objects.create(
            user = user,
            product = product,
            raiting = serializer.validated_data.get ('raiting'),
            comment_text = serializer.validated_data.get ('comment_text'),
        )
        return Response(CommentSerializer(comment).data)

class CommentView(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def perform_create(self, serializer):
        return serializer.save(user = self.request.user)

class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username = username).exists():
            return Response({'message': 'Username with such username is already exist'})
        user = User.objects.create_user(
            username = username,
            password = password,
            email = email,
        )
        send_msg(email=email, username=username)    
        token = Token.objects.create(user = user)
        return Response({'token': token.key})
class AuthoriationView(APIView):
    def post(self, request):
        serializer = AuthorizationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username).first()

        if user is not None:
            if check_password(password, user.password):
                token, _=Token.objects.get_or_create(user=user)
                return Response({'token':token.key})
            return Response({'error': 'Password is not vallid'}, status=400)
        return Response({'error': 'username is not registered'}, status=400)
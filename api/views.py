from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from . import serializers
from main import models


from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status


@api_view(['GET'])
def list_products(request):
    products = models.Product.objects.all()
    serializer = serializers.ListProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([IsAuthenticated])
def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    product_ser = serializers.DetailProductSerializer(product)
    return Response(product_ser.data)


@api_view(['GET'])
def category_list(request):
    categorys = models.Category.objects.all()
    serializer = serializers.CategorySerializer(categorys, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def category_detail(request, slug):
    products = models.Product.objects.filter(category__slug = slug)
    serializer = serializers.ListProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def log_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        data = {
            'token':token.key,
            'status':status.HTTP_200_OK
        }
    else:
        data = {'status':status.HTTP_404_NOT_FOUND}
    return Response(data)


@api_view(['POST'])
def register_user(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = User.objects.create_user(
        username=username, 
        password=password)
    token = Token.objects.create(user=user)

    return Response({
        'username':user.username,
        'token':token.key}
        )


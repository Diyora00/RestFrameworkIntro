from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken


class LoginModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(username=obj['username'])
        refresh = RefreshToken.for_user(user)
        return {
            'username': user.username,
            'email': user.email,
            'tokens': {
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }
        }

    class Meta:
        model = User
        fields = ['username', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', )
        password = attrs.get('password', )
        user = auth.authenticate(username=username, password=password)
        if not user:
            raise AuthenticationFailed('Bad credentials')
        if not user.is_active:
            raise AuthenticationFailed('User inactive or deleted')
        return attrs


class LoginAPIView(APIView):
    serializer_class = LoginModelSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh = request.data['refresh']
            RefreshToken(refresh).blacklist()
            data = {
                'message': 'Token is added to the blacklist'
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name', ]
        extra_kwargs = {
            'password': {"write_only": True}
        }

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            detail = {
                "detail": "User already exist!"
            }
            raise serializers.ValidationError(detail=detail)
        return username

    def validate(self, instance):
        if instance['password'] != instance['password2']:
            raise serializers.ValidationError({"message": "Passwords do not match"})

        if User.objects.filter(email=instance['email']).exists():
            raise serializers.ValidationError({"message": "Email already exists !"})

        return instance

    def create(self, validated_data):
        password2 = validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        user.is_staff = True
        user.save()
        return user


class RegisterAPIView(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = User.objects.get(username=serializer.data['username'])
            refresh = RefreshToken.for_user(user)
            data = {
                'success': True,
                'user': serializer.data,
                'tokens': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }
            return Response(data, status=status.HTTP_201_CREATED)

from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken as OAT
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView as TOPV
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.conf import settings

import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from serializers.accounts.serializers import RegistrationModelSerializer, AuthTokenSerializer, TokenObtainPairSerializer, ChangePasswordSerializer, ProfileModelSerializer
from accounts.models import Profile
from handlers.accounts.activation import Activation

User = get_user_model()

class RegistrationApiView(GenericAPIView):
    serializer_class = RegistrationModelSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            object = serializer.save()
            email = serializer.validated_data['email']

            response = {
                'email': email,
                'id': object.id
            }

            user = get_object_or_404(User, email=email)
            Activation.activate_with_email(user)
            
            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthToken(OAT):

    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class DiscardAuthToken(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TokenObtainPairView(TOPV):
    serializer_class = TokenObtainPairSerializer


class ChangePasswordGenericView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)

            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            return Response({'detail': 'Password updated successfully'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileViewSet(ViewSet):
    serializer_class = ProfileModelSerializer
    queryset = Profile.objects.all()

    def retrieve(self, request, pk=None):
        profile = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.queryset.get(pk=kwargs.get('pk'))
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def me(self, request):
        profile = get_object_or_404(self.queryset, user=request.user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data)
    

class ActivationEmailViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        return Activation.activate_with_email(user)
    
    def post(self, request, *args, **kwargs):
        try:
            token = jwt.decode(kwargs.get('token'), settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(pk=token.get('user_id'))
            
            if user.is_verified:
                return Response({'details': 'Account is Already Verified!'}, status=status.HTTP_200_OK )
            else:
                user.is_verified = True
                user.save()
                return Response({'details': 'Account Activated Successfully!'}, status=status.HTTP_200_OK )
            
        except ExpiredSignatureError:
            return Response({'detials': 'Token Has Been Expired!'}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidSignatureError:
            return Response({'detials': 'Token is Invalid!'}, status=status.HTTP_400_BAD_REQUEST)
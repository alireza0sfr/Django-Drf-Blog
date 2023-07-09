from rest_framework.serializers import ModelSerializer, CharField, Serializer, ValidationError as RestValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer as TOPS
from phonenumber_field.validators import validate_international_phonenumber, ValidationError as PhoneNumberValidationError

from accounts.models import Profile

User = get_user_model()


class RegistrationModelSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password', 'phone_number',
                  'is_active', 'is_anonymous', 'is_verified', 'is_staff']

    def validate(self, attrs):

        if attrs.get('password') != attrs.get('confirm_password'):
            raise RestValidationError({'detail': "password doesn't match"})

        try:
            validate_password(attrs.get('password'))
        except DjangoValidationError as e:
            raise RestValidationError({'password': list(e.messages)})
        
        if attrs.get('phone_number'):
            try:
                validate_international_phonenumber(attrs.get('phone_number'))
            except PhoneNumberValidationError as e:
                raise RestValidationError({'phone_number': list(e.messages)})
        
        return super().validate(attrs)

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return User.objects.create_user(**validated_data)


class AuthTokenSerializer(Serializer):
    email = CharField(
        label=_("Email"),
        write_only=True
    )
    password = CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise RestValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise RestValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class TokenObtainPairSerializer(TOPS):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        validated_data['email'] = self.user.email
        validated_data['user_id'] = self.user.id
        return validated_data


class ChangePasswordSerializer(Serializer):

    old_password = CharField(required=True)
    new_password = CharField(required=True)
    confirm_password = CharField(required=True)

    def validate(self, attrs):

        if attrs.get('new_password') != attrs.get('confirm_password'):
            raise RestValidationError({'detail': "password doesn't match"})

        try:
            validate_password(attrs.get('new_password'))
        except DjangoValidationError as e:
            raise RestValidationError({'new_password': list(e.messages)})

        return super().validate(attrs)


class ProfileModelSerializer(ModelSerializer):

    class Meta:
        model = Profile
        fields = ['id', 'user', 'first_name', 'last_name', 'full_name', 'image', 'bio', 'created_date']
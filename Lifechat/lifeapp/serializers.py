from rest_framework import serializers
from django.contrib.auth.models import User
from lifeapp.models import Profile,Connection

from django.contrib.auth import authenticate   #14 sept
from django.db.models import Q 

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=6)
    password2=serializers.CharField(write_only=True,min_length=6)
    phone_number=serializers.CharField(max_length=15)
    address = serializers.CharField(max_length=255, required=False, allow_blank=True)
    blood_group=serializers.ChoiceField(choices=Profile.BLOOD_GROUP_CHOICES)
    city=serializers.CharField(max_length=50)
    account_type=serializers.ChoiceField(choices=Profile.ACCOUNT_TYPE_CHOICES,default='Public')

    def validate_username(self,data):
        if User.objects.filter(username=data).exists():
            raise serializers.ValidationError("Username already taken, veere username nooktto😊")
        return data

    def validate_email(self, data):
        if User.objects.filter(email=data).exists():
            raise serializers.ValidationError("Email already registerd, veere email try cheyyuu🌝")
        return data

    def validate(self, data):
        if data['password']!=data['password2']:
            raise serializers.ValidationError({"password do not match"})
        return data

    def validate_phone_number(self, data):
            if Profile.objects.filter(phone_number=data).exists():
                raise serializers.ValidationError("Phone number already registerd analloo")
            return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user=User.objects.create_user(
             username=validated_data['username'],
             email=validated_data['email'],
             password=validated_data['password']
        )
        Profile.objects.create(
             user=user,
             phone_number=validated_data['phone_number'],
             address=validated_data.get('address',''),
             blood_group=validated_data['blood_group'],
             city=validated_data['city'],
             account_type=validated_data.get('account_type','public'),
             blood_status='available',
             badge_tier='none'
             
        )
        return user


# 14 sept

class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField(write_only=True)

    def validate(self, data):
        user=authenticate(username=data['username'],password=data['password'])
        if not user:
            raise serializers.ValidationError("invalid usernam eor passsword")
        data['user']=user
        return data


class ConnectionRequestSerializer(serializers.Serializer):
    to_user_id=serializers.IntegerField()

    def validate(self, data):
        request_user=self.context['request'].user
        to_user_id=data['to_user_id']

        if to_user_id==request_user.id:
            raise serializers.ValidationError("enthonna kanikkane , agage onnum request edan pattula, cannod send request to yourself")

        if not User.objects.filter(id=to_user_id).exists():
            raise serializers.ValidationError("agane oru user ellalloo👀")

        if Connection.objects.filter(from_user=request_user, to_user_id=to_user_id).exists():
            raise serializers.ValidationError("oruvattam request etta pore , pinnem pinnem onnum edan pattulatto")

        return data

    def create(self, validated_data):
        request_user=self.context['request'].user
        return Connection.objects.create(
            from_user=request_user,
            to_user_id=validated_data['to_user_id']
        )

class ConnectionSerializer(serializers.ModelSerializer):
    from_username=serializers.CharField(source='from_user.username',read_only=True)
    to_username=serializers.CharField(source='to_user.username',read_only=True) 

    class Meta:
        model = Connection
        fields=['id','from_username','to_username','status','created_at']   
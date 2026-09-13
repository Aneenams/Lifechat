from rest_framework import serializers
from django.contrib.auth.models import User
from lifeapp.models import Profile

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField(max_length=50)
    email=serializers.EmailField()
    password=serializers.CharField(write_only=True,min_length=6)
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

    def validate_phone_number(self, data):
            if Profile.objects.filter(phone_number=data).exists():
                raise serializers.ValidationError("Phone number already registerd analloo")
            return data
    
    def create(self, validated_data):
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

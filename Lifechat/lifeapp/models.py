from django.db import models
from django.contrib.auth.models import User
# Create your models here.



class Profile(models.Model):
    BLOOD_GROUP_CHOICES=(
        ('A+','A+'),('A-','A-'),
        ('B+','B+'),('B-','B-'),
        ('O+','O+'),('O-','O-'),
        ('AB-','AB-'),('AB+','AB+'),
    )
    ACCOUNT_TYPE_CHOICES=(
            ('private','Private'),
            ('public','Public')
    )
    ADDRESS_VISIBILITY_CHOICES=(
        ('private','Private'),
        ('public','Public'),
        ('friends','Friends Only'),
    )
    BLOOD_STATUS_CHOICES = (
        ('available', 'Available'),
        ('recently_donated', 'Recently Donated'),
        ('unavailable_medical', 'Temporarily Unavailable - Medical'),
        ('not_available', 'Not Available')
    )
    BADGE_TIER_CHOICES=(
        ('none', 'None'),
        ('bronze', 'Bronze'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
    )

    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    phone_number=models.CharField(max_length=12,unique=True)
    address=models.CharField(max_length=100,blank=True,null=True)
    address_visibility=models.CharField(max_length=20,choices=ADDRESS_VISIBILITY_CHOICES)
    account_type=models.CharField(max_length=20,choices=ACCOUNT_TYPE_CHOICES)
    blood_group=models.CharField(max_length=10,choices=BLOOD_GROUP_CHOICES)
    blood_status=models.CharField(max_length=20,choices=BLOOD_STATUS_CHOICES,default=None)
    city=models.CharField(max_length=50)
    donation_availability=models.DateField(null=True,blank=True)
    badge_tier=models.CharField(max_length=10,choices=BADGE_TIER_CHOICES,default=None)
    verified_donation_count=models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.blood_group} "




from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(max_length=200,unique=True)
    full_name=models.CharField(max_length=50)
    phone_number=models.CharField(max_length=11,unique=True)
    is_active=models.BooleanField(default=True)
    is_admin=models.BooleanField(default=False)
     
    USERNAME_FIELD='phone_number'
    REQUIRED_FIELDS=['email','full_name']
    objects=UserManager()
    
    def __str__(self):
       return self.email
   
   #  def has_perm(self,perm,obj=None):
   #     return True 
   
   #  def has_module_perms(self,app_label):
   #     return True
    @property
    def is_staff(self):
        return self.is_admin
     
   
     
     
     
class OtpCode(models.Model):
   phone_number=models.CharField(max_length=11)
   code=models.PositiveSmallIntegerField()
   created=models.DateTimeField(auto_now=True)
   
   def __str__(self):
       return f'{self.phone_number}--{self.code}--{self.created}'
   
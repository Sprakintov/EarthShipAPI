from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# class CustomUserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         return self.create_user(email, password, **extra_fields)

# class CustomUser(AbstractUser):
#     username = None
#     email = models.EmailField(unique=True)
#     phone_number = models.CharField(max_length=20)
#     address = models.TextField()
#     is_customer = models.BooleanField(default=True)
#     is_agent = models.BooleanField(default=False)
    
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []
    
#     objects = CustomUserManager()
    
#     def __str__(self):
#         return self.email



class Users(models.Model):
    userID= models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    mobile_number = models.CharField(max_length=15)
    mailAddress = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    user_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_creation_date_time = models.DateTimeField(auto_now_add=True)   
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Agent(Users):
    agent_id = models.AutoField(primary_key=True)
    agent_status = models.CharField(max_length=50)
    agent_creation_date_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'

  
class Customer(Users):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(Users, on_delete=models.CASCADE, related_name='customer_profile')
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    ESCoins = models.IntegerField(default=500)
    ref_date = models.DateTimeField(auto_now_add=True)
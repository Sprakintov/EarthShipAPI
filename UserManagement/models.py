from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, AbstractUser
from django.db import models
from api import models as api_models
# from Base.models import Countries


# class Users(AbstractUser):
#     userID= models.AutoField(primary_key=True)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     birth_date = models.DateField(null=True)
#     mobile_number = models.CharField(max_length=15)
#     mailAddress = models.CharField(max_length=100)
#     # password = models.CharField(max_length=128)
#     username = models.CharField(max_length=100, unique=True)
#     # created_at = models.DateTimeField(auto_now_add=True)
#     user_creation_date_time = models.DateTimeField(auto_now_add=True)   
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'
#         swappable = 'AUTH_USER_MODEL'




class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    def create_user(self,username, password=None):
        """Create a new user profile"""
        if not username:
            raise ValueError('Users must have an email address')
        # email = self.normalize_email(email)
        user = self.model(username=username)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(username, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user




class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""

    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null= True,blank=True)
    birth_date = models.DateField(null= True,blank=True)
    mobile_number = models.CharField(max_length=15,null=  True,blank=True)
    username = models.CharField(max_length=100, unique=True,null= True,blank=True)
    user_creation_date_time = models.DateTimeField(auto_now_add=True,null=True,blank=True)   
    email = models.EmailField(max_length=255,unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['']

    def get_full_name(self):
        """Retrieve full name of user"""
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.first_name

    def __str__(self):
        """Return string representation of our user"""
        return self.username

class Agent(UserProfile):
    agent_id = models.AutoField(primary_key=True)
    agent_status = models.CharField(max_length=50)
    agent_creation_date_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = 'Agent'
        verbose_name_plural = 'Agents'


class Countries(models.Model):
    countryID = models.AutoField(primary_key=True)
    countryName = models.CharField(max_length=100)
    countryISO = models.CharField(max_length=10)
    countryCode = models.CharField(max_length=10)
    countryCurrency = models.CharField(max_length=10)
    countryLanguage = models.CharField(max_length=50)
    countryCapital = models.CharField(max_length=100)
    countryPopulation = models.IntegerField()
    countryArea = models.FloatField()
    # countryFlag = models.ImageField(upload_to='country_flags')
    countryContinent = models.CharField(max_length=50)
    countryCurrencySymbol = models.CharField(max_length=10)
    countryCurrencyCode = models.CharField(max_length=10)
    countryCurrencyName = models.CharField(max_length=50)
    countryCurrencySymbol = models.CharField(max_length=10)
    countryCurrencyRate = models.FloatField()
    countryTimezone = models.CharField(max_length=50)
    countryTimezoneGMT = models.CharField(max_length=10)
    countryTimezoneDST = models.CharField(max_length=10)
    countryTimezoneDSTStart = models.DateTimeField()
    countryTimezoneDSTEnd = models.DateTimeField()

    def __str__(self):
        return self.countryName

    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = 'Countries'
        ordering = ['countryName']



class Customer(UserProfile):
    customer_id = models.AutoField(primary_key=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    ESCoins = models.IntegerField(default=500)
    # refUser = models.ForeignKey('self', on_delete=models.CASCADE, related_name='referral_user', null=True, blank=True)
    refDate = models.DateTimeField(auto_now_add=True)

    def add_balance(self, amount):
        """Add balance to the customer's account."""
        self.balance += amount
        self.save()

    def deduct_balance(self, amount):
        """Deduct balance from the customer's account."""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False

    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'


    
class PaymentMethod(models.Model):
    payment_method_id = models.AutoField(primary_key=True)
    cardNumber = models.CharField(max_length=16,null=True,blank=True)
    card_holder_name = models.CharField(max_length=100)
    cvv = models.CharField(max_length=4)
    expiry = models.DateField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_payment_methods',null=True,blank=True)


class Address(models.Model):
    addressID = models.AutoField(primary_key=True)
    default = models.BooleanField(default=False)
    senderFullName = models.CharField(max_length=100)
    senderMailAddress = models.CharField(max_length=100)
    addressLine1 = models.CharField(max_length=255)
    addressLine2 = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipCode = models.CharField(max_length=20)
    country = models.ForeignKey(Countries, on_delete=models.CASCADE, related_name='country_addresses', null=True, blank=True)
    addressType = models.CharField(max_length=5)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_addresses')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Referral(models.Model):
    referralID = models.AutoField(primary_key=True)
    referralCode = models.CharField(max_length=50)
    referralCreationDateTime = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)



    
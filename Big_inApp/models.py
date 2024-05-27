from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    USER_TYPES = [
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    ]
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='buyer')
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    def is_buyer(self):
        return self.user_type == "buyer"

    def is_seller(self):
        return self.user_type == "seller"

    def __str__(self):
        return self.email


class BuyerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='buyer_profile')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SellerProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='seller_profile')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    dob = models.DateField()
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='seller_photos/')
    citizenship_card = models.ImageField(upload_to='seller_citizenship_cards/')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by: {self.name}"


class ProductCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


STATUS = (
    (0, "Draft"),
    (1, "Publish")
)


class ProductSellEntry(models.Model):
    seller_profile = models.ForeignKey(SellerProfile, on_delete=models.CASCADE, related_name='products')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    photo = models.ImageField(upload_to='product_owner_photos/')
    citizenship = models.CharField(max_length=100)
    product_name = models.CharField(max_length=200)
    product_image = models.ImageField(upload_to='product_images/')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    offered_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.IntegerField(choices=STATUS, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.product_name} by {self.first_name} {self.last_name}"


class Article(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    cover_img = models.ImageField(upload_to='article_covers/')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Order(models.Model):
    product = models.ForeignKey(ProductSellEntry, on_delete=models.CASCADE)
    ordered_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    ordered_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Video(models.Model):
    title = models.CharField(max_length=255)
    video_id = models.FileField(upload_to='uploads/')  # Assuming YouTube video IDs are 11 characters long

    def __str__(self):
        return self.title


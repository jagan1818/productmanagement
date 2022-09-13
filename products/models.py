from statistics import mode
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    class Meta:
        abstract = True

class Role(BaseModel):
    role = models.CharField(max_length=255)
    
    def __str__(self):
        return self.role

    class Meta:
        db_table = 'role'

class UserProfile(BaseModel):
    phone = models.PositiveBigIntegerField()
    role  = models.ForeignKey('Role', on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_profile'

class Products(BaseModel):
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField()
    product_description = models.TextField(blank=True)
    inventory_count = models.IntegerField()

    def __str__(self):
        return self.product_name

    class Meta:
        db_table = 'products'

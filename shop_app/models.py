from django.db import models

from auth_user.models import UserProfile, CustomModelUser


class Brand(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class CategoryCHOICES(models.TextChoices):
    NOTEBOOK = 'notebook'
    DISHWASHER = 'dishwasher'
    VACUUM_CLEANER = 'vacuumCleaner'
    TV = 'tv'


class Products(models.Model):
    description = models.TextField()
    model = models.CharField(max_length=128)
    price = models.FloatField()
    color = models.CharField(max_length=30)
    warranty = models.IntegerField()
    count = models.IntegerField()
    brand_name = models.ForeignKey(Brand, on_delete=models.CASCADE, default=None)
    category = models.CharField(max_length=150, choices=CategoryCHOICES.choices)

    def __str__(self):
        return f'{self.category} {self.brand_name} {self.model}'


class Notebook(Products):
    display = models.DecimalField(max_digits=5, decimal_places=3)
    memory = models.IntegerField()
    video_memory = models.IntegerField()
    cpu = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.brand_name} {self.model} ({self.__class__.__name__})'


class Dishwasher(Products):
    energy_saving_class = models.CharField(max_length=2, default='A+')
    power = models.IntegerField(default=0)
    width = models.FloatField()
    height = models.FloatField()

    def __str__(self):
        return f'{self.brand_name} {self.model} ({self.__class__.__name__})'


class VacuumCleaner(Products):
    noise_level = models.FloatField()
    power = models.IntegerField()
    width = models.FloatField()
    height = models.FloatField()
    eco_engine = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.brand_name} {self.model} ({self.__class__.__name__})'


class TV(Products):
    display = models.DecimalField(max_digits=5, decimal_places=3)
    memory = models.IntegerField()
    display_type = models.CharField(max_length=8)
    smart_tv = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.brand_name} {self.model} ({self.__class__.__name__})'


class Backpack(models.Model):

    # backpack_manager = models.Manager()

    bayer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.bayer.user.username}___{self.product}"


class ShoppingList(models.Model):
    bayer_archive = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    id_product_archive = models.IntegerField()
    model = models.CharField(max_length=128)
    price = models.FloatField()
    warranty = models.IntegerField()
    count = models.IntegerField()
    brand_name = models.CharField(max_length=64)
    category = models.CharField(max_length=64)
    purchase_date = models.DateField(auto_now=True, blank=True,
                                     null=True)

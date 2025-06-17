from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth import get_user_model
from . import utils

# from django.db.models.signals import pre_save
# from django.dispatch import receiver

User = get_user_model()


class ProductCategory(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=200, null=False)
    slug = models.SlugField(max_length=100, null=False, blank=True, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=150, null=False)
    description = models.TextField(max_length=5000, null=False)
    slug = models.SlugField(max_length=300, null=False, blank=True, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    discount_price = models.DecimalField(max_digits=5, decimal_places=2, null=False, default=0.00)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.URLField(null=False, default=utils.get_product_defult_image_url)
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        limit_choices_to={"is_vendor": True},
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        return super().save(*args, **kwargs)


# @receiver(pre_save, sender=Product)
# def pre_save_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = utils.unique_slug_generator(instance)

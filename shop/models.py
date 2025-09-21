from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

"""
adrees
phone number 
location gis
نمایندگی کجاها دارد
description
"""

class Shop(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    title = models.CharField(max_length=200,unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=200)
    postal_code = models.CharField(max_length=10)
    description = models.TextField()
    phone_number = models.CharField(max_length=20)
    admins = models.ManyToManyField(User, related_name='Admins')


    def __str__(self):
        return f"{self.owner.phone_number} - {self.title}"

class Category(models.Model):
    title = models.CharField(max_length=200)
    sub_category = models.ForeignKey(
        'self', on_delete=models.CASCADE,
        related_name='sub_categories', null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)

    def __str__(self):
        return self.title or "Untitled Category"

    def get_absolute_url(self):
        if not self.slug:
            # Generate a slug if it's empty
            self.slug = slugify(self.title, allow_unicode=True)
            if not self.slug:
                self.slug = f"category-{self.id or 'new'}"
            # Save the object if it has an ID (already exists in the database)
            if self.id:
                self.save(update_fields=['slug'])
        return reverse('shop:filter_by_category', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs): # new
        if not self.title:
            self.title = "Untitled Category"
        self.slug = slugify(self.title, allow_unicode=True)
        if not self.slug:
            # If slugify returns empty (e.g., for non-Latin characters)
            # Use a default slug with the ID
            self.slug = f"category-{self.id or 'new'}"
        return super().save(*args, **kwargs)

"""
for which car
brand 
company name
price date 
garanty darad ya na
چند ماه گارانتی دارد 
"""




class CarBrand(models.Model):
    """Car manufacturers like Toyota, Honda, BMW, etc."""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.name, allow_unicode=True) or f"brand-{self.pk or ''}"
            slug = base
            i = 1
            # تضمین یکتایی
            while CarBrand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('shop:car_brand_articles', kwargs={'brand_slug': self.slug})
class CarModel(models.Model):
    """Specific car models like Corolla, Civic, 3-Series, etc."""
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='car_models')
    name = models.CharField(max_length=100)
    year_start = models.PositiveIntegerField(null=True, blank=True)  # Optional start year
    year_end = models.PositiveIntegerField(null=True, blank=True)    # Optional end year
    
    class Meta:
        unique_together = ('brand', 'name')
        
    def __str__(self):
        return f"{self.brand} {self.name}"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='shop')
    image = models.ImageField(upload_to='products')
    main_image = models.ImageField(upload_to='products', null=True, blank=True)
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.IntegerField()
    discount_price = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, allow_unicode=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(max_length=100, help_text="Color of the product", default="balck")
    number_of_sales = models.PositiveIntegerField(default=0)
    compatible_cars = models.ManyToManyField(CarModel, related_name='compatible_products')
    brand = models.CharField(max_length=100, help_text="Brand of the product")
    manufacturer = models.CharField(max_length=100, help_text="Company that manufactured the product")
    price_valid_until = models.DateField(null=True, blank=True)
    has_warranty = models.BooleanField(default=False)
    warranty_months = models.PositiveIntegerField(default=0, help_text="Number of months of warranty")
    stock = models.PositiveBigIntegerField(default=0)
    
    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.title or "Untitled Product"
        
    def get_absolute_url(self):
        if not self.slug:
            # Generate a slug if it's empty
            self.slug = slugify(self.title, allow_unicode=True)
            if not self.slug:
                self.slug = f"product-{self.id or 'new'}"
            # Save the object if it has an ID (already exists in the database)
            if self.id:
                self.save(update_fields=['slug'])
        return reverse('shop:product_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = "Untitled Product"
        self.slug = slugify(self.title, allow_unicode=True)
        if not self.slug:
            # If slugify returns empty (e.g., for non-Latin characters)
            # Use a default slug with the ID
            self.slug = f"product-{self.id or 'new'}"
        return super().save(*args, **kwargs)
    


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products')
    alt_text = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.product.title} - {self.id}"
    


class CarArticle(models.Model):
    car_brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE, related_name='articles')
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(unique=True, allow_unicode=True, verbose_name="اسلاگ")
    content = models.TextField(verbose_name="محتوای مقاله")
    image = models.ImageField(upload_to='car_articles', verbose_name="تصویر مقاله")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    def __str__(self):
        return f"{self.car_brand.name} - {self.title}"
    
    def get_absolute_url(self):
        return reverse('shop:car_article_detail', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        return super().save(*args, **kwargs)
    
    def get_related_products(self):
        """دریافت محصولات مرتبط با این برند خودرو"""
        return Product.objects.filter(
            compatible_cars__brand=self.car_brand
        ).distinct()[:12]
    



from django.contrib import admin
from .models import Product, CarBrand, CarModel, Shop, Category, CarArticle
# Register your models here.



admin.site.register(CarModel)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(Shop)
class ShopAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'date_created']
    list_filter = ['date_created']
    search_fields = ['title', 'owner__username']
    list_per_page = 20
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'price']
    list_filter = ['price', 'date_created']
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        return super().get_queryset(request).filter(shop__owner=request.user)


@admin.register(CarArticle)
class CarArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'car_brand', 'created_at', 'is_active']
    list_filter = ['car_brand', 'created_at', 'is_active']
    search_fields = ['title', 'content', 'car_brand__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('اطلاعات اصلی', {
            'fields': ('car_brand', 'title', 'slug', 'image')
        }),
        ('محتوا', {
            'fields': ('content',)
        }),
        ('وضعیت', {
            'fields': ('is_active',)
        }),
    )

@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


















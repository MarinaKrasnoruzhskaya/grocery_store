from django.contrib import admin

from catalog.models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "slug",
        "image",
    )
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    max_num = 3
    min_num = 3


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "subcategory",
        "name",
        "slug",
        "price"
    )
    prepopulated_fields = {'slug': ('name',)}

    inlines = [ProductImageInline,]

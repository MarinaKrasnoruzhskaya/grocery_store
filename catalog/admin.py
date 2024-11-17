from django.contrib import admin

from catalog.models import Category, Subcategory, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        # "slug_name"
        "image",
    )
    prepopulated_fields = {'slug_name': ('name',)}


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        "category",
        "name",
        # "slug_name"
        "image",
    )
    prepopulated_fields = {'slug_name': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "subcategory",
        "name",
        # "slug_name"
        "image",
        "price"
    )
    prepopulated_fields = {'slug_name': ('name',)}

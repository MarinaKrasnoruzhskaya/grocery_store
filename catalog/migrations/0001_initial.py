# Generated by Django 5.1.3 on 2024-11-17 21:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите наименование категории",
                        max_length=255,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "slug_name",
                    models.SlugField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="slug-имя",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение для категории",
                        null=True,
                        upload_to="catalog/category/",
                        verbose_name="Изображение",
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Subcategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите наименование подкатегории",
                        max_length=255,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "slug_name",
                    models.SlugField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="slug-имя",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение для подкатегории",
                        null=True,
                        upload_to="catalog/subcategory/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Выберите категорию продукта",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="subcategories",
                        to="catalog.category",
                        verbose_name="Категория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Подкатегория",
                "verbose_name_plural": "Подкатегории",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        help_text="Введите наименование продукта",
                        max_length=255,
                        unique=True,
                        verbose_name="Наименование",
                    ),
                ),
                (
                    "slug_name",
                    models.SlugField(
                        blank=True,
                        max_length=255,
                        null=True,
                        unique=True,
                        verbose_name="slug-имя",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите изображение для продукта в 3-х размерах",
                        null=True,
                        upload_to="catalog/product/",
                        verbose_name="Изображение",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Введите цену продукта",
                        max_digits=10,
                        verbose_name="Цена",
                    ),
                ),
                (
                    "subcategory",
                    models.ForeignKey(
                        help_text="Выберите подкатегорию продукта",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="products",
                        to="catalog.subcategory",
                        verbose_name="Подкатегория",
                    ),
                ),
            ],
            options={
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
                "ordering": ["name"],
            },
        ),
    ]

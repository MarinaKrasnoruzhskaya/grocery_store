from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """ Класс для модели Категория продукта """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите наименование категории"
    )
    slug_name = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="slug-имя")
    image = models.ImageField(
        upload_to='catalog/category/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для категории"
    )

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['name',]


class Subcategory(models.Model):
    """ Класс для модели Подкатегория продукта """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="subcategories",
        help_text="Выберите категорию продукта"
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите наименование подкатегории"
    )
    slug_name = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="slug-имя")
    image = models.ImageField(
        upload_to='catalog/subcategory/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для подкатегории"
    )

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ['name',]


class Product(models.Model):
    """ Класс для модели Продукт """

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        verbose_name="Подкатегория",
        related_name="products",
        help_text="Выберите подкатегорию продукта"
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите наименование продукта"
    )
    slug_name = models.SlugField(max_length=255, unique=True, blank=True, null=True, verbose_name="slug-имя")
    image = models.ImageField(
        upload_to='catalog/product/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для продукта в 3-х размерах"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену продукта"
    )

    def save(self, *args, **kwargs):
        if not self.slug_name:
            self.slug_name = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name',]

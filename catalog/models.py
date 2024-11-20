from django.db import models
from pytils.translit import slugify


class Category(models.Model):
    """ Класс для модели Категория продукта """

    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите наименование категории"
    )
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
    image = models.ImageField(
        upload_to='catalog/category/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для категории"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
    image = models.ImageField(
        upload_to='catalog/subcategory/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для подкатегории"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Цена",
        help_text="Введите цену продукта"
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['name',]


class ProductImage(models.Model):
    """ Класс для модели Изображение продукта """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
        related_name="product_images",
    )
    image = models.ImageField(
        upload_to='catalog/product_image/',
        verbose_name="Изображение",
        help_text="Загрузите изображение для продукта"
    )

    def __str__(self):
        return self.product.name

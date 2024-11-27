from django.db import models
from pytils.translit import slugify


class Category(models.Model):
    """ Класс для модели Категория/Подкатегория продукта """

    category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="subcategories",
        help_text="Выберите родительскую категорию продукта",
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=255,
        unique=True,
        verbose_name="Наименование",
        help_text="Введите наименование категории/подкатегории"
    )
    slug = models.SlugField(unique=True, blank=True, null=True, max_length=255)
    image = models.ImageField(
        upload_to='catalog/category/',
        blank=True,
        null=True,
        verbose_name="Изображение",
        help_text="Загрузите изображение для категории/подкатегории"
    )

    def __str__(self):
        if self.category:
            return f"{self.category}/{self.name}"
        return self.name

    def save(self, *args, **kwargs):
        if not self.id and not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Категория|Подкатегория"
        verbose_name_plural = "Категории/Подкатегории"
        ordering = ['name',]


class Product(models.Model):
    """ Класс для модели Продукт """

    subcategory = models.ForeignKey(
        Category,
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

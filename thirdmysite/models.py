from django.db import models
from django.urls import reverse


class Product(models.Model):
    name = models.CharField(max_length=150)
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    aprice = models.PositiveIntegerField(default=0)
    photo = models.ImageField(upload_to='products/')
    photo2 = models.ImageField(upload_to='products/')
    photo3 = models.ImageField(upload_to='products/')
    size = models.CharField(max_length=3)
    colours = models.CharField(max_length=150)
    short_description = models.TextField()
    description = models.TextField()
    information = models.TextField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={
            'slug': self.slug,
        })

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Category(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    photo = models.ImageField(null=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class RatingStar(models.Model):
    value = models.SmallIntegerField('Значение', default=0)

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ['-value']


class Rating(models.Model):
    ip = models.CharField('IP-адрес', max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Фильм')

    def __str__(self):
        return f'{self.star} - {self.movie}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class ContactWithUs(models.Model):
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    subject = models.CharField('Тема', max_length=250)
    email = models.EmailField()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Reviews(models.Model):
    email = models.EmailField()
    name = models.CharField('Имя', max_length=100)
    text = models.TextField('Сообщение', max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    product = models.ForeignKey(Product,verbose_name='продукт', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} - {self.product}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

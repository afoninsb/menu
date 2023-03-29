from django.core.exceptions import ValidationError
from django.core.validators import validate_unicode_slug
from django.db import models


class Menu(models.Model):
    title = models.CharField(
        verbose_name='Название меню',
        max_length=255,
        unique=True
    )
    slug = models.SlugField(
        verbose_name="Слаг меню",
        max_length=255,
        unique=True,
        validators=[validate_unicode_slug]
    )

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.title


class Item(models.Model):
    title = models.CharField(verbose_name='Название пункта', max_length=255)
    slug = models.SlugField(
        verbose_name="Слаг пункта",
        max_length=255,
        unique=True,
        validators=[validate_unicode_slug]
    )
    parent = models.ForeignKey(
        'self',
        verbose_name="Родительский пункт",
        blank=True,
        null=True,
        related_name='children',
        on_delete=models.CASCADE,
    )
    menu = models.ForeignKey(
        Menu,
        verbose_name="Меню",
        related_name='items',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.title

    def clean(self):
        if self.parent and self.parent.id == self.id:
            raise ValidationError(
                'Нельзя назначить пункт сам себе родительским'
            )

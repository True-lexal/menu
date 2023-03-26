from django.db import models
from django.urls import reverse
from .utils import MyUrlField


class Menu(models.Model):
    """
    Main menu block name
    """
    name = models.CharField(verbose_name='Название меню', max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class MenuElements(models.Model):
    """
    Elements of menus table
    """
    title = models.CharField(verbose_name='Заголовок пункта меню', max_length=150)
    main_menu = models.ForeignKey(Menu, models.PROTECT, verbose_name='Меню')
    parent = models.ForeignKey('MenuElements',
                               models.CASCADE,
                               verbose_name='Родительский пункт меню',
                               blank=True,
                               null=True,
                               help_text='Оставить пустым, если корневой',)
    url = MyUrlField(verbose_name='link or url name', max_length=200, unique=True,
                     help_text='Заменить на полную внешнюю ссылку при необходимости ( https://... или http://... )')

    def save(self, *args, **kwargs):
        """
        Check parents before saving.
        Cansel save if:
                parent is itself,
                same object in parent tree,
                parent belong to another menu.
        """
        if self.parent:
            if self.parent.pk == self.pk:
                # Cannot be inherited from itself
                return
            if self.main_menu != self.parent.main_menu:
                # main menu must be the same
                return
            parent = self.parent
            while parent:
                parent = parent.parent
                if parent and parent.pk == self.pk:
                    # An object cannot inherit from a tree that already has this object
                    return
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Return inner url or outer
        """
        if any(map(lambda el: el in self.url, ':/.')):
            if self.url.startswith('http'):
                return self.url
            return '#'
        return reverse('menu', kwargs={'slug': self.url})

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

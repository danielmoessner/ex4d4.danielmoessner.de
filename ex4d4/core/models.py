from django.db import models


class Seo(models.Model):
    url = models.CharField(max_length=200, unique=True, blank=True, verbose_name='Url',
                           help_text='Activates on this url. If empty usually active.')
    title_tag = models.CharField(max_length=200, verbose_name='Title')
    meta_description = models.TextField(verbose_name='Description')

    objects = models.Manager()

    def __str__(self):
        if self.url:
            return '/{}: {}'.format(self.url, self.title_tag)
        return self.title_tag

    class Meta:
        verbose_name = 'Seo Setting'
        verbose_name_plural = 'Seo Settings'


class Code(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    url = models.CharField(max_length=200, blank=True, verbose_name='Url')
    LOCATIONS = [('HEAD', 'Head'), ('BODY', 'Body')]
    location = models.CharField(choices=LOCATIONS, max_length=200, verbose_name='Location',
                                help_text='Where is the code supposed to be?')
    code = models.TextField(verbose_name='Code', help_text='The code is not validated and should be correct.')

    objects = models.Manager()

    def __str__(self):
        if self.url:
            return '/{}: {}'.format(self.url, self.name)
        return self.name

    class Meta:
        verbose_name = 'Code'
        verbose_name_plural = 'Code'


class Page(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    slug = models.SlugField(unique=True, verbose_name='Slug',
                            help_text='How the page shows up in the url.')
    shown_in_footer_other = models.BooleanField(verbose_name='Shown in the footer section other',
                                                help_text='Should a link to the page in the footer be displayed?')
    shown_in_footer_legal = models.BooleanField(verbose_name='Shown in the footer section legal',
                                                help_text='Should a link to the page in the footer be displayed?')
    shown_in_navigation = models.BooleanField(verbose_name='Shown in the navigation',
                                              help_text='Should a link to the page in the navigation be displayed?')
    html_activated = models.BooleanField(verbose_name='Html Code Activated',
                                         help_text='Should the content be rendered as html?')
    content = models.TextField(verbose_name='Content')

    objects = models.Manager()

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

    def __str__(self):
        return str(self.name)

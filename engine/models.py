# -*- coding:utf-8 -*-
from django.db import models
from siteavers.settings import STATIC_ROOT, TEMPLATE_DIRS

#################  METAS ###############################
class Language(models.Model):
    class Meta:
        verbose_name = 'мова'
        verbose_name_plural = 'мови'
    def __unicode__(self):
        return self.mnemo
        
    mnemo = models.CharField('мнемо', max_length = 5)
    nazva = models.CharField('назва', max_length = 50)
    deflang = models.BooleanField('мова за умовчанням', default = False)
    in_use = models.BooleanField('використовується', default = True)
########################################################




#=======================================================
# HEAD
#=======================================================
###################  TITLE  ############################

class SiteTitle(models.Model):
    class Meta:
        verbose_name='тайтл сайту'
        verbose_name_plural='тайтли сайту'
    def __unicode__(self):
        return self.content
    content = models.CharField('title', max_length = 200, blank = True, null = True)
    lang = models.ForeignKey(Language, verbose_name = 'мова')
    in_use = models.BooleanField('використовується', default = True)
    def get_sitetitle(self,lang):
        try:
            return self.objects.get(lang__mnemo=lang,in_use=True).content
        except:
            return self.objects.get(lang__deflang=True,in_use=True).content
       
        
class ChapterTitle(models.Model):
    class Meta:
        verbose_name = 'title'
        verbose_name_plural = 'titles'
    def __unicode__(self):
        return self.content
    content = models.CharField('title', max_length = 200, blank = True, null = True)
    section = models.ForeignKey('Chapter', verbose_name = 'розділ',related_name='titles')
    lang = models.ForeignKey(Language, verbose_name = 'мова')
    in_use = models.BooleanField('використовується', default = True)
########################################################




################### METATAGS ##########################

class MetaContent(models.Model):
    class Meta:
        verbose_name = 'вміст тега meta'
        verbose_name_plural = 'вміст тега meta'
    def __unicode__(self):
        return self.content
    content = models.CharField('вміст', max_length = 250)
    lang = models.ForeignKey(Language, verbose_name = 'мова')
    in_use = models.BooleanField('використовується', default = True)
    

class MetaTag(models.Model):
    CHARSETS = (
        ('utf-8','UTF-8'),
    )
    NAMES = (
        ('application-name','application-name'),
        ('author','author'),
        ('description','description'),
        ('generator','generator'),
        ('keywords','keywords'),)
    HTTP_EQUIV=(
        ('content-type','content-type'),
        ('default-style','default-style'),
        ('refresh','refresh'),)
    class Meta:
        verbose_name = 'метатег'
        verbose_name_plural = 'метатеги'
    def __unicode__(self):
        if self.charset is not None:
            return self.charset
        else:
            if name is not None:
                return self.name
            else:
                return self. http_equiv
    charset = models.CharField('атрибут charset', max_length = 20, choices = CHARSETS, blank = True, null = True)
    name = models.CharField('атрибут name', max_length = 20, choices = NAMES, blank = True, null = True)
    http_equiv = models.CharField('атрибут http-equiv',max_length = 20, choices = HTTP_EQUIV, blank = True, null = True)
    content = models.ManyToManyField(MetaContent,verbose_name='вміст тега',related_name='content_by_language',blank = True, null = True)

#######################################################




#################### CSS FILES LOADER  ################
class CSSFile(models.Model):
    class Meta:
        verbose_name = 'css - файл'
        verbose_name_plural = 'css - файли'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва', max_length = 150)
    file = models.FilePathField('файл',path='{0}{1}/'.format(STATIC_ROOT, 'css'), match='.*\.css$', recursive = True)
    rank = models.IntegerField('місце у списку', default = 0)
    media = models.CharField('атрибут media',max_length=30, blank = True, null = True)
    in_use = models.BooleanField('використовується', default = True)
########################################################




#################### JS FILES LOADER  ##################
class JSSFile(models.Model):
    class Meta:
        verbose_name = 'js - файл'
        verbose_name_plural = 'js - файли'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва', max_length = 150)
    file = models.FilePathField('файл',path='{0}{1}/'.format(STATIC_ROOT, 'jss'), match='.*\.js$', recursive = True)
    rank = models.IntegerField('місце у списку')
    head_section = models.BooleanField('розмістити у секції head', default = True)
    in_use = models.BooleanField('використовується', default = True)
########################################################


################  SECTION  #########################
class ChapterType(models.Model):
    class Meta:
        verbose_name = 'тип розділу'
        verbose_name_plural = 'типи розділів'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва типу',max_length=150)
    mnemo = models.CharField('мнемо',max_length=50)
    template = models.FilePathField('шаблон',path=TEMPLATE_DIRS[0], match='.*\.html$',recursive = True)
    layout = models.FilePathField('layout',path = '{0}/{1}'.format(TEMPLATE_DIRS[0],'layouts'), match='.*\.html$')
    in_use = models.BooleanField('використовується',default = True)
    
####################################################
class Chapter(models.Model):
    class Meta:
        verbose_name = 'розділ сайту'
        verbose_name_plural = 'розділи сайту'
    def __unicode__(self):
        try:
            lang = Language.objects.get(deflang = True).mnemo
            return self.titles.get(lang__mnemo = lang).content
        except:
            return self.mnemo
    mnemo = models.CharField('mnemo',max_length = 200)
    chapparent = models.ForeignKey('self',related_name='parent_chapter',verbose_name = 'розділ-предок',blank=True,null=True)
    chaptype = models.ForeignKey(ChapterType,verbose_name = 'тип розділу')
    created = models.DateTimeField('створений',auto_now_add=True, auto_now = False)
    updated = models.DateTimeField('оновлений',auto_now = True, auto_now_add = False,blank=True,null=True)
    use_redir = models.BooleanField('використовувати редирект',default = False)
    redir = models.ForeignKey('self', verbose_name='редирект', blank = True, null = True)
    in_use = models.BooleanField('використовується', default = False)
#########################################################

#########################################################
class ChapterContent(models.Model):
    class Meta:
        verbose_name = 'текстова частина'
        verbose_name_plural = 'текстові частини'
    def __unicode__(self):
        return self.chapter.mnemo
    lang = models.ForeignKey(Language, verbose_name = 'мова')
    chapter = models.ForeignKey(Chapter, verbose_name = 'розділ',related_name='contents')
    tekst = models.TextField('текст', blank = True, null = True)
    created = models.DateTimeField('створений', auto_now = False, auto_now_add = True)
    updated = models.DateTimeField('оновлений',auto_now = True, auto_now_add = False,blank=True,null=True)
    in_use = models.BooleanField('використовується', default = False)
#########################################################

####################### MENU AND NAVIGATION #############
class Menu(models.Model):
    class Meta:
        verbose_name='меню'
        verbose_name_plural='меню'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва', max_length=150)
    mnemo = models.CharField('mnemo', max_length=100)
    parent_chaptypes = models.ManyToManyField(ChapterType,related_name='menues')
    in_use = models.BooleanField('використовується', default = False)
    def get_menuitems(self):
        for elem in self.punkts.all:
            return elem
##########################################################

##########################################################
class MenuItem(models.Model):
    class Meta:
        verbose_name='пункт меню'
        verbose_name_plural='пункти меню'
    def __unicode__(self):
        lang = Language.objects.get(deflang = True).mnemo
        if not self.use_chapter:
            if not self.names:
                return self.mnemo
            else:
                return self.names.get(lang__mnemo=lang).nazva
        else:
            return self.chapter.titles.get(section = self.chapter.id,lang__mnemo = lang).content
         
    mnemo = models.CharField('mnemo', max_length=100, blank=True,null=True)
    menu = models.ForeignKey(Menu,related_name='punkts')
    rank = models.IntegerField('№ у списку',blank=True,null=True)
    use_chapter = models.BooleanField('використовувати розділ', default=False)
    chapter = models.ForeignKey(Chapter,verbose_name='розділ', blank=True,null=True)
    in_use = models.BooleanField('використовується', default = False)

class MenuItemName(models.Model):
    class Meta:
        verbose_name='назва пункту меню'
        verbose_name_plural='назви пунктів меню'
    def __unicode__(self):
        return self.nazva        
    nazva = models.CharField('назва', max_length=150)
    menuitem = models.ForeignKey(MenuItem,related_name='names')
    lang = models.ForeignKey(Language, verbose_name = 'мова')
    in_use = models.BooleanField('використовується', default = True)    
##########################################################
    
    




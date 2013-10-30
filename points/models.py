# -*- coding:utf-8 -*-
from django.db import models
import datetime
from engine.models import Language
################### COUNTRIES  #####################

class Country(models.Model):
    class Meta:
        verbose_name='країна'
        verbose_name_plural='країни'
    def __unicode__(self):
        if self.nazva_inner:
            return self.nazva_inner
        else:
            return self.mnemo
    nazva_inner = models.CharField('назва у адмін. частині',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    in_use = models.BooleanField('використовується',default = True)

class CountryName(models.Model):
    class Meta:
        verbose_name='назва країни'
        verbose_name_plural='назви країн'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    country = models.ForeignKey(Country,related_name='names',verbose_name='країна')
    in_use = models.BooleanField('використовується',default = True)

####################################################


################### CITIES #########################

class City(models.Model):
    class Meta:
        verbose_name='місто'
        verbose_name_plural='міста'
    def __unicode__(self):
        if self.nazva_inner:
            return '{0} ({1})'.decode('UTF-8').format(self.nazva_inner,self.country.nazva_inner)
        else:
            return self.mnemo
    nazva_inner = models.CharField('назва у адмін. частині',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    country = models.ForeignKey(Country,related_name='cities',verbose_name='країна')
    in_use = models.BooleanField('використовується',default = True)

class CityName(models.Model):
    class Meta:
        verbose_name='назва міста'
        verbose_name_plural='назви міст'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    city = models.ForeignKey(City,related_name='names',verbose_name='місто')
    in_use = models.BooleanField('використовується',default = True)
    
####################################################


################# TRANSFER SYSTEMS #################
class TransferSystem(models.Model):
    class Meta:
        verbose_name='система переказів'
        verbose_name_plural='системи переказів'
    def __unicode__(self):
        if self.nazva_inner:
            return self.nazva_inner
        else:
            return self.mnemo
    nazva_inner = models.CharField('назва у адмін. частині',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    in_use = models.BooleanField('використовується',default = True)

class TransferSystemName(models.Model):
    class Meta:
        verbose_name='назва системи переказів'
        verbose_name_plural='назви систем переказів'
    def __unicode__(self):
        return self.nazva
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    tsystem = models.ForeignKey(TransferSystem,related_name='names',verbose_name='система переказів')
    in_use = models.BooleanField('використовується',default = True)
####################################################


################# TARIFFS AND CURRENCY ##########################
class Currency(models.Model):
    class Meta:
        verbose_name='валюта'
        verbose_name_plural='валюти'
    def __unicode__(self):
        return '{0} ({1})'.decode('UTF-8').format(self.nazva, self.mnemo)
    nazva = models.CharField('назва',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    in_use = models.BooleanField('використовується',default = True)
        
class Tariff(models.Model):
    class Meta:
        verbose_name='тариф'
        verbose_name_plural='тарифи'
    def __unicode__(self):
        if self.in_persents and not self.in_currency:
            return '{0} ({1})'.decode('UTF-8').format(str(self.in_persents),self.currency)
        elif self.in_currency and not self.in_persents:
            return '{0} ({1})'.decode('UTF-8').format(str(self.in_currency),self.currency)
        else:
            return 'Tariff № '+str(self.id)
    in_persents = models.DecimalField('у відсотках', max_digits=5, decimal_places=2, blank=True, null=True)
    in_currency = models.DecimalField('ставка (грошове вираження)', max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.ForeignKey(Currency,related_name='tariffs', verbose_name='валюта')
    from_sum = models.DecimalField('від', max_digits=10, decimal_places=2, blank=True, null=True)
    to_sum = models.DecimalField('до', max_digits=10, decimal_places=2, blank=True, null=True)
    in_use = models.BooleanField('використовується',default = True)
####################################################


################# DIRECTIONS #######################
class Direction(models.Model):
    class Meta:
        verbose_name='напрямок'
        verbose_name_plural='напрямки'
    def __unicode__(self):
        return self.nazva_inner
    nazva_inner = models.CharField('назва',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    country_from = models.ForeignKey(Country, related_name='from_countries', verbose_name='з країни')
    country_to = models.ForeignKey(Country, related_name='to_countries', verbose_name='в країну')
    in_use = models.BooleanField('використовується',default = True)
####################################################

################# TRANSFER MODE ####################
class TransferMode(models.Model):
    class Meta:
        verbose_name='модель переказу'
        verbose_name_plural='моделі переказів'
    def __unicode__(self):
        return self.nazva_inner
    nazva_inner = models.CharField('назва',max_length=150)
    mnemo = models.CharField('мнемо',max_length=150)
    direction = models.ForeignKey(Direction,related_name='transfer_modes')
    tsystem = models.ForeignKey(TransferSystem,related_name='transfer_modes')
    tariff = models.ManyToManyField(Tariff,related_name='transfer_modes')
    in_use = models.BooleanField('використовується',default = True)
####################################################

#################### POINT #########################
class Point(models.Model):
    class Meta:
        verbose_name='точка переказу'
        verbose_name_plural='точки переказів'
    def __unicode__(self):
        if self.nazva_inner:
            return self.nazva_inner
        else:
            return self.code
    nazva_inner = models.CharField('назва',max_length=150)
    code = models.CharField('код', max_length=30, help_text='ідентифікатор точки')
    city = models.ForeignKey(City,related_name='points',verbose_name='місто', blank = True, null = True)
    tsystems = models.ManyToManyField(TransferSystem,related_name='points',verbose_name='системи переказів', blank = True, null = True)
    currencies = models.ManyToManyField(Currency, related_name='points',verbose_name='валюти переказу',blank = True, null = True)
    teln = models.CharField('тел.', max_length=150,blank = True, null = True)
    geo_latitude = models.DecimalField('геогр. широта', max_digits=8, decimal_places=6, blank = True, null = True)
    geo_longitude = models.DecimalField('геогр. довгота', max_digits=8, decimal_places=6, blank = True, null = True)
    fc_point = models.BooleanField('точка FC', default = False)
    created = models.DateTimeField('завантажена у базу', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('оновлена', auto_now=True, auto_now_add=True)
    in_use = models.BooleanField('використовується',default = True)
    def has_providernames(self):
        return self.provider_names.filter(point = self.id).count()
    def has_addressnames(self):
        return self.address_names.filter(point = self.id).count()
    def has_worktimenames(self):
        return self.worktime_names.filter(point = self.id).count()
    def has_tsystems(self):
        if self.tsystems.filter(points__id__in=[self.id,]):
            return True
        else:
            return False
    has_providernames.short_description = 'Чи є назви точок розміщення?'
    has_addressnames.short_description = 'Чи є адреси?'
    has_worktimenames.short_description = 'Чи вказаний час роботи?'
    has_tsystems.short_description='Є прив"язка до системи'

class ProviderName(models.Model):
    class Meta:
        verbose_name='постачальник послуги'
        verbose_name_plural='постачальники послуги'
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    point = models.ForeignKey(Point,related_name='provider_names', verbose_name='постачальник послуги')

class AddressName(models.Model):
    class Meta:
        verbose_name='адреса'
        verbose_name_plural='адреси'
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    point = models.ForeignKey(Point,related_name='address_names', verbose_name='адреса')

class WorkTime(models.Model):
    class Meta:
        verbose_name='робочі години точки'
        verbose_name_plural='робочі години точок'
    nazva = models.CharField('назва',max_length=150)
    lang = models.ForeignKey('engine.Language',verbose_name='мова')
    point = models.ForeignKey(Point,related_name='worktime_names', verbose_name='робочі години')
    
####################################################

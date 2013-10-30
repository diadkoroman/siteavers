# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Country, CountryName, City, CityName, TransferSystem, TransferSystemName, Currency, Tariff, Direction, TransferMode, Point, ProviderName, AddressName, WorkTime

################################################
class CountryNameInline(admin.TabularInline):
    model=CountryName
    extra = 0
class CountryAdmin(admin.ModelAdmin):
    inlines = [CountryNameInline,]

admin.site.register(Country,CountryAdmin)
################################################



################################################
class CityNameInline(admin.TabularInline):
    model = CityName
    extra = 0

class CityAdmin(admin.ModelAdmin):
    inlines = (CityNameInline,)
    list_filter=('country','in_use')
    list_display=('__unicode__','id',)
    ordering=('country','nazva_inner')
admin.site.register(City, CityAdmin)
################################################



################################################
class TransferSystemNameInline(admin.TabularInline):
    model = TransferSystemName
    extra = 0

class TransferSystemAdmin(admin.ModelAdmin):
    inlines = (TransferSystemNameInline,)
    list_display=('nazva_inner','in_use')
admin.site.register(TransferSystem,TransferSystemAdmin)
################################################


################################################
class CurrencyAdmin(admin.ModelAdmin):
    list_display=('nazva','mnemo','in_use')
admin.site.register(Currency,CurrencyAdmin)
################################################


################################################
class TariffAdmin(admin.ModelAdmin):
    list_display=('__unicode__','currency','in_use')
    list_filter=('currency',)
admin.site.register(Tariff, TariffAdmin)
################################################



################################################
class DirectionAdmin(admin.ModelAdmin):
    list_display=('__unicode__','in_use')
    list_filter=('country_from','country_to','in_use')
admin.site.register(Direction, DirectionAdmin)
################################################



################################################
class TransferModeAdmin(admin.ModelAdmin):
    list_display=('nazva_inner','direction','tsystem','in_use')
    list_filter=('direction','tsystem','tariff','in_use')
admin.site.register(TransferMode, TransferModeAdmin)
################################################


###############  POINT  ########################
class ProviderNameInline(admin.TabularInline):
    model=ProviderName
    extra = 0
    
class AddressNameInline(admin.TabularInline):
    model = AddressName
    extra = 0
    
class WorkTimeInline(admin.TabularInline):
    model = WorkTime
    extra = 0
    
class PointAdmin(admin.ModelAdmin):
    search_fields=('code','nazva_inner')
    list_display=('code','__unicode__','city','in_use','has_tsystems','has_providernames','has_addressnames','has_worktimenames')
    inlines = (ProviderNameInline,AddressNameInline,WorkTimeInline)
admin.site.register(Point,PointAdmin)
################################################

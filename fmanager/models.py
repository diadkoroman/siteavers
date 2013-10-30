# -*- coding:utf-8 -*-
import re
from django.db import models
from django.db.models import Q
from siteavers.settings import MEDIA_ROOT
from engine.models import Language
from points.models import Point, Country, CountryName,  City, CityName,ProviderName,AddressName, WorkTime
#################################################
class Loader(models.Model):
    class Meta:
        verbose_name='файл з точками (завантажити нові)'
        verbose_name_plural='файли з точками (завантажити нові)'
    def __unicode__(self):
        return '{0} - {1}'.decode('UTF-8').format(str(self.id),self.upl_date)
    upl_file = models.FileField('завантажити файл', upload_to='files/points/loader')
    tsystem = models.ForeignKey('points.TransferSystem',verbose_name='прив"язати до системи', blank=True, null = True)
    upl_date = models.DateTimeField('останнє завантаження',auto_now=True,auto_now_add=True)
    upl_iter = models.IntegerField('розміщено точок',default = 0)
    ############################
    def parsefile(self,filename,stack):
        with open(filename) as f:
            for line in f:
                line_splitted = re.split(r'\s{2,}', line, flags=re.U+re.I)
                if line_splitted[0] != '' and re.match(r'^[0-9]{2}',line, flags=re.U+re.I):
                    try:
                        line_splitted = [item.decode('UTF-8') for item in line_splitted]
                        stack.append(line_splitted)
                    except:
                        continue
            f.close()

    def prepare_lines(self,stack,prepared):
        for line in stack:
        #
            split_line0=re.split(r'\s',line[0],flags=re.U+re.I)
            split_line4 = re.split(r'\s',line[4],flags=re.U+re.I)
            split_line5=line[5].split(';')
            try:
                lined = dict(
                    code=split_line0[1],
                    city=line[1],
                    provider=line[2],
                    address=line[3],
                    country_mnemo=split_line4[0],
                    works=split_line5[0],
                    currencies=split_line5[1].strip(),
                    telns=split_line5[2].strip()
                )
                prepared.append(lined)
            except:
                continue
    ############################
    def save(self,*args,**kwargs):
        self.upl_iter = 0
        stack=[]
        prepared=[]
        deflang = Language.objects.get(deflang = True)
        super(Loader,self).save(*args,**kwargs)
        path = self.upl_file.path
        self.parsefile(path,stack)
        self.prepare_lines(stack,prepared)
        for line in prepared:
            ############################################
            country_count = Country.objects.filter(mnemo=line['country_mnemo']).count()
            if country_count == 0:
                cntr = Country(
                    nazva_inner=line['country_mnemo'],
                    mnemo = line['country_mnemo'],
                )
                cntr.save()
                cntrN = CountryName(
                    nazva=line['country_mnemo'],
                    lang=deflang,
                    country=cntr
                    
                )
                cntrN.save()
            else:
                cntr = Country.objects.get(mnemo=line['country_mnemo'])
            ############################################
            ############################################
            city_count=City.objects.filter(nazva_inner=line['city']).count()
            if city_count == 0:
                city = City(
                    nazva_inner=line['city'],
                    mnemo = line['city'],
                    country = cntr
                )
                city.save()
                cityN = CityName(
                    nazva=line['city'],
                    lang=deflang,
                    city=city
                )
                cityN.save()
            else:
                city = City.objects.get(nazva_inner=line['city'])
            ############################################
            pnt_count = Point.objects.filter(Q(code=line['code'])|Q(nazva_inner=line['provider'])).count()
            if pnt_count == 0:
                pnt = Point(
                    nazva_inner=line['provider'],
                    code=line['code'],
                    teln=line['telns'],
                    city = city,
                    in_use=False
                )
                pnt.save()
                if self.tsystem:
                    pnt.tsystems.add(self.tsystem)
                    pnt.save()
                prv = ProviderName(
                    nazva = line['provider'],
                    lang = deflang,
                    point = pnt
                )
                prv.save()
                adr = AddressName(
                    nazva = line['address'],
                    lang = deflang,
                    point = pnt
                )
                adr.save()
                wkt = WorkTime(
                    nazva = line['works'],
                    lang = deflang,
                    point=pnt
                )
                wkt.save()
                self.upl_iter = self.upl_iter + 1
            else:
                continue
        super(Loader,self).save(*args,**kwargs)
#################################################


class Updater(models.Model):
    class Meta:
        verbose_name='файл з точками (CRUD)'
        verbose_name_plural='файли з точками (CRUD)'
    upl_file = models.FileField('завантажити файл', upload_to='files/points/updater')
    upl_date = models.DateTimeField('останнє завантаження',auto_now=True,auto_now_add=True)
    upl_iter = models.IntegerField('оновлено точок',default = 0)
    ins_iter = models.IntegerField('розміщено нових точок',default = 0)
    del_iter = models.IntegerField('видалено точок',default = 0)
    #############################################
    def parsefile(self,stack,allowed_linestarts):
        with open(self.upl_file.path) as f:
            for line in f:
                line_splitted = re.split(r'\s{2,}|:\s+',line,flags=re.I+re.U)
                if line_splitted[0]!='' and line_splitted[0].startswith(allowed_linestarts):
                    stack.append(line_splitted)
        f.close()
    #############################################


    #############################################
    def groupres(self,stack,allowed_linestarts,groups):
        for elem in stack:
            if elem[0] == allowed_linestarts[0]:
                groups['i'].append(elem)
                del elem
            elif elem[0] == allowed_linestarts[1]:
                groups['d'].append(elem)
                del elem
            elif elem[0] == allowed_linestarts[2]:
                groups['u'].append(elem)
                del elem
    #############################################


    #############################################
    def prepare_lines(self,stack,allowed_linestarts):
        prepared=[]
        for line in stack:
            # insert & update
            if line[0] == allowed_linestarts[0] or line[0] == allowed_linestarts[2]:
                split_line5=re.split(r'\s',line[5],flags=re.U+re.I)
                split_line7=line[7].split(';')
                try:
                    lined = dict(
                        code=line[1].strip(),
                        city=line[2].strip(),
                        provider=line[3].strip(),
                        address=line[4].strip(),
                        country_mnemo=split_line5[0].strip(),
                        works=line[6].strip() + ' '+split_line7[0].strip(),
                        currencies=split_line7[1].strip(),
                        telns=split_line7[2].strip()
                    )
                except:
                    continue
            # delete
            elif line[0] == allowed_linestarts[1]:
                try:
                    lined = dict(
                        code=line[1].strip(),
                        city='',
                        provider='',
                        address='',
                        country_mnemo='',
                        works='',
                        currencies='',
                        telns=''
                    )
                except:
                    continue
            prepared.append(lined)
        return prepared
    #############################################



    #############################################
    def do_update(self,deflang):
        self.upl_iter = 0
        #deflang = Language.objects.get(deflang = True)
        for line in self.for_update:
            try:
                ############## GET COUNTRY ###############
                country_count = Country.objects.filter(mnemo=line['country_mnemo']).count()
                if country_count == 0:
                    cntr = Country(
                        nazva_inner=line['country_mnemo'],
                        mnemo = line['country_mnemo'],
                    )
                    cntr.save()
                    cntrN = CountryName(
                        nazva=line['country_mnemo'],
                        lang=deflang,
                        country=cntr
                    
                    )
                    cntrN.save()
                else:
                    cntr = Country.objects.get(mnemo=line['country_mnemo'])
                ############################################
                
                ###########    GET CITY   #############
                city_count=City.objects.filter(nazva_inner=line['city']).count()
                if city_count == 0:
                    city = City(
                        nazva_inner=line['city'],
                        mnemo = line['city'],
                        country = cntr
                    )
                    city.save()
                    cityN = CityName(
                        nazva=line['city'],
                        lang=deflang,
                        city=city
                    )
                    cityN.save()
                else:
                    city = City.objects.get(nazva_inner=line['city'])
                ###########################################
                pntU_count = Point.objects.filter(code = line['code']).count()
                if pntU_count > 0:
                    # здійснюємо оновлення безпосередньо даних точки
                    pntU = Point.objects.get(code = line['code'])
                    pntU.teln = line['telns']
                    pntU.city = city
                    pntU.nazva_inner = line['provider']
                    #pntU.in_use = False
                    pntU.save()
                    self.upl_iter = self.upl_iter + 1
                    if not pntU.provider_names.filter(lang__id = deflang.id,point__id = pntU.id):
                        prv = ProviderName(
                            nazva = line['provider'],
                            lang = deflang,
                            point = pnt
                        )
                        prv.save()
                    else:
                        pntU.provider_names.filter(lang__id = deflang.id,point__id = pntU.id).update(nazva = line['provider'])
                        pntU.provider_names.filter(point__id = pntU.id).exclude(lang__id = deflang.id).delete()
                        
                    if not pntU.address_names.filter(lang__id = deflang.id,point__id = pntU.id):
                        adr = AddressName(
                            nazva = line['address'],
                            lang = deflang,
                            point = pnt
                        )
                        adr.save()
                    else:
                        pntU.address_names.filter(lang__id = deflang.id,point__id = pntU.id).update(nazva = line['address'])
                        pntU.address_names.filter(point__id = pntU.id).exclude(lang__id = deflang.id).delete()

                    if not pntU.worktime_names.filter(lang__id = deflang.id,point__id = pntU.id):
                        wkt = WorkTime(
                            nazva=line['works'],
                            lang=deflang,
                            point=pnt
                        )
                        wkt.save()
                    else:
                        pntU.worktime_names.filter(lang__id = deflang.id,point__id = pntU.id).update(nazva = line['works'])
                        pntU.worktime_names.filter(point__id = pntU.id).exclude(lang__id = deflang.id).delete()
                    
            except:
                continue
        
        
    #############################################


    #############################################
    def do_insert(self,deflang):
        self.ins_iter = 0
        #deflang = Language.objects.get(deflang = True)
        for line in self.for_insert:
            try:
                ############################################
                country_count = Country.objects.filter(mnemo=line['country_mnemo']).count()
                if country_count == 0:
                    cntr = Country(
                        nazva_inner=line['country_mnemo'],
                        mnemo = line['country_mnemo'],
                    )
                    cntr.save()
                    cntrN = CountryName(
                        nazva=line['country_mnemo'],
                        lang=deflang,
                        country=cntr
                        
                    )
                    cntrN.save()
                else:
                    cntr = Country.objects.get(mnemo=line['country_mnemo'])
                ############################################
                ############################################
                city_count=City.objects.filter(nazva_inner=line['city']).count()
                if city_count == 0:
                    city = City(
                        nazva_inner=line['city'],
                        mnemo = line['city'],
                        country = cntr
                    )
                    city.save()
                    cityN = CityName(
                        nazva=line['city'],
                        lang=deflang,
                        city=city
                    )
                    cityN.save()
                else:
                    city = City.objects.get(nazva_inner=line['city'])
                ############################################
                pnt_count = Point.objects.filter(Q(code=line['code'])|Q(nazva_inner=line['provider'])).count()
                if pnt_count == 0:
                    pnt = Point(
                        nazva_inner=line['provider'],
                        code=line['code'],
                        teln=line['telns'],
                        city = city,
                        in_use=False
                    )
                    pnt.save()
                    prv = ProviderName(
                        nazva = line['provider'],
                        lang = deflang,
                        point = pnt
                    )
                    prv.save()
                    adr = AddressName(
                        nazva = line['address'],
                        lang = deflang,
                        point = pnt
                    )
                    adr.save()
                    wkt = WorkTime(
                        nazva = line['works'],
                        lang = deflang,
                        point=pnt
                    )
                    wkt.save()
                    self.ins_iter = self.ins_iter + 1
            except:
                continue
    #############################################


    #############################################
    def do_delete(self):
        self.del_iter = 0
        #pntD = Point.objects.filter(code__in=self.for_delete)
        for line in self.for_delete:
            try:
                Point.objects.get(code=line['code']).delete()
                self.del_iter = self.del_iter + 1
            except:
                continue
                
            
    #############################################
    


    ############################################
    def save(self,*args,**kwargs):
        super(Updater,self).save(*args,**kwargs)
        deflang = Language.objects.get(deflang = True)
        stack=[]
        inserts=[]
        deletes=[]
        updates=[]
        groups=dict(i=inserts,d=deletes,u=updates)
        allowed_linestarts=('Добавлен','Удален','Изменен')
        
        self.parsefile(stack,allowed_linestarts)
        self.groupres(stack,allowed_linestarts,groups)
        self.for_insert = self.prepare_lines(groups['i'], allowed_linestarts)
        self.for_delete = self.prepare_lines(groups['d'], allowed_linestarts)
        self.for_update = self.prepare_lines(groups['u'], allowed_linestarts)
        self.do_update(deflang)
        self.do_insert(deflang)
        self.do_delete()
        super(Updater,self).save(*args,**kwargs)
        
    ############################################

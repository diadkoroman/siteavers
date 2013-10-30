# -*- coding: utf-8 -*-
import os
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import simplejson
from utils import header,locale,template,lswitcher
from siteavers.settings import TEMPLATE_DIRS
from engine.models import Chapter, SiteTitle
from models import Country, City, Point
from forms import ChooserForm

# перша сторінка зі списком точок
def points_home_view(request,lang=None,page=None):
    incl={}
    incl['lang'] = lang = locale.setlang(lang)
    incl['cssfiles'] = header.csslinks()
    incl['jssfiles'] = header.jsslinks(head_section = True)
    incl['jssfiles_footer'] = header.jsslinks()
    incl['title'] = None
    incl['pagetitle'] = None
    incl['content_tekst'] = None
    chapt = Chapter.objects.get(mnemo = page,in_use = True)


    
    if chapt.use_redir:
        return template.redirTemplate(reverse('points.views.points_inner_view', args=(lang,chapt.redir.mnemo)))
    else:
        chapt_template = os.path.relpath(chapt.chaptype.template,TEMPLATE_DIRS[0])
        pageuri = reverse('points.views.points_home_view',args=(lang,page))
        ########################### TITLE  #################################
        stitle = SiteTitle.objects.get(lang__mnemo=lang).content

        try:
            incl['pagetitle'] = pagetitle = chapt.titles.get(lang__mnemo =lang).content
            incl['title'] = pagetitle+' :: '+stitle
            
        except:
            incl['title'] = ''
            incl['pagetitle'] = ''

        ######################################################################
        ############################## MENUES ################################
        ######################################################################
        incl['topmenu']=[]
        topmenu =chapt.chaptype.menues.get(mnemo='toppanel_menu').punkts.filter(menu__mnemo='toppanel_menu',in_use=True).order_by('rank')
        for item in topmenu:
            try:
                if item.use_chapter:
                    item_mnemo = item.chapter.mnemo
                    item_name = item.chapter.titles.get(lang__mnemo =lang)
                else:
                    item_mnemo = item.mnemo
                    item_name = item.names.get(lang__mnemo =lang)
                menuitem = (item_mnemo,item_name)
                incl['topmenu'].append(menuitem)          
            except:
                continue
                
        ########################### LANGUAGES ###############################
        incl['lsw'] = lsw = lswitcher.langslist('/%s/' % (page,))
        #####################################################################


        ########################## CHOOSER ##################################
        incl['chooser']={}
        ctrs = Country.objects.filter(in_use = True)
        incl['chooser']['countries'] = [(item.id,item.names.get(lang__mnemo = lang)) for item in ctrs]
        #####################################################################

        ########################## LISTING ##################################
        listing =Point.objects.filter(city__id__in=[1,254],in_use=True).order_by('-fc_point')
        formap=[]
        for item in listing:
            item.countryid = item.city.country.id
            item.cityid =item.city.id
            item.provider = item.nazva_inner
            item.addr = None
            item.wrk = None
            try:
                item.provider = item.provider_names.get(lang__mnemo=lang).nazva
            except:
                pass
            try:
                item.addr = item.address_names.get(lang__mnemo=lang).nazva
            except:
                pass
            try:
                item.wrk = item.worktime_names.get(lang__mnemo=lang).nazva
            except:
                pass
            if item.geo_latitude and item.geo_longitude:
                formap.append({
                    'latitude':str(item.geo_latitude),
                    'longitude':str(item.geo_longitude),
                    'hintc':item.provider,
                    'provider':item.provider,
                    'addr':item.addr,
                    'wrk':item.wrk
                })
                
            
            
        incl['listing'] = listing
        incl['formap'] = formap
        #####################################################################

        
        #######################################################################
        return template.showTemplate(chapt_template,incl,request)





# перегляд списків точок при здійсненні вибору "звідки-куди"
def points_inner_view(request,lang=None, page=None):
    incl={}
    incl['lang'] = lang = locale.setlang(lang)
    incl['cssfiles'] = header.csslinks()
    incl['jssfiles'] = header.jsslinks(head_section = True)
    incl['jssfiles_footer'] = header.jsslinks()
    incl['title'] = None
    incl['pagetitle'] = None
    incl['content_tekst'] = None
    chapt = Chapter.objects.get(mnemo = page,in_use = True)


# відповідь на запити через ajax
def ajax_get_cities_list(request,lang=None, page=None):
    res = None
    cnt = int(request.GET['sel'])
    cities = City.objects.filter(country = cnt,in_use = True).order_by('nazva_inner')
    cities_prep = []
    for item in cities:
        d={}
        d['value'] = item.id if item.id else ''
        item_nazva = None
        try:
            item_nazva = item.names.get(lang__mnemo = lang)
        except:
            item_nazva = item.nazva_inner
        finally:
            d['nazva'] = item_nazva
        cities_prep.append(d)
    res = simplejson.dumps(cities_prep)
    return HttpResponse(res)
    



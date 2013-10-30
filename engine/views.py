# -*- coding:utf-8 -*-
import os
from django.http import Http404
from django.core.urlresolvers import reverse
from utils import header,locale,template,lswitcher
from siteavers.settings import TEMPLATE_DIRS
from models import Chapter, SiteTitle

def home_view(request,lang = None):
    page='/'
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
        return template.redirTemplate(reverse('engine.views.inner_text_view',args=(lang,chapt.redir.mnemo)))
    else:
        chapt_template = os.path.relpath(chapt.chaptype.template,TEMPLATE_DIRS[0])
        pageuri = reverse('engine.views.home_view',args=(lang,))
        ########################### TITLE  #################################
        stitle = SiteTitle.objects.get(lang__mnemo=lang).content

        try:
            incl['pagetitle'] = pagetitle = chapt.titles.get(lang__mnemo =lang).content
            incl['title'] = pagetitle+' :: '+stitle
            
        except:
            incl['title'] = ''
            incl['pagetitle'] = ''
        ####################################################################


                

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
        #lsw=[]
        #lsw.append('index')
        #lsw.append()
        incl['lsw'] = lsw = lswitcher.langslist('')
        #####################################################################
        
        #######################################################################
        return template.showTemplate(chapt_template,incl,request)








def inner_text_view(request,lang=None,page=None):
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
        return template.redirTemplate(reverse('engine.views.inner_text_view',args=(lang,chapt.redir.mnemo)))
    else:
        chapt_template = os.path.relpath(chapt.chaptype.template,TEMPLATE_DIRS[0])
        pageuri = reverse('engine.views.inner_text_view',args=(lang,chapt.mnemo))
        ########################### TITLE  #################################
        stitle = SiteTitle.objects.get(lang__mnemo=lang).content

        try:
            incl['pagetitle'] = pagetitle = chapt.titles.get(lang__mnemo =lang).content
            incl['title'] = pagetitle+' :: '+stitle
            
        except:
            incl['title'] = ''
            incl['pagetitle'] = ''
        ####################################################################


                
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
        ################################ BREADCRUMBS ##########################
        bcr=[]
        def append_to_bc(chapt,bcr):
            
            bc_url=reverse('engine.views.inner_text_view',args=(lang,chapt.mnemo)) if chapt.mnemo!='/'\
                else reverse('engine.views.home_view',args=(lang,))
            bcitem = (bc_url,chapt.titles.get(lang__mnemo = lang))
            bcr.append(bcitem)
            if chapt.chapparent:
                append_to_bc(chapt.chapparent,bcr)
                
        append_to_bc(chapt,bcr)
        bcr.reverse()
        incl['bcr']=bcr

        ########################### LANGUAGES ###############################
        #lsw=[]
        #lsw.append('inner')
        #lsw.append()
        incl['lsw'] = lsw = lswitcher.langslist(reverse('engine.views.inner_text_view',args=(chapt.mnemo,)))
        #####################################################################

            
        ###### CONTENT  ######
        try:
            incl['content_tekst'] = chapt.contents.get(lang__mnemo = lang).tekst
        except:
            raise Http404
            
        return template.showTemplate(chapt_template,incl,request)
        

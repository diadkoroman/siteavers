# -*- coding: utf-8 -*-
import os
from engine.models import CSSFile, JSSFile
from siteavers.settings import STATIC_URL,STATIC_ROOT


def csslinks():
    cssfiles = CSSFile.objects.filter(in_use = True).order_by('rank')
    for cssfile in cssfiles:
        cssfile.file = '{0}{1}'.format(STATIC_URL,os.path.relpath(cssfile.file,STATIC_ROOT))
    return cssfiles

def jsslinks(head_section = None):
    if head_section:
        jssfiles = JSSFile.objects.filter(head_section = True,in_use = True).order_by('rank')
    else:
        jssfiles = JSSFile.objects.exclude(head_section = True).filter(in_use = True).order_by('rank')

    for jssfile in jssfiles:
        jssfile.file = '{0}{1}'.format(STATIC_URL,os.path.relpath(jssfile.file,STATIC_ROOT))
    return jssfiles

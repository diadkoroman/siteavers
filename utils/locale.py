# -*- coding: utf-8 -*-
import re
from engine.models import Language

def setlang(lang, preconf = None):
    #встановлююємо мовну локаль
    if lang is None and preconf is None:
        lang=Language.objects.get(deflang = True).mnemo
    elif lang is None and not preconf is None:
        lang=Language.objects.get(mnemo = preconf).mnemo
    else:
        try:
            lang=Language.objects.get(mnemo = lang).mnemo
        except:
            lang=Language.objects.get(deflang = True).mnemo
    return lang



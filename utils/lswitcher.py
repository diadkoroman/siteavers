# -*- coding: utf-8 -*-
from engine.models import Language

def langslist(pageuri):
    elems=[]
    for lang in [item.mnemo for item in Language.objects.filter(in_use = True)]:
        elems.append([lang, pageuri])
    return elems

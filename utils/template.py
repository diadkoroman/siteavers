# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.shortcuts import render_to_response,redirect

#   відобразити шаблон
def showTemplate(filename,incl,request):
    return render_to_response(filename,incl,context_instance=RequestContext(request))

#   редирект на інший шаблон виводу
def redirTemplate(path):
    return redirect(path)

#   вибір варіанту відображення або-або
def chooseTemplate(ivar,fnames,incl,request):
    if ivar is True:
        return render_to_response(fnames['pass'],incl,context_instance=RequestContext(request))
    elif ivar is False:
        return render_to_response(fnames['fail'],incl,context_instance=RequestContext(request))
    else:
        pass





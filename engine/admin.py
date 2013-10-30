# -*- coding:utf-8 -*-
from django.contrib import admin
from models import Language, SiteTitle,ChapterTitle, MetaContent, MetaTag, CSSFile, JSSFile,ChapterType,Chapter,ChapterContent,Menu,MenuItem,MenuItemName

###################################
class C_Language(admin.ModelAdmin):
    list_display=('nazva','mnemo','deflang','in_use')
admin.site.register(Language,C_Language)
###################################

###################################
admin.site.register(SiteTitle)
###################################


###################################
class ChapterTitleInline(admin.TabularInline):
    model = ChapterTitle
    extra = 0
#admin.site.register(ChapterTitle)
###################################


###################################
admin.site.register(MetaContent)
###################################


###################################
admin.site.register(MetaTag)
###################################


###################################
class C_CSSFile(admin.ModelAdmin):
    list_display = ('nazva','file','rank','media','in_use')
admin.site.register(CSSFile, C_CSSFile)
###################################


###################################
class C_JSSFile(admin.ModelAdmin):
    list_display=('nazva','file','rank','head_section','in_use')
admin.site.register(JSSFile, C_JSSFile)
###################################

###################################
admin.site.register(ChapterType)
###################################

###################################
class ChapterContentInline(admin.TabularInline):
    model = ChapterContent
    extra = 0
#admin.site.register(ChapterContent)
###################################

###################################
class ChapterAdmin(admin.ModelAdmin):
    inlines=[ChapterTitleInline,ChapterContentInline]
admin.site.register(Chapter,ChapterAdmin)
###################################


###################################
class MenuItemNameInline(admin.TabularInline):
    model = MenuItemName
    extra = 0
#admin.site.register(MenuItemName)
###################################

###################################
class MenuItemAdmin(admin.ModelAdmin):
    inlines=[MenuItemNameInline,]
admin.site.register(MenuItem, MenuItemAdmin)

class MenuItemInline(admin.TabularInline):
    model=MenuItem
    extra = 0
###################################

###################################
class MenuAdmin(admin.ModelAdmin):
    inlines=[MenuItemInline,]
admin.site.register(Menu,MenuAdmin)
#admin.site.register(Menu)
###################################



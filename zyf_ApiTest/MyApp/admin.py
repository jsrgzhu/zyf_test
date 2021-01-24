from django.contrib import admin

# Register your models here.
from MyApp.models import *

admin.site.register(DB_tucao)#注册吐槽表
admin.site.register(DB_home_href)#注册主页链接表
admin.site.register(DB_project)#注册项目表
admin.site.register(DB_apis)#注册接口表
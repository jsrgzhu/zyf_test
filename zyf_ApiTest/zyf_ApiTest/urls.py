"""zyf_ApiTest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path

from MyApp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^welcome/$', welcome),  # 获取菜单
    path('home/', home),  # 进入首页
    re_path(r'^child/(?P<eid>.+)/(?P<oid>.*)/$', child),  # 进入子页面
    re_path(r'^login/$', login),  # 进入登录页面
    re_path(r'^login_action/$', login_action),  # 登录
    re_path(r'^register_action/$', register_action),  # 注册
    re_path(r'^accounts/login/$', login),  # 重定向登录页面
    re_path(r'^logout/$', logout),  # 退出
    re_path(r'^pei/$', pei),  # 吐槽
    re_path(r'^help/$', api_help),  # 进入帮助文档
    re_path(r'^project_list/$', project_list),  # 进入项目列表
    re_path(r'^delete_project/$', delete_project),  # 删除项目
    re_path(r'^add_project/$', add_project),  # 新增项目
    re_path(r'^apis/(?P<id>.*)/$', open_apis),  # 打开接口库
    re_path(r'^cases/(?P<id>.*)/$', open_cases),  # 打开用例库
    re_path(r'^project_set/(?P<id>.*)/$', open_project_set),  # 打开项目配置
    re_path(r'^save_project_set/(?P<id>.*)/$', save_project_set),  # 保存项目配置
    re_path(r'^project_api_add/(?P<Pid>.*)/$', project_api_add),  # 新增接口api
    re_path(r'^project_api_delete/(?P<id>.*)/$', project_api_delete),  # 删除接口api
    re_path(r'^save_bz/$', save_bz),  # 保存备注
    re_path(r'^get_bz/$', get_bz),  # 获取备注
    re_path(r'^Api_save/$', Api_save),  # 保存接口数据
    re_path(r'get_api_data/$', get_api_data),  # 获取接口数据
    re_path(r'Api_send/$', Api_send),  # send接口数据
    re_path(r'copy_api/$', copy_api),  # 复制接口
    re_path(r'error_request/$', error_request),  # 异常值测试

]

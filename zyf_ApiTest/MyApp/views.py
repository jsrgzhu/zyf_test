from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from MyApp.models import *
import json
import requests


# Create your views here.

# 欢迎页面
def welcome(request):
    return render(request, "welcome.html")


# 登录态验证后，进入主页
@login_required
def home(request):
    return render(request, 'welcome.html', {"whichHTML": "home.html", "oid": ""})


# 登录
def login(request):
    return render(request, 'login.html')


# 登录操作
def login_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']
    user = auth.authenticate(username=u_name, password=p_word)

    if user is not None:
        auth.login(request, user)
        request.session['user'] = u_name
        return HttpResponse('成功')
    else:
        return HttpResponse('失败')


# 注册
def register_action(request):
    u_name = request.GET['username']
    p_word = request.GET['password']

    try:
        user = User.objects.create_user(username=u_name, password=p_word)
        user.save()
        return HttpResponse("注册成功！")
    except:
        return HttpResponse("注册失败！用户名已存在~")


# 退出
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')


# 公用一个主页面
def child(request, eid, oid):
    res = child_json(eid, oid)
    return render(request, eid, res)


# 控制不同的页面返回不同的数据：数据分发器
def child_json(eid, oid=''):
    res = {}
    if eid == 'home.html':
        data = DB_home_href.objects.all()
        res = {"hrefs": data}

    if eid == 'project_list.html':
        data = DB_project.objects.all()
        res = {'projects': data}

    if eid == 'P_apis.html':
        project = DB_project.objects.filter(id=oid)[0]
        apis = DB_apis.objects.filter(project_id=oid)
        res = {'project': project, 'apis': apis}

    if eid == 'P_cases.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project': project}

    if eid == 'project_set.html':
        project = DB_project.objects.filter(id=oid)[0]
        res = {'project': project}
    return res


# 吐槽
def pei(request):
    t_text = request.GET['tucao_text']
    DB_tucao.objects.create(user=request.user.username, text=t_text)
    return HttpResponse('')


# 进入帮助页面
def api_help(request):
    return render(request, 'welcome.html', {'whichHTML': "help.html", "oid": ""})


# 进入项目列表
def project_list(request):
    return render(request, 'welcome.html', {'whichHTML': "project_list.html", "oid": ""})


# 删除项目
def delete_project(request):
    project_id = request.GET['id']
    DB_project.objects.filter(id=project_id).delete()
    DB_apis.objects.filter(project_id=project_id).delete()
    return HttpResponse('')


# 新增项目
def add_project(request):
    project_name = request.GET['name']
    DB_project.objects.create(name=project_name, user=request.user.username, remark='', other_user='')
    return HttpResponse('')


# 展示api
def open_apis(request, id):
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': "P_apis.html", "oid": project_id})


# 展示用例库
def open_cases(request, id):
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': "P_cases.html", "oid": project_id})


# 项目设置
def open_project_set(request, id):
    project_id = id
    return render(request, 'welcome.html', {'whichHTML': "project_set.html", "oid": project_id})


# 保存项目设置
def save_project_set(request, id):
    project_name = request.GET['name']
    project_remark = request.GET['remark']
    project_other_user = request.GET['other_user']
    project_id = id

    DB_project.objects.filter(id=project_id).update(name=project_name, remark=project_remark,
                                                    other_user=project_other_user)
    return HttpResponse('')


# 新增api接口
def project_api_add(request, Pid):
    project_id = Pid
    DB_apis.objects.create(project_id=project_id, api_method='none')
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 删除api接口
def project_api_delete(request, id):
    api_id = id
    project_id = DB_apis.objects.filter(id=api_id)[0].project_id
    DB_apis.objects.filter(id=api_id).delete()
    return HttpResponseRedirect('/apis/%s/' % project_id)


# 保存备注
def save_bz(request):
    api_id = request.GET['id']
    api_bz = request.GET['bz_text']
    # api_name = request.GET['bzapi_name']
    DB_apis.objects.filter(id=api_id).update(des=api_bz)
    return HttpResponse('')


# 获取备注
def get_bz(request):
    api_id = request.GET['id']
    res = DB_apis.objects.filter(id=api_id)[0].des
    return HttpResponse(res)


# 保存接口数据
def Api_save(request):
    api_name = request.GET['api_name']
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
    else:
        ts_api_body = request.GET['ts_api_body']

    DB_apis.objects.filter(id=api_id).update(
        name=api_name,
        api_method=ts_method,
        api_url=ts_url,
        api_host=ts_host,
        api_header=ts_header,
        body_method=ts_body_method,
        api_body=ts_api_body
    )
    return HttpResponse('success')


# 获取接口数据
def get_api_data(request):
    api_id = request.GET['api_id']
    api = DB_apis.objects.filter(id=api_id).values()[0]
    return HttpResponse(json.dumps(api), content_type='application/json')


# send接口数据
def Api_send(request):
    api_name = request.GET['api_name']
    api_id = request.GET['api_id']
    ts_method = request.GET['ts_method']
    ts_url = request.GET['ts_url']
    ts_host = request.GET['ts_host']
    ts_header = request.GET['ts_header']
    ts_body_method = request.GET['ts_body_method']

    if ts_body_method == '返回体':
        api = DB_apis.objects.filter(id=api_id)[0]
        ts_body_method = api.last_body_method
        ts_api_body = api.last_api_body
        if ts_body_method in ["", None]:
            return HttpResponse("请先选择请求体编码格式，并输入请求体，再点击Send")
    else:
        ts_api_body = request.GET['ts_api_body']
        DB_apis.objects.filter(id=api_id).update(last_body_method=ts_body_method, last_api_body=ts_api_body)
    # 发送请求获取返回值
    header = json.loads(ts_header)
    if ts_host[-1] == '/' and ts_url[0] == '/':
        url = ts_host[:-1] + ts_url
    elif ts_host[-1] != '/' and ts_url[0] != '/':
        url = ts_host + '/' + ts_url
    else:
        url = ts_host + ts_url
    if ts_body_method == 'none':
        response = requests.request(ts_method.upper(), url, headers=header, data={})
    elif ts_body_method == 'form-data':
        files = []
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = requests.request(ts_method.upper(), url, headers=header, data=payload, files=files)
    elif ts_body_method == 'x-www-form-urlencoded':
        header['Content-Type'] = 'application/x-www-form-urlencoded'
        payload = {}
        for i in eval(ts_api_body):
            payload[i[0]] = i[1]
        response = requests.request(ts_method, url, headers=header, data=payload)
    else:
        if ts_body_method == 'Text':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'JavaScript':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Json':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Html':
            header['Content-Type'] = 'text/plain'
        if ts_body_method == 'Xml':
            header['Content-Type'] = 'text/plain'
        response = requests.request(ts_method, url, headers=header, data=ts_api_body.encode('utf-8'))
    response.encoding = 'utf-8'
    return HttpResponse(response.text)


# 复制接口
def copy_api(request):
    api_id = request.GET['api_id']
    # 开始复制接口
    old_api = DB_apis.objects.filter(id=api_id)[0]

    DB_apis.objects.create(project_id=old_api.project_id,
                           name=old_api.name + '_副本',
                           api_method=old_api.api_method,
                           api_url=old_api.api_url,
                           api_header=old_api.api_header,
                           api_login=old_api.api_login,
                           api_host=old_api.api_host,
                           des=old_api.des,
                           body_method=old_api.body_method,
                           api_body=old_api.api_body,
                           result=old_api.result,
                           sign=old_api.sign,
                           file_key=old_api.file_key,
                           file_name=old_api.file_name,
                           public_header=old_api.public_header,
                           last_body_method=old_api.last_body_method,
                           last_api_body=old_api.last_api_body
                           )
    # 返回
    return HttpResponse('')


# 异常值发送请求
def error_request(request):
    api_id = request.GET['api_id']
    new_body = request.GET['new_body']
    span_text = request.GET['span_text']
    print(new_body)
    api = DB_apis.objects.filter(id=api_id)[0]
    method = api.api_method
    url = api.api_url
    host = api.api_host
    header = api.api_header
    body_method = api.body_method
    header = json.loads(header)
    if host[-1] == '/' and url[0] == '/':  # 都有/
        url = host[:-1] + url
    elif host[-1] != '/' and url[0] != '/':  # 都没有/
        url = host + '/' + url
    else:  # 肯定有一个有/
        url = host + url

    try:
        if body_method == 'form-data':
            files = []
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload, files=files)
        elif body_method == 'x-www-form-urlencoded':
            header['Content-Type'] = 'application/x-www-form-urlencoded'
            payload = {}
            for i in eval(new_body):
                payload[i[0]] = i[1]
            response = requests.request(method.upper(), url, headers=header, data=payload)
        elif body_method == 'Json':
            header['Content-Type'] = 'text/plain'
            response = requests.request(method.upper(), url, headers=header, data=new_body.encode('utf-8'))
        else:
            return HttpResponse('非法的请求体类型')
        # 把返回值传递给前端页面
        response.encoding = "utf-8"
        res_json = {"response":response.text,"span_text":span_text}
        return HttpResponse(json.dumps(res_json),content_type='application/json')
    except:
        res_json = {"response": "对不起接口未通！", "span_text": span_text}
        return HttpResponse(json.dumps(res_json),content_type='application/json')

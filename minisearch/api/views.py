# coding=utf-8
# Create your views here.

import json
import data
import auth
import os
import urllib2
import sys

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, FileResponse

# 用于校验http请求的内容的存在，无内容返回None


def vornone(dict, key):
    if key in dict and dict[key] != "":
        return dict[key]
    else:
        return None


# 用于处理日志查找的http请求


def query(request):
    # 验证是否登录
    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")

    # 获取http post的request参数
    request_data = request.POST['request']

    # 初始化response
    response = "error"

    if None != request_data:
        try:
            # 将string进行序列化
            request = json.loads(request_data)
            # 判断是否存在return_count参数，如果有则select count *， return_count默认为无
            return_count = vornone(request, 'return_count')
            return_count = False if None == return_count else return_count

            # 调用api的query函数进行查找，输入可能存在的查找因素
            response = json.dumps(data.query(vornone(request, 'input_src'), vornone(request, 'input_sport'),
                      vornone(request, 'input_dst'), vornone(request, 'input_dport'),
                      vornone(request, 'tech_syn_flood'), vornone(request, 'tech_ack_flood'),
                      vornone(request, 'tech_udp_flood'), vornone(request, 'tech_icmp_flood'),
                      vornone(request, 'tech_connection_flood'),
                      vornone(request, 'tech_stream_flood'), vornone(request, 'tech_content_drop'),
                      vornone(request, 'tech_udp_dns_flood'), vornone(request, 'flag'),
                      vornone(request, 'start_time'), vornone(request, 'end_time'),
                      vornone(request, 'page'), return_count))
        except Exception , e:
            response = "error:" + "search error"

    return HttpResponse(response, content_type="application/json")


# 用于处理报表生成的http请求


def report(request):
    # 验证是否登录
    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")

    request_data = request.POST['request']

    response = "error"

    if None != request_data:
        try:
            # 将request_date进行序列化操作
            request = json.loads(request_data)
            # 获取报表的生成因素
            report_type = vornone(request, 'report_type')
            report_start_date = vornone(request, 'report_start_date')
            report_end_date = vornone(request, 'report_end_date')
            report_icon = vornone(request, 'report_icon')

            # 处理报表生成因素异常的情况，缺少参数一律直接返回错误
            if report_type is None or report_start_date is None or report_end_date is None or report_icon is None:
                return HttpResponse("error:args error")

            # report_icon为1，生成日报
            if report_icon == "1":
                report_data1 = data.report_query1(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data1)

            # report_icon为2，生成周报
            if report_icon == "2":
                report_data2 = data.report_query2(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data2)

            # report_icon为3，生成月报
            if report_icon == "3":
                report_data3 = data.report_query3(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data3)

        except:
            pass

    return HttpResponse(response, content_type="application/json")


# 用于处理登录请求


def login(request):
    result = {}

    user = request.POST['user']
    password = request.POST['password']

    login_state = auth.user_auth(user, password)
    result['result'] = login_state
    
    if login_state:
        auth.set_login(request)
    
    return HttpResponse(json.dumps(result), content_type = "application/json")


# 用于处理注销请求


def logout(request):
    auth.set_logout(request)
    request_redirect = request.GET['redirect']
    if None == request_redirect:
        return HttpResponse("OK")
    else:
        return HttpResponseRedirect(request_redirect)


# 用于处理重置密码请求


def reset_pass(request):
    # 用于确认是否登录
    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")

    request_str = vornone(request.POST, 'request')
    request_data = json.loads(request_str)

    if None != request_data and None != request_str:
        # 获取老密码和新密码
        old_pass = vornone(request_data, 'now_password')
        new_pass = vornone(request_data, 'new_password')

        # 通过session获取用户名
        user = request.session['user']

        # 处理缺少老密码或新密码的情况
        if old_pass is None or new_pass is None:
            return HttpResponse("error")

        # 对老密码进行验证，确认老密码是否输入正确
        if not auth.user_auth(user, old_pass):
            return HttpResponse("error: Current password is error, enter again please!")

        # 修改密码文件
        secret_file = sys.path[0] + "\\secret.txt"
        with open(secret_file, 'r') as file_tmp:
            secret = file_tmp.read()
            secret = json.loads(secret)

        with open(secret_file, 'w') as file_tmp:
            secret[user] = new_pass
            file_tmp.write(json.dumps(secret))

        # 注销当前登录会话，并返回成功用于浏览器跳转到主页
        auth.set_logout(request)
        return HttpResponse("success")

    #错误情况
    return HttpResponse("error")


# 待删除


def photo(request):
    if not auth.check_login(request):
        return HttpResponse("error")
    
    sid = request.REQUEST.get('id')
    if None == sid:
        return HttpResponseNotFound("not found")
    
    file_path = data.photo_path(sid)
    if not os.path.exists(file_path):
        return HttpResponseNotFound('not found')
    
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'image/jpeg'
    
    return response


def idcard(request):
    id_num = request.REQUEST.get('id')
    if None == id_num:
        return HttpResponse("error")
    
    url = "http://apis.baidu.com/apistore/idservice/id" + "?id=" + id_num.lower()
    headers = {
        'apikey':'ef804e1460acfabfd8b721c83e679f4b',
    }
    request = urllib2.Request(url, headers=headers)

    return HttpResponse(urllib2.urlopen(request).read())

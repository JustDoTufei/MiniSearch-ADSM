# Create your views here.

import json
import data
import auth
import os
import urllib2

from django.http.response import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, FileResponse


def vornone(dict, key):
    if key in dict and dict[key] != "":
        return dict[key]
    else:
        return None


def query(request):
    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")
    
    #request_data = request.REQUEST.get('request')
    request_data = request.POST['request']
    print request_data

    response = "error"

    if None != request_data:
        try:
            request = json.loads(request_data)
            return_count = vornone(request, 'return_count')
            return_count = False if None == return_count else return_count

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


def report(request):

    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")

    #request_data = request.REQUEST.get('request')
    request_data = request.POST['request']

    print request_data

    response = "error"

    if None != request_data:
        try:
            request = json.loads(request_data)
            report_type = vornone(request, 'report_type')
            report_start_date = vornone(request, 'report_start_date')
            report_end_date = vornone(request, 'report_end_date')
            report_icon = vornone(request, 'report_icon')

            if report_type is None or report_start_date is None or report_end_date is None or report_icon is None:
                return HttpResponse("error:args error")

            if report_icon == "1":
                report_data1 = data.report_query1(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data1)

            if report_icon == "2":
                report_data2 = data.report_query2(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data2)

            if report_icon == "3":
                report_data3 = data.report_query3(report_type, report_start_date, report_end_date)
                response = json.dumps(report_data3)
                print response

        except:
            pass

    #print response
    return HttpResponse(response, content_type="application/json")


def login(request):
    result = {}

    user = request.POST['user']
    password = request.POST['password']

    login_state = auth.user_auth(user, password)
    result['result'] = login_state
    
    if login_state:
        auth.set_login(request)
    
    return HttpResponse(json.dumps(result), content_type = "application/json")


def logout(request):
    auth.set_logout(request)
    #request_redirect = request.REQUEST.get('redirect')
    request_redirect = request.GET['redirect']
    if None == request_redirect:
        return HttpResponse("OK")
    else:
        return HttpResponseRedirect(request_redirect)


def reset_pass(request):

    if not auth.check_login(request):
        return HttpResponse("error: access denied", content_type="application/json")

    request_str = vornone(request.POST, 'request')
    request_data = json.loads(request_str)

    if None != request_data and None != request_str:

        old_pass = vornone(request_data, 'now_password')
        new_pass = vornone(request_data, 'new_password')

        user = request.session['user']

        if old_pass is None or new_pass is None:
            return HttpResponse("error")

        if not auth.user_auth(user, old_pass):
            return HttpResponse("error: Current password is error, enter again please!")

        with open('secret.txt', 'r') as file_tmp:
            secret = file_tmp.read()
            secret = json.loads(secret)

        with open('secret.txt', 'w') as file_tmp:
            secret[user] = new_pass
            file_tmp.write(json.dumps(secret))

        auth.set_logout(request)
        return HttpResponse("success")

    return HttpResponse("error")


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

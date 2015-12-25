'''
Created on May 24, 2015

@author: luodichen
'''

from pages import page_urls
from api import auth, interface
from django.template import Context, loader
from django.http.response import HttpResponse, HttpResponseRedirect
from urllib import urlencode


def login(request):
    if auth.check_login(request):
        return HttpResponseRedirect(page_urls.INFO)
    
    t = loader.get_template("login.html")
    c = Context({
        'login_url':interface.LOGIN,
        'on_success':page_urls.INFO,
    })
    return HttpResponse(t.render(c))


def info(request):
    if not auth.check_login(request):
        return HttpResponseRedirect(page_urls.LOGIN)
        
    t = loader.get_template("info.html")
    c = Context({
        'query_url': interface.QUERY,
        'logout_href': interface.LOGOUT + "?" + urlencode({"redirect":page_urls.LOGIN}),
        'login_url': interface.LOGIN,
        'current_url': page_urls.INFO,
        'idcard_url': interface.IDCARD,
        'report_href': page_urls.REPORT,
    })
    return HttpResponse(t.render(c))


def report(request):
    if not auth.check_login(request):
        return HttpResponseRedirect(page_urls.LOGIN)

    t = loader.get_template("report.html")
    c = Context({
        'report_query_url': interface.REPORT,
        'logout_href': interface.LOGOUT + "?" + urlencode({"redirect":page_urls.LOGIN}),
        'login_url': interface.LOGIN,
        'current_url': page_urls.REPORT,
        'idcard_url': interface.IDCARD,
        'report_href': page_urls.REPORT,
        'info_url': page_urls.INFO,
    })
    return HttpResponse(t.render(c))
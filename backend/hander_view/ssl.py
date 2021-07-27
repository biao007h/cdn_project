# Create your views here.
from django.shortcuts import render,HttpResponse
import json,re,copy
from tools.pager import *
from tools.forms_tpl import *
from database.model.models import *
from datetime import datetime
from datetime import date
class CJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def sslManage(request):
    ret=render(request, "ssl/sslmanage.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret

def getSslList(request):
    currentPage=int(request.GET.get("curr"))
    dataCount=int(Cert.objects.all().count())
    perPageCount=int(request.GET.get("nums"))
    page_obj = Pagination(dataCount=dataCount, currentPage=currentPage, perPageCount=perPageCount)
    data_start = page_obj.data_start()
    data_end = page_obj.data_end()
    certlist={
      "code": 0,
      "msg": "",
      "count": dataCount,
      "data": []
    }
    cert_obj=list(Cert.objects.all()[data_start:data_end].values())
    certlist["data"]=cert_obj
    return HttpResponse(json.dumps(certlist,cls=CJsonEncoder))

def addSsl(request):
    if request.is_ajax():
        ajax_rsp = {"status": "err", "msg": None}
        NewCert=Certform(data=request.POST)
        if NewCert.is_valid():
            print(NewCert.cleaned_data)
            Cert.objects.create(**NewCert.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = NewCert.errors
            print(NewCert.errors)
        return HttpResponse(json.dumps(ajax_rsp))
    ret=render(request, "ssl/addSsl.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret


def delSsl(request):
    if request.is_ajax():
        certArray=re.split(',',request.POST.get("Cert"))
        ajax_rsp={"status":"err","msg":None}
        try:
            for cert in certArray:
                Cert.objects.filter(crt=cert).delete()
            ajax_rsp["status"]= "ok"
        except Exception as e:
            ajax_rsp["msg"]=str(e)
        return HttpResponse(json.dumps(ajax_rsp))

    return HttpResponse("ok")

def editSsl(request):
    if request.is_ajax():
        postdata=copy.deepcopy(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        old_crt = request.POST.get("old_crt")
        del postdata["old_crt"]
        Newcrt=Certform(data=postdata)
        if Newcrt.is_valid():
            print(Newcrt.cleaned_data)
            Cert.objects.filter(crt=old_crt).update(**Newcrt.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = Newcrt.errors

        return HttpResponse(json.dumps(ajax_rsp))
    ret = render(request, "ssl/editSsl.html")
    ret["X-Frame-Options"] = "sameorigin"
    return ret
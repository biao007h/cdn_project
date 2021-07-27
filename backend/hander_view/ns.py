# Create your views here.
from backend.hander_view.ns import *
from django.shortcuts import render,HttpResponse
import json,re,copy
from tools.pager import *
from tools.forms_tpl import *
from database.model.models import *
def nsList(request):
    ret=render(request,"ns/nsList.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret

def getnsList(request):
    currentPage=int(request.GET.get("curr"))
    dataCount=int(NameServer.objects.all().count())
    perPageCount=int(request.GET.get("nums"))
    page_obj = Pagination(dataCount=dataCount, currentPage=currentPage, perPageCount=perPageCount)
    data_start = page_obj.data_start()
    data_end = page_obj.data_end()
    nslist={
      "code": 0,
      "msg": "",
      "count": dataCount,
      "data": []
    }
    ns_obj=list(NameServer.objects.all()[data_start:data_end].values())
    nslist["data"]=ns_obj
    return HttpResponse(json.dumps(nslist))


def addns(request):
    if request.is_ajax():
        print(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        Newns=nsform(data=request.POST)
        if Newns.is_valid():
            print(Newns.cleaned_data)
            NameServer.objects.create(**Newns.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = Newns.errors
        print(Newns.errors)
        return HttpResponse(json.dumps(ajax_rsp))
    ret=render(request,"ns/addns.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret


def delns(request):
    if request.is_ajax():
        nsArray=re.split(',',request.POST.get("ns"))
        ajax_rsp={"status":"err","msg":None}
        try:
            for ns in nsArray:
                NameServer.objects.filter(ns=ns).delete()
            ajax_rsp["status"]= "ok"
        except Exception as e:
            ajax_rsp["msg"]=str(e)
        return HttpResponse(json.dumps(ajax_rsp))

    return HttpResponse("ok")


def editns(request):
    if request.is_ajax():
        postdata=copy.deepcopy(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        old_ns = request.POST.get("old_ns")
        Newns=ns_update_form(data=postdata)
        if Newns.is_valid():
            print(Newns.cleaned_data)
            NameServer.objects.filter(ns=old_ns).update(**Newns.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = Newns.errors

        return HttpResponse(json.dumps(ajax_rsp))
    ret = render(request, "ns/editns.html")
    ret["X-Frame-Options"] = "sameorigin"
    return ret
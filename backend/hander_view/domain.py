# Create your views here.
from backend.hander_view.ns import *
from django.shortcuts import render,HttpResponse
import json,re,copy
from tools.pager import *
from tools.forms_tpl import *
from database.model.models import *
from django.db.models import F
def OneD1CList(request):
    ret=render(request,"domain/OneD1CList.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret

def get1D1CList(request):
    currentPage=int(request.GET.get("curr"))
    dataCount=int(NameServer.objects.all().count())
    perPageCount=int(request.GET.get("nums"))
    page_obj = Pagination(dataCount=dataCount, currentPage=currentPage, perPageCount=perPageCount)
    data_start = page_obj.data_start()
    data_end = page_obj.data_end()
    dClist={
      "code": 0,
      "msg": "",
      "count": dataCount,
      "data": []
    }
    dC_obj=list(Domain_Cname.objects.all()[data_start:data_end].values("id","domain__domain","cname__cname"))
    dClist["data"]=dC_obj
    return HttpResponse(json.dumps(dClist))


def add1D1C(request):
    if request.is_ajax():
        ajax_rsp = {"status": "err", "msg": None}
        Newns=nsform(data=request.POST)
        if Newns.is_valid():
            print(Newns.cleaned_data)
            NameServer.objects.create(**Newns.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = Newns.errors
        return HttpResponse(json.dumps(ajax_rsp))
    ns_list=NameServer.objects.all()
    group_list=Group.objects.all()
    protocol_type=SubDomain_Src.protocol_type
    ret=render(request,"domain/add1D1C.html",{"ns_list":ns_list,"group_list":group_list,"protocol_type":protocol_type})
    ret["X-Frame-Options"]="sameorigin"
    return ret


def del1D1C(request):
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


def edit1D1C(request):
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
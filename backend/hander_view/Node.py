# Create your views here.
from backend.hander_view.Node import *
from django.shortcuts import render,HttpResponse
import json,re,copy
from tools.pager import *
from tools.forms_tpl import *
from database.model.models import *
def nodeList(request):
    ret=render(request, "node/nodeList.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret

def getNodeList(request):

    currentPage=int(request.GET.get("curr"))
    dataCount=int(Node.objects.all().count())
    perPageCount=int(request.GET.get("nums"))
    page_obj = Pagination(dataCount=dataCount, currentPage=currentPage, perPageCount=perPageCount)
    data_start = page_obj.data_start()
    data_end = page_obj.data_end()
    nodelist={
      "code": 0,
      "msg": "",
      "count": dataCount,
      "data": []
    }
    node_ip=request.GET.get("node_ip","")
    group_name=request.GET.get("group_name","")
    searchParam={}
    # node_ip如果为空，crm搜不到值，所以创建searchparam字典，没有就不赋值
    # 这样搜出来就是全部
    print(searchParam)
    if node_ip:
        searchParam["node_ip"]=node_ip
    if group_name:
        searchParam["node_group__Group__group_name"]=group_name
    node_obj=list(Node.objects.filter(**searchParam)[data_start:data_end].values())
    for item in node_obj:
        if item["work_or_no"]=="1":
            item["work_or_no"]="开"
        else:
            item["work_or_no"] = "关"
    nodelist["data"]=node_obj
    return HttpResponse(json.dumps(nodelist))


def addNode(request):
    if request.is_ajax():
        print(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        NewNode=Nodeform(data=request.POST)
        if NewNode.is_valid():
            print(NewNode.cleaned_data)
            Node.objects.create(**NewNode.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = NewNode.errors
        print(NewNode.errors)
        return HttpResponse(json.dumps(ajax_rsp))
    ret=render(request, "node/addNode.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret


def delNode(request):
    if request.is_ajax():
        nodeArray=re.split(',',request.POST.get("Nodeip"))
        ajax_rsp={"status":"err","msg":None}
        try:
            for ip in nodeArray:
                Node.objects.filter(node_ip=ip).delete()
            ajax_rsp["status"]= "ok"
        except Exception as e:
            ajax_rsp["msg"]=str(e)
        return HttpResponse(json.dumps(ajax_rsp))

    return HttpResponse("ok")


def editNode(request):
    if request.is_ajax():
        postdata=copy.deepcopy(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        old_node_ip = request.POST.get("old_node_ip")
        NewNode=Node_update_form(data=postdata)
        if NewNode.is_valid():
            print(NewNode.cleaned_data)
            Node.objects.filter(node_ip=old_node_ip).update(**NewNode.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = NewNode.errors

        return HttpResponse(json.dumps(ajax_rsp))
    ret = render(request, "node/editNode.html")
    ret["X-Frame-Options"] = "sameorigin"
    return ret
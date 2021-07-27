from django.shortcuts import render,HttpResponse
from tools.pager import *
import json,copy,re
from tools.forms_tpl import *
def groupControl(request):
    ret=render(request, "group/groupControl.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret

def getGroupList(request):

    currentPage=int(request.GET.get("curr"))
    dataCount=int(Group.objects.all().count())
    perPageCount=int(request.GET.get("nums"))
    page_obj = Pagination(dataCount=dataCount, currentPage=currentPage, perPageCount=perPageCount)
    data_start = page_obj.data_start()
    data_end = page_obj.data_end()
    Grouplist={
      "code": 0,
      "msg": "",
      "count": dataCount,
      "data": []
    }
    Group_obj=list(Group.objects.all()[data_start:data_end].values())
    Grouplist["data"]=Group_obj
    return HttpResponse(json.dumps(Grouplist))


def addGroup(request):
    if request.is_ajax():
        print(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        NewGroup=Groupform(data=request.POST)
        if NewGroup.is_valid():
            print(NewGroup.cleaned_data)
            Group.objects.create(**NewGroup.cleaned_data)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = NewGroup.errors
        print(NewGroup.errors)
        return HttpResponse(json.dumps(ajax_rsp))
    ret=render(request, "group/addGroup.html")
    ret["X-Frame-Options"]="sameorigin"
    return ret


def delGroup(request):
    if request.is_ajax():
        GroupArray=re.split(',',request.POST.get("group_name"))
        ajax_rsp={"status":"err","msg":None}
        try:
            for group in GroupArray:
                Group.objects.filter(group_name=group).delete()
            ajax_rsp["status"]= "ok"
        except Exception as e:
            ajax_rsp["msg"]=str(e)
        return HttpResponse(json.dumps(ajax_rsp))

    return HttpResponse("ok")
#
#
def editGroup(request):
    if request.is_ajax():
        # 取出新的ip id值列表
        node=[]
        for item in json.loads(request.POST.get("use_node")):
            node.append(str(item['value']))
        print(node)
        postdata=copy.deepcopy(request.POST)
        ajax_rsp = {"status": "err", "msg": None}
        old_Group_name = request.POST.get("old_group_name")
        new_Group_name = request.POST.get("group_name")
        NewGroup=GroupRegform(data=request.POST)
        if NewGroup.is_valid():
            print(NewGroup.cleaned_data)
            Group.objects.filter(group_name=old_Group_name).delete()
            Group.objects.create(**NewGroup.cleaned_data)
            Group.objects.filter(group_name=old_Group_name).update(**NewGroup.cleaned_data)
            NewGroup_obj=Group.objects.filter(group_name=new_Group_name).first()
            node_obj=Node.objects.filter(id__in=node)
            for obj in node_obj:
                Node_Group.objects.create(Group=NewGroup_obj,Node=obj)
            ajax_rsp["status"]="ok"
        else:
            ajax_rsp["msg"] = NewGroup.errors
        return HttpResponse(json.dumps(ajax_rsp))
    ret = render(request, "group/editGroup.html")
    ret["X-Frame-Options"] = "sameorigin"
    return ret

def getGroupUseNode(request):
    group_name=request.POST.get('old_group_name')
    node_all=Node.objects.all().values("id","node_ip")
    use_node=Node.objects.filter(node_group__Group=group_name).values_list("id")
    GroupUseNode={ }
    GroupUseNode["data"]=list(node_all)
    GroupUseNode["value"]=list(use_node)
    print(json.dumps(GroupUseNode))
    return HttpResponse(json.dumps(GroupUseNode))

# Create your views here.
from tools.check_code import *
from io import BytesIO
from backend.hander_view.Group import *
from backend.hander_view.Node import *
from backend.hander_view.ssl import *
from backend.hander_view.ns import *
from backend.hander_view.domain import *
from django.shortcuts import render,HttpResponse,redirect

def login(request):
    if request.is_ajax():
        print(request.POST)
        captcha=request.POST.get("captcha")
        ajax_asp={"status":"err","errmsg":None}
        username=request.POST.get("username")
        password=request.POST.get("password")
        if captcha.lower() != request.session.get("captcha").lower():
            ajax_asp["errmsg"]="验证码错误"
        elif not User.objects.filter(user_name=username):
            ajax_asp["errmsg"] = "用户名不存在"
        elif not User.objects.filter(user_name=username,user_password=password):
            ajax_asp["errmsg"] = "密码错误"
        else:
            ajax_asp["status"] = "ok"
            request.session["is_login"]=True
            request.session["username"]=username
        return HttpResponse(json.dumps(ajax_asp))
    return render(request,'login.html')


def loginOut(request):
    request.session.flush()
    return HttpResponse("flush ok")


def index(request):
    if not request.session.get("is_login"):
        return redirect('/backend/login')
    username=request.session.get("username")
    print(username)
    return render(request,'index.html',{
        "username":username,
    })


def get_CheckCode(request):
    code_pic=BytesIO()
    img,code=create_validate_code()
    img.save(code_pic,'PNG')
    request.session["captcha"]=code
    print(code)
    return HttpResponse(code_pic.getvalue())


from tools.pemissionControl import *
import json
def print_json(data):
    print(json.dumps(data, sort_keys=True, indent=4, separators=(', ', ': '), ensure_ascii=False))
def getMenu(request):
    user=request.session.get("username")
    per_obj=pemissionControl(user)
    Menu=per_obj.creatLayuiSimpleMenu()
    # Menu=per_obj.creatLayuiMenu()

    print_json(Menu)
    ret=HttpResponse(json.dumps(Menu))
    ret["X-Frame-Options"]="sameorigin"
    return ret


def asset(request):
    # token_list=[]
    # token=request.POST.get("token")
    # Time=request.POST.get("Time")
    # token_ele={
    #     "token":token,
    #     "Time":Time,
    #     "hostname":"xxx"
    # }
    # if token_ele in token_list:
    #     # 如果完全匹配则接受
    #     accept()
    # else:
    #     # 如果不匹配且token在，则表明被黑了，决绝
    #     for item in token_list:
    #         if item["token"] == token:
    #             refuse()
    #     Token = "asd23k4uhg23t894iasjdf8o"
    #     Time = time.time()
    #     Token_Time = "%s|%s" % (Token, Time)
    #     Token_Time_md5 = hashlib.md5(Token_Time.encode(encoding='utf-8')).hexdigest()
    #     # 如果哈希值匹配则加入列表并接受，并传递超时时间
    #     if token ==  Token_Time_md5
    #         token_list.append(token_ele)
    #         accept()
    #         request.session["tokenUseTime"]=Time+超时时间
    print(Menu.objects.all().values("icon","title"))
    return HttpResponse("200ok")


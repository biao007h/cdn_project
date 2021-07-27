"""cdn_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
from backend import views
domain_url =[
    path('1D1CList', views.OneD1CList),
    path('get1D1CList', views.get1D1CList),
    path('add1D1C', views.add1D1C),
    path('del1D1C', views.del1D1C),
    path('edit1D1C', views.edit1D1C),
]
ns_url =[
    path('nsList', views.nsList),
    path('getnsList', views.getnsList),
    path('addns', views.addns),
    path('delns', views.delns),
    path('editns', views.editns),
]
node_url =[
    path('nodeList', views.nodeList),
    path('getNodeList', views.getNodeList),
    path('addNode', views.addNode),
    path('delNode', views.delNode),
    path('editNode', views.editNode),
]
group_url =[
    path('groupControl',views.groupControl),
    path('getGroupList',views.getGroupList),
    path('addGroup',views.addGroup),
    path('delGroup',views.delGroup),
    path('editGroup',views.editGroup),
    path('getGroupUseNode',views.getGroupUseNode),
]
ssl_url=[
    path('sslManage', views.sslManage),
    path('getSslList', views.getSslList),
    path('addSsl', views.addSsl),
    path('delSsl', views.delSsl),
    path('editSsl', views.editSsl),
]
backend_url = [
    path('login',views.login),
    path('loginOut',views.loginOut),
    path('index',views.index),
    path('get_CheckCode',views.get_CheckCode),
    path('node/',include(node_url)),
    path('group/', include(group_url)),
    path('ssl/', include(ssl_url)),
    path('ns/', include(ns_url)),
    path('domain/', include(domain_url)),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include(backend_url)),
    path('getMenu/', views.getMenu),
    path('asset/', views.asset),
]

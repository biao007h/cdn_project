
from database.model.permission import *

class pemissionControl(object):

    def __init__(self,user="default"):
        self.user=user
        self.PemissionDict={}
        self.MenuDict={}
        self.LayuiMenuDict={}
        self.LayuiLastMenu={
                "homeInfo": {
                    "title": "首页",
                    "href": "/static/page/welcome-1.html?t=1"
                },
                "logoInfo": {
                    "title": "LAYUI MINI",
                    "image": "/static/images/logo.png",
                    "href": ""
                },
                "menuInfo": []
            }
    def getPemissionDict(self):
        user=User.objects.filter(user_name=self.user).first()
        # 一个用户多角色
        role=Roles.objects.filter(user2role__user=user)
        page_action_obj=list(Role2Page2Actions.objects.filter(role__in=role).distinct().values_list("page_action__page__page","page_action__action__code"))
        # 对权限列表进行判断，如果没有键值就生成列表赋值，否则追加到列表后面
        # 最终字典格式: {'index': ['put', 'get'], 'test.html': ['get']}
        for item in page_action_obj:
            if self.PemissionDict.get(item[0]):
                if self.PemissionDict[item[0]].count(item[1]) == 0:  # 列表去重
                    self.PemissionDict[item[0]].append(item[1])
            else:
                self.PemissionDict[item[0]] = [item[1]]
        return self.PemissionDict

    def createMenuEle(self,menu_id,menu_str,parent_id):
        ele_dict = {
           "menu_id": menu_id,
             "title": menu_str,
         "parent_id": parent_id,
             "child": []
        }
        return ele_dict

    def createPageEle(self,item):
        ele_dict = {
          "title": item,
          "url":""
        }
        return ele_dict


    def InitMenuDict(self):
        # 生成菜单
        # 理论上应该根据菜单多次查找父级菜单，但是那样变成数据库多次操作
        # 因为菜单数量不多，一次取出全部，再根据对象操作更为高效
        menu_obj=Menu.objects.all().values_list("id","title","father_menu")
        for item in menu_obj:
            menu_ele= self.createMenuEle(item[0],item[1],item[2])
            self.MenuDict[str(item[0])]=menu_ele
        return self.MenuDict


    def PageHangToMenu(self):
        # 权限列表的key为页面值，所以可以用keys取有权访问的页面
        PemissionDict=self.getPemissionDict()
        self.InitMenuDict()
        for item in PemissionDict.keys():
            item_ele=self.createPageEle(item)
            MenuPage_obj=list(Menu2Page.objects.filter(page__page=item).values("menu_id"))
            for MenuPage_ele in MenuPage_obj:
                self.MenuDict[str(MenuPage_ele["menu_id"])]["child"].append(item_ele)
        return self.MenuDict

    def creatMenu(self):
        MenuDict=self.PageHangToMenu()
        menu_obj = list(Menu.objects.all().values("id", "father_menu"))
        # 菜单的挂载最新想到的逻辑是从生成的字典中pop子菜单id加入父菜单的child中
        # 但是这样不确定父菜单是不是别的子菜单，如果是，父菜单先挂载后，子菜单会找不到已经被挂载的父菜单
        # 所以就不pop子菜单，而是全部挂载后，再判断菜单节点的child是否为空，从中剔除
        # 而能这样做的原因在于，python对象是同一片内存区域，当你挂载的时候，它并不重新生成对象
        # 所以不会出现子挂父，父还要挂爷的情况
        # 但是还要记录挂载的子菜单id，没挂载过的就是根id，据此删除多余的菜单
        sonId = []
        for menu_ele in menu_obj:
            if menu_ele["father_menu"] :
                sonId.append(menu_ele['id'])
                MenuDict[str(menu_ele["father_menu"])]["child"].append(MenuDict[str(menu_ele["id"])])

        for menu_ele in list(MenuDict.keys()):
            if not MenuDict[menu_ele].get("child"):
                del MenuDict[menu_ele]
            elif int(menu_ele) in sonId:
                del MenuDict[menu_ele]
        return MenuDict
################# layui ###################################
    def createLayuiMenuEle(self,menu_id,menu_str,parent_id,icon,target):
        ele_dict = {
           "menu_id": menu_id,
           "title"  : menu_str,
         "parent_id": parent_id,
             "child": [],
            "icon"  : icon,
            "target": target
        }
        return ele_dict

    def createLayuiPageEle(self,page,target,icon):
        ele_dict = {
        "target"  : target,
          "href"  : page,
        }
        return ele_dict
    def InitLayuiMenuDict(self):
        # 生成菜单
        # 理论上应该根据菜单多次查找父级菜单，但是那样变成数据库多次操作
        # 因为菜单数量不多，一次取出全部，再根据对象操作更为高效
        menu_obj=Menu.objects.all().values_list("id","title","father_menu","icon","target")
        for item in menu_obj:
            menu_ele=self.createLayuiMenuEle(*item)
            self.LayuiMenuDict[str(item[0])]=menu_ele
        return self.LayuiMenuDict

    def LayuiPageHangToMenu(self):
        # Layui最后一个菜单只有一个页面，不存在多个页面问题，所以直接用字典update，而不用列表的append
        PemissionDict=self.getPemissionDict()
        self.InitLayuiMenuDict()
        page_ele=Pages.objects.filter(page__in=PemissionDict.keys()).values_list("page","target","icon")
        for item in page_ele:
            item_ele=self.createLayuiPageEle(*item)  # 元组展开用*,字典展开用 **
            MenuPage_obj=list(Menu2Page.objects.filter(page__page=item[0]).values("menu_id"))
            for MenuPage_ele in MenuPage_obj:
                self.LayuiMenuDict[str(MenuPage_ele["menu_id"])].update(item_ele)
        return self.LayuiMenuDict

    def creatLayuiMenu(self):
        LayuiMenuDict=self.LayuiPageHangToMenu()
        menu_obj = list(Menu.objects.all().values("id", "father_menu"))
        sonId=[]
        for menu_ele in menu_obj:
            if menu_ele["father_menu"] :
                sonId.append(menu_ele['id'])
                LayuiMenuDict[str(menu_ele["father_menu"])]["child"].append(LayuiMenuDict[str(menu_ele["id"])])

        for menu_ele in list(LayuiMenuDict.keys()):
            if not LayuiMenuDict[menu_ele].get("child"):
                del LayuiMenuDict[menu_ele]
            elif int(menu_ele) in sonId:
                del LayuiMenuDict[menu_ele]
        # 去掉id，做成列表加到默认的Menuinfo
        for item in LayuiMenuDict:
            self.LayuiLastMenu["menuInfo"].append(LayuiMenuDict[item])
        return self.LayuiLastMenu

    def creatLayuiSimpleMenu(self):
        LayuiMenuDict=self.LayuiPageHangToMenu()
        menu_obj = list(Menu.objects.all().values("id", "father_menu"))
        # 不生成的菜单有两个特性：
        #  1.不是挂载页面的菜单
        #  2.不是别的菜单的父菜单
        # 据此，可以判断id是否在这个范围，然后不做挂载处理，直接continue
        useInMenuId=list(Menu.objects.all().values_list("father_menu",flat=True))
        useInPageId=list(Pages.objects.all().values_list("belong_menu",flat=True))
        sonId=[]
        useInMenuId.extend(useInPageId)
        for menu_ele in menu_obj:
            if menu_ele['id'] not in useInMenuId:
                continue
            if menu_ele["father_menu"] :
                sonId.append(menu_ele['id'])
                LayuiMenuDict[str(menu_ele["father_menu"])]["child"].append(LayuiMenuDict[str(menu_ele["id"])])
        for menu_ele in list(LayuiMenuDict.keys()):
            if not LayuiMenuDict[menu_ele].get("child"):
                del LayuiMenuDict[menu_ele]
            elif int(menu_ele) in sonId:
                del LayuiMenuDict[menu_ele]
        # 去掉id，做成列表加到默认的Menuinfo
        for item in LayuiMenuDict:
            self.LayuiLastMenu["menuInfo"].append(LayuiMenuDict[item])
        return self.LayuiLastMenu
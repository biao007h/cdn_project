from django.contrib import admin
from database.model.models import User,Node,Node_Group,Group
from database.model.permission import *
# Register your models here.
admin.site.register(User)
admin.site.register(Node)
admin.site.register(Node_Group)
admin.site.register(Group)
admin.site.register(Roles)
admin.site.register(Role2Page2Actions)
admin.site.register(Pages)
admin.site.register(Page2Actions)
admin.site.register(Actions)
admin.site.register(User2Role)
admin.site.register(Menu)
admin.site.register(Menu2Page)
admin.site.register(Cert)
admin.site.register(NameServer)
admin.site.register(Cname)
admin.site.register(Domain)
admin.site.register(Domain_Cname)
admin.site.register(Cname_Group)
admin.site.register(SubDomain_Src)
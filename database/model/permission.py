
from database.model.models import *
class Roles(models.Model):
    roles_name=models.CharField(max_length=16)
    class Meta:
        verbose_name_plural = "角色表"
    def __str__(self):
        return self.roles_name

class Actions(models.Model):
    action = models.CharField(max_length=16)
    code = models.CharField(max_length=16)
    class Meta:
        verbose_name_plural = "操作"
    def __str__(self):
        return  "%s - %s" %(self.action,self.code)

class Menu(models.Model):
    title = models.CharField(max_length=32)
    href = models.CharField(max_length=64,blank=True)
    icon = models.CharField(max_length=32,blank=True)
    target = models.CharField(max_length=32, default="_self")
    father_menu=models.ForeignKey("Menu",null=True,blank=True,on_delete=models.DO_NOTHING)
    class Meta:
        verbose_name_plural = "菜单表"
    def __str__(self):
        return  self.title

class Pages(models.Model):
    target=models.CharField(max_length=32,default="_self")
    icon=models.CharField(max_length=32,blank=True)
    page = models.CharField(max_length=32)
    belong_menu = models.ForeignKey(Menu,on_delete=models.CASCADE)
    def __str__(self):
        return  self.page

class User2Role(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    role=models.ForeignKey(Roles,on_delete=models.CASCADE)
    def __str__(self):
        return  "%s-%s" %(self.user,self.role)

class Page2Actions(models.Model):
    page=models.ForeignKey(Pages,on_delete=models.CASCADE)
    action=models.ForeignKey(Actions,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "页面权限表"
    def __str__(self):
        return "%s - %s" %(self.page,self.action)

class Role2Page2Actions(models.Model):
    role=models.ForeignKey(Roles,on_delete=models.CASCADE)
    page_action=models.ForeignKey(Page2Actions,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = "角色权限表"
    def __str__(self):
        return "%s -%s-%s" %(self.role,self.page_action.page,self.page_action.action)


class Menu2Page(models.Model):
    page=models.ForeignKey(Pages,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)

    def __str__(self):
        return  "%s-%s" %(self.menu,self.page)
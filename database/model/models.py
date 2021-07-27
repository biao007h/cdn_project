from django.db import models

# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=32,unique=True)
    user_password=models.CharField(max_length=32)
    user_create_at=models.DateField(auto_created=True)
    # is_active=models.CharField(max_length=5,choices=(('1','yes'),('0','no')),default=0)
    # user_power=models.CharField(max_length=5,choices=(("1","supper"),("2","common")))
    def __str__(self):
        return  self.user_name



class Node(models.Model):
    work_status = {
        ("1", "active"),
        ("0", "inactive")
    }
    node_ip=models.GenericIPAddressField(unique=True)
    work_or_no=models.CharField(max_length=2,choices=work_status)
    remark=models.CharField(max_length=32,null=True)
    def __str__(self):
        return self.node_ip

class Group(models.Model):
    group_name=models.CharField(max_length=32,unique=True)
    remark = models.CharField(max_length=32, null=True)
    def __str__(self):
        return self.group_name


class Node_Group(models.Model):
    Group=models.ForeignKey(
        to="Group",
        to_field="group_name",
        on_delete=models.CASCADE,
    )
    Node=models.ForeignKey(
        to="Node",
        to_field="node_ip",
        on_delete=models.CASCADE,
    )


class Domain(models.Model):
    domain=models.CharField(max_length=256)
    owner=models.ForeignKey(
        to="User",
        to_field="user_name",
        on_delete=models.DO_NOTHING
    )
    def __str__(self):
        return self.domain

class Cert(models.Model):
    crt=models.TextField()
    key=models.TextField()
    contain_domain=models.TextField()
    expired_time=models.DateField()
    def __str__(self):
        return self.contain_domain


class NameServer(models.Model):
    ns=models.CharField(max_length=254,unique=True)
    alias=models.CharField(max_length=32)
    def __str__(self):
        return self.ns

class Cname(models.Model):
    ns=models.ForeignKey(
        to="NameServer",
        to_field="ns",
        on_delete=models.CASCADE,)
    cname=models.CharField(max_length=254,unique=True)
    def __str__(self):
        return self.cname

class Cname_Group(models.Model):
    group=models.ForeignKey(
        to="Group",
        on_delete=models.SET_NULL,
        null=True
    )
    cname=models.ForeignKey(
        to="Cname",
        to_field="cname",
        on_delete=models.CASCADE,
    )
    unique_together =[['group','cname']]


class  SubDomain_Src(models.Model):
    protocol_type={
        ("1","http"),
        ("2","https"),
        ("3","ws"),
        ("4","wss"),
    }
    pre_proto=models.CharField(choices=protocol_type,max_length=2)
    pre_port=models.IntegerField()
    host_head=models.CharField(max_length=32)
    domain=models.ForeignKey("Domain",on_delete=models.CASCADE)
    use_src=models.CharField(max_length=256)
    suf_proto = models.CharField(choices=protocol_type, max_length=2)
    suf_port = models.IntegerField()

class Domain_Cname(models.Model):
    domain = models.ForeignKey("Domain", on_delete=models.CASCADE)
    cname = models.ForeignKey(
        "Cname",
        on_delete=models.SET_NULL,
        null=True)
    def __str__(self):
        return "%s    %s" %(self.domain,self.cname)
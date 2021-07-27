from django import forms
from database.model.models import *
from django.core.exceptions import ValidationError
from tools.checkssl import *
import re,datetime
class  Nodeform(forms.Form):

    node_ip=forms.GenericIPAddressField(
        required=True,
    )
    work_or_no=forms.ChoiceField(choices=(("1","active"),("0","inactive")),)
    remark=forms.CharField(required=False,)
    def clean_node_ip(self):
        node_ip = self.cleaned_data.get("node_ip")
        if Node.objects.filter(node_ip=node_ip).exists():
            raise ValidationError("ip已存在")
        else:
            return node_ip

class  Node_update_form(forms.Form):

    node_ip=forms.GenericIPAddressField(
        required=True,
    )
    work_or_no=forms.ChoiceField(choices=(("1","active"),("0","inactive")),)
    remark=forms.CharField(required=False,)


class Groupform(forms.Form):
    group_name=forms.CharField(required=True)
    remark=forms.CharField(required=False,)
    def clean_group_name(self):
        group_name = self.cleaned_data.get("group_name")
        if Group.objects.filter(group_name=group_name).exists():
            raise ValidationError("分组已存在")
        else:
            return group_name

class GroupRegform(forms.Form):
    group_name=forms.CharField(required=True)
    remark=forms.CharField(required=False,)

class Certform(forms.Form):
    crt=forms.CharField(required=True)
    key=forms.CharField(required=True)

    # crt 格式判断
    def clean_crt(self):
        crt = self.cleaned_data.get("crt")
        if Cert.objects.filter(crt=crt).exists():
            raise ValidationError("证书已存在")
        else:
            r = re.compile("\s*-----BEGIN (.*)CERTIFICATE-----\n")
            m = r.match(crt)
            if not m:
                raise ValidationError("Not a valid PEM pre boundary")
            marker = m.group(1)
            r = re.compile("-----END (.*)CERTIFICATE-----\s*$")
            m = r.search(crt)
            if not m or m.group(1) != marker:
                raise ValidationError("Not a valid PEM post boundary")
            return crt

    # key格式判断
    def clean_key(self):
        r = re.compile("\s*-----BEGIN (.*)KEY-----\n")
        key = self.cleaned_data.get("key")
        m = r.match(key)
        if not m:
            raise ValidationError("Not a valid PEM pre boundary")
        marker = m.group(1)
        r = re.compile("-----END (.*)KEY-----\s*$")
        m = r.search(key)
        if not m or m.group(1) != marker:
            raise ValidationError("Not a valid PEM post boundary")
        return key

    # 证书匹配，并赋值过期时间和认证域名
    def clean(self):
        crt = self.cleaned_data.get("crt")
        # clean_crt里面如果已存在，则raise，此时没有return crt的值，crt的值为空，如果不判断会在cert_key的检验中报错
        if not crt:
            return
        key = self.cleaned_data.get("key")
        cert_obj = cert_key(crt, key)
        if cert_obj.verify() == "ok":
            self.cleaned_data["contain_domain"]=cert_obj.get_subject_domain()
            dt = datetime.datetime.strptime(cert_obj.get_expired_time(), "%Y%m%d%H%M%SZ").strftime('%Y-%m-%d')
            self.cleaned_data["expired_time"]=str(dt)
            return self.cleaned_data
        else:
            raise ValidationError("证书和key不匹配")


class nsform(forms.Form):
    ns=forms.CharField(max_length=256)
    alias=forms.CharField(required=False)
    def clean_ns(self):
        ns = self.cleaned_data.get("ns")
        if NameServer.objects.filter(ns=ns).exists():
            raise ValidationError("ns已存在")
        else:
            return ns

class ns_update_form(forms.Form):
    ns = forms.CharField(max_length=256)
    alias = forms.CharField(required=False)
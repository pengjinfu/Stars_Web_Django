import json

from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_POST, require_GET

from Stars_Web_Django.settings import EMAIL_FROM
from Users.models import User, EmailValid, EmailType
from utils.email import get_random_code, check_email
from utils.permission import check_login


@require_POST
def login_auth(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(Q(username=data['username']) | Q(email=data['username']))
        # 验证密码
        if not user.check_password(data['password']):
            return JsonResponse(status=400, data={'status': 2, 'msg': '用户名或密码错误!'})
        obj = redirect(reverse('Users:login'))
        obj.set_cookie('Token', user.token, 60*60*24)
    # 未找到用户
    except User.DoesNotExist:
        return JsonResponse(status=400, data={'status': 2, 'msg': '用户名&邮箱未注册!'})
    # 缺少参数
    except KeyError:
        return JsonResponse(status=400, data={'status': 2, 'msg': '不合法的参数!'})
    return obj


@require_POST
def register(request):
    data = json.loads(request.body)
    print(data)
    try:
        username = data['username']  # 用户名
        password = data['password']  # 密码
        nickname = data['nickname']  # 昵称
        email_item = email = data['email']  # 邮箱
        check = data['check']  # 验证码
        check_email(email, EmailType.REGISTER, check)
        User.objects.create_user(username, password, nickname, email)
        # 创建成功就删除对应的邮件
        email_item.delete()
    except KeyError:
        return JsonResponse(status=400, data={'status': 2, 'msg': '不合法的请求数据'})
    except ValueError as e:
        return JsonResponse(status=400, data={'status': 2, 'msg': str(e)})
    except ValidationError as e:
        return JsonResponse(status=400, data={'status': 2, 'msg': str(e)})
    return JsonResponse(data={'status': 1, 'msg': f'创建用户 {nickname} 成功'})


@require_POST
def email_register_verify(request):
    data = json.loads(request.body)
    resp = {}
    try:
        email = data['email']
        obj = User.objects.filter(email=email)
        if not obj:
            subject = '【群星小说网】欢迎加入群星小说网~请接收您的验证码'  # 邮件标题
            code = get_random_code()  # 获取一个随机的验证码
            print(code)
            text_content = f'我才不会告诉你验证码是 {code} 呢!'  # 邮件的文本格式
            html_content = f'<span>我才不会告诉你验证码是 <br><b>{code}</b><br> </span>呢!'  # 邮件的html格式
            msg = EmailMultiAlternatives(subject, text_content, EMAIL_FROM, [email])
            msg.attach_alternative(html_content, 'text/html')
            msg.send()
            resp['status'] = 1
            resp['msg'] = '发送邮件成功'
        else:
            resp['status'] = 2
            resp['msg'] = '邮箱已被注册!'
            return JsonResponse(status=400, data=resp)
    except Exception as e:
        # 简单的异常处理,后期需要进行细分.
        resp['status'] = 3
        resp['msg'] = str(e)
        return JsonResponse(status=400, data=resp)
    else:
        EmailValid.objects.create(code=code, email_address=email)
    # 成功就返回一个200状态码就行了.
    return JsonResponse(data=resp)


@require_GET
@check_login
def main(request):
    return HttpResponse('用户中心')

# 群星小说网

## **项目说明**

**开发环境: python3.8 + django3.1**

**依赖:**

- **django**  # 开发框架
- **django-cors-headers**  # 解决跨域问题
- **mysql, mysqlclient**  # 连接mysql数据库
- **django-shortuuidfield**  # 自动生成用户的uid

本项目将会采用两种开发方式,分别是

- 前后端结合,即前后端都用django来做.
- 前后端分离,后端用drf来做,前端用vue来做.

**当前项目采用前后端结合实现**

**前后端分离项目地址:** 

后端: https://github.com/challeger/Starts_Web

前端: 暂无

本项目目标是实现一个大型的小说网站,目标功能包括 **用户的注册登录等基本操作(用邮箱验证实现)**, **用户的VIP等级**, **用户与作者两种身份**, **小说的订阅,投票等**

## **开发日志**

### **2020.09.30**

​	项目初始化,环境配置

​	创建Users模型,在settings.py中对 会用的到应用与数据库进行了配置

### **2020.10.02**

​	前端页面 登录注册页面的完成,表单数据的提交试用ajax来实现.

​	后台的邮箱验证逻辑还没实现,预计明天完成.

### **2020.10.03**

​	完成了邮箱注册功能.登录验证准备用jwt来做

​	使用中间件+jwt实现了登录验证,在用户登录后会设置一个 时长一天的 Token 在cookie上,然后通过中间件在每次请求中判断是否带有token,有则将request.user设置为获取到的user.

​	然后自定义一个验证装饰器,判断request.user是否是User类,是的话说明已经登录的.

## Bug记录

### **2020 09 30**

#### **1.自定义用户模型替换之后,创建迁移失败**

**原因:** 修改用户模型之前进行了迁移,数据库之前已经创建了与用户相关的依赖表

**修改:** 删库重建.

### **2020 10 02**

#### **1. CSRF验证**

**原因:** 在使用ajax提交表单数据时遇到了csrf验证问题

**解决办法:** 将ajax请求的请求头加上一个csrf token

```
$.ajaxSetup({
        beforeSend: function(xhr, settings){
            xhr.setRequestHeader("X-CSRFToken", "{{ csrf_token }}")
        }
    });
```

#### **2. SMTP出现编码问题**

**原因:** 计算机名中带了中文,导致出现**UnicodeDecodeError**

**解决办法:** 修改计算机名... (我是nt)

### **2020 10 03**

#### **1. 邮箱验证失败**

**原因:** 邮箱的验证密码失效

**解决办法:** 重新获取验证密码
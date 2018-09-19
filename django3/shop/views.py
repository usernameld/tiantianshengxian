from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Shop, Category, Goods,Cart,CartGoods,Site,OrderInfo,OrderGoods  # 数据库表名
# from .form import Shop
from .form import LoginForm
import math
from django.core.paginator import Paginator#分页类


#注册
def register(request):
    # 获取表单数据
    if request.method == 'POST':
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        email = request.POST.get('email')
        # 正则验证数据
        # 使用模型类添加用户
        shop = Shop.objects.create(username=username, password=password1, email=email)  # 只写一个密码是因为数据库只有一个密码
        if shop is not None:
            return HttpResponse('注册成功')
        else:
            return HttpResponse('注册失败')
    else:
        return render(request, 'register.html')




#form登录
def login(request):
    if request.method == 'POST':
        # 用表单提交过来的数据创建一个LoginForm对象
        form = LoginForm(request.POST)
        # 判断表单数据是否合法
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = Shop.objects.get(username=data['username'], password=data['password'])
            except Exception:
                return HttpResponse('用户名密码错误')
            # 登录成功，需要将当前登录的用户保存记录下来(使用session存储数据，可以在服务端进行全局共享)
            request.session['user'] = user.serializable_value('username')
            return redirect('index')  # 重定向到首页
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

#注销
def log_off(request):
    request.session.clear()
    return redirect("index")

#首页
def index(request):
    """首页信息"""
    categories = Category.objects.all()
    return render(request, 'index.html', {'categories': categories, 'user': request.session.get('user')})


#商品列表
def goods_list(request):
    #搜索
    #获取关键字
    word = request.GET.get('q')
    if word != None:
        try:
            goods = Goods.objects.filter(name__contains=word)
            print(goods)
        except Exception:
            return HttpResponse('不存在商品')
        paginator = Paginator(goods,2)
        num = request.GET.get('num',1)
        page = paginator.page(num)
        return render(request, 'list.html', {'page':page, 'q':word})
    #搜索

    #1.获取分类id
    category_id = request.GET.get('category_id')
    #2.根据分类ID查询该分类下面的所有商品
    try:
        goods = Category.objects.get(pk=category_id).goods_set.all()
    except Exception:
        return HttpResponse('不存在商品')
    #3.初始化paginator分页类的对象
    paginator = Paginator(goods,2)#一页显示两个
    #4.获取页码
    num = request.GET.get('num', 1)
    #5.通过页面初始化当前页面的page对象
    page = paginator.page(num)
    #6.返回响应结果
    return render(request, 'list.html',{
        'page':page,
        'category_id':category_id,
         'user': request.session.get('user')
    })



# 商品详情页面
def detail(request):
    goods_id = request.GET.get('goods_id')
    goods = Goods.objects.get(pk=goods_id)
    return render(request, 'detail.html', {'goods': goods,
                                           'user': request.session.get('user')
                                           })

#购物车
def cart(request):
    cart = Cart.objects.get(user__username=request.session.get('user')).cartgoods_set.all()#条件语句都用双下划线
    num = cart.count()
    return render(request, 'cart.html',{'cart':cart,'num':num,
                                        'user': request.session.get('user')})


#添加购物车
def add_to_cart(request):
    #获取请求提交的商品id和数量
    goods_id = request.POST.get('goods_id')
    number = request.POST.get('number')
    try:
        """get_or_create返回（object,created）object是数据对象，
        created为布尔值，True为创建的数据，false为查询的数据"""
        #获取当前用户的购物车
        cart = Cart.objects.get_or_create(
            user__username=request.session.get('user'),
            defaults={'user_id':Shop.objects.get(username=request.session.get('user')).id}
            )
    except Exception:
        return HttpResponse('没有该用户')
    #给当前的用户的购物车添加或更新商品数量
    cartgoods = CartGoods.objects.update_or_create(cart=cart[0], goods_id=goods_id)
    cartgoods[0].number += int(number)
    cartgoods[0].save()
    # 返回结果
    if cartgoods[0]:
        return HttpResponse(cart[0].cartgoods_set.count())
    else:
        return HttpResponse('添加失败')

#购物车的删除
def shanchu(request):
    cart_goods_id=request.GET.get('cart_goods_id')
    goods_id = CartGoods.objects.filter(id=cart_goods_id).delete()
    return redirect('cart')

#结算
def placeorder(request):
    import json
    # 获取到被选中的商品的ID们
    cartgoods = json.loads(request.GET.get('data'))
    ids = []
    for item in cartgoods:          #循环购物车
        ids.append(item['cartgoods_id'])       #添加购物车商品id到ids空列表中
        CartGoods.objects.filter(pk=item['cartgoods_id']).update(number=item['num'])  #找到购物车商品id并更新数量
    date = CartGoods.objects.filter(id__in=ids)
    num = date.count()
    return render(request, 'place_order.html', {'num':num,'cartgoods': date,
                                                'user': request.session.get('user')})#大括号的内容传到模板里


#地址
def site(request):
    if request.method == 'POST':
        addressee = request.POST.get('addressee')  #收件人
        amply = request.POST.get('amply')          #详细地址
        zip = request.POST.get('zip')             #邮编
        phone = request.POST.get('phone')         #电话
        shop_id = Shop.objects.get(username=request.session.get('user')).id
        sites = Site.objects.create(addressee=addressee, amply=amply, zip=zip, phone=phone,shop_id=shop_id)
        if sites is not None:
            return redirect("site")
        else:
            return HttpResponse('添加失败')
    user_id = Shop.objects.get(username=request.session.get('user')).id
    silt = Site.objects.filter(shop_id=user_id)
    return render(request, 'user_center_site.html',{'user': request.session.get('user'),'silt':silt})


#个人信息
def message(request):
    user_id = Shop.objects.get(username=request.session.get('user')).id
    addr=Shop.objects.filter(id=user_id)          #在地址表查询用户id和登录用户id相同          #拿到键值，用户名
    add = Site.objects.filter(shop_id=user_id)
    return render(request, 'user_center_info.html', {'user': request.session.get('user'),
                                                     'addr':addr,
                                                     'add':add})


#把结算页面的数据放在orderinfo和ordergoods里
def create_order(request):
    use_id = Shop.objects.get(username=request.session.get('user')).id
    ordergoods_id = request.POST.get('ordergoods_id')
    aa = ordergoods_id.strip().split(',')
    cartgoods = CartGoods.objects.filter(id__in=aa)
    order = OrderInfo.objects.create(user_id=use_id)
    for i in cartgoods:
        ordergoods = OrderGoods.objects.create(order_info=order, goods=i.goods, number=i.number)
    if ordergoods:
        CartGoods.objects.filter(id__in=aa).delete()
    return render(request, 'user_center_order.html')

#展示全部订单页面
def order(request):
    user_id = Shop.objects.get(username=request.session.get('user')).id
    dingdans = OrderInfo.objects.filter(user_id=user_id)
    print(dingdans)
    paginator = Paginator(dingdans, 1)
    # 4. 获取页码
    num = request.GET.get('num', 1)
    # 5. 通过页码初始化当前页面的Page对象
    page = paginator.page(num)
    #6.返回响应结果
    return render(request, 'user_center_order.html', {
        'page': page,
        'user': request.session.get('user')
    })


# def info(request):
#     user_id = Shop.objects.get(username=request.session.get('user')).id
#     silt =Site.objects.filter(shop_id=user_id)
#     return render(request, 'user_center_info.html',{'siit':silt})



# 寄送到地址
def aaa(request):
    aaa = request.GET.get('aaa')
    car = Site.objects.filter(id=aaa)
    return render(request,'place_order.html',{'car':car})


#删除收货地址
def dell(request):
    add_id=request.GET.get('address')
    goods_id = Site.objects.filter(id=add_id).delete()
    return redirect('site')























# 登录
# def login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         try:
#             shop = Shop.objects.get(username=username, password=password)#查询
#         except Exception:
#             return HttpResponse('账号或密码不对')
#         return HttpResponse('登录成功')
#     else:
#         return render(request, 'login.html')



#页码设置
# def goods_list(request):
#     """商品列表请求"""
#     category_id = request.GET.get('category_id')#获得分类id
#     #从页面获取当前点击的页码（转成整数类型）
#     page = int(request.GET.get('page',1))
#     is_first = True
#     if page != 1:
#         is_first = False
#     #获取当前分类下的所有商品
#     goods = Category.objects.get(pk=category_id).goods_set.all()
#     #计算总页码
#     page = range(1, math.ceil(goods.count() /1)+1)
#     return render(request, 'list.html', {
#         'category_id': category_id,
#         'goods': goods[(page-1)*1:(page-1)*1+1],
#         'page': pages,
#         'is_first': is_first
#     })




# def text(request):
#     if request.method == 'POST':
#         form = Shop(request.POST)#实例化一个空的Form对象，并传入模板
#         if form.is_valid():#验证post提交的数据
#             print(form.cleaned_data)#可以得到表单数据的一个字典
#             return HttpResponse(form.cleaned_data)
#     else:
#         form = Shop()
#     return render(request, 'text.html', {'form': form})


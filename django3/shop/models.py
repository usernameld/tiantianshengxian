from django.db import models
from django.core import validators
import datetime


class Shop(models.Model):
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name
    username = models.CharField('用户名', unique=True, max_length=30,
                                validators=[validators.MinLengthValidator(
                                    limit_value=6, message='请输入6到20位用户名')])
    password = models.CharField('密码', max_length=32)
    address = models.CharField('地址', max_length=30, default='')
    email = models.EmailField('邮箱')


    def validate_unique(self, exclude=None):
        super().validate_unique(exclude=['username'])


class Category(models.Model):
    """分类信息"""
    class Meta:
        verbose_name = '分类信息'
        verbose_name_plural = verbose_name
    name = models.CharField('名称', max_length=10)
    icon = models.ImageField('图片样式', max_length=20)


def upload_thumb(instance, filename):  #图片的上传，模型实例对象，文件名
    return '{0}_{1}.png'.format(
         instance.id, datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%d%H%M%S')
     )


class Goods(models.Model):
    """商品信息"""
    class Meta:
        verbose_name = '商品信息'
        verbose_name_plural = verbose_name
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=30)
    price = models.DecimalField('价格', max_digits=5, decimal_places=2)
    thumb = models.ImageField('主图', upload_to=upload_thumb, null=True, blank=True)
    brief = models.CharField('简介', max_length=100, default=0)
    unit = models.IntegerField('单位', default=5)
    intorduce = models.CharField('介绍', max_length=100, default=1)


class Cart(models.Model):
    """购物车"""
    user = models.OneToOneField(Shop, on_delete=models.CASCADE)
    goods = models.ManyToManyField(Goods, through='CartGoods', through_fields=('cart', 'goods'))


class CartGoods(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    number = models.SmallIntegerField(default=0)


class Site(models.Model):
    class Meta:
        verbose_name = '编辑地址'
        verbose_name_plural = verbose_name
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)   #外键是父表写在子表里
    addressee = models.CharField('收件人', max_length=30)
    amply = models.CharField('详细地址', max_length=100)
    zip = models.IntegerField('邮编')
    phone = models.CharField('手机', max_length=11)


class OrderInfo(models.Model):
    """订单信息"""
    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name
    user = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name='用户')
    goods = models.ManyToManyField(Goods, through='OrderGoods', through_fields=('order_info', 'goods'), verbose_name='商品')
    pay_status = models.SmallIntegerField('支付状态', choices=[(0, '未付款'), (1, '付款中'), (2, '已付款')], default=0)
    shipping_status = models.SmallIntegerField('配送状态', choices=[(0, '未发货'), (1, '已发货'), (2, '已收货'), (3, '退货 ')], default=0)
    add_time = models.DateTimeField('创建时间', auto_now_add=True)


class OrderGoods(models.Model):
    """订单商品（订单和商品是多对多关系，该表是中间表）"""
    order_info = models.ForeignKey(OrderInfo, on_delete=models.CASCADE, verbose_name='订单ID')
    goods = models.ForeignKey(Goods, '商品ID')
    number = models.SmallIntegerField('数量')










# Create your models here.

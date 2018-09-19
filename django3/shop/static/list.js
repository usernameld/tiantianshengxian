/**
 * Created by gogo on 17-7-12.
 */
$(function () {
    //var add_url = $('#add_url').text();
    //var $show_count = $('#show_count');
    //$('.add_goods').click(function () {
    //    // 在列表也点击购物车
    //    //var goods_num = parseInt($show_count.text());
    //    //$show_count.text(goods_num + 1);
    //    //data = {'buy_num': 1};
    //    $.get(add_url, data, function (data) {
    //        if (data.code === 0) {
    //            alert('添加成功')
    //        }
    //    })
    //
    //});
    $('.add_goods').click(
                function(){
                    $.get("/shop_cart/add_cart/"+$(this).attr('gid'),function(res){
                            if(res.code==0){
                                $('#show_count').html(res.buy_num);
                                alert('添加成功')
                            }if(res.code==1){
                                alert('亲，登陆后才能有自己的购物车哦!');
                                location.href='/account/login'
                            } if(res.code==-2){
                                alert('参数错误')
                            }
                    })
                }
        )
});
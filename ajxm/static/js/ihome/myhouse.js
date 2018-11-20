//判断是否实名认证
$.get('/house/auth_myhouse',function(data){
    if(data.code == '200'){
        $('#houses-list').show();
        var html=template('house_list',{hlist:data.hlist});
        $('#houses-list').append(html);
    }else{
        $(".auth-warn").show();
    }
});
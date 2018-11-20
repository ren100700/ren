function logout() {
    $.ajax({
        url:'/user/logout/',
        type:'DELETE',
        dataType:'json',
        success: function(data){
            if(data.code == '200'){
                location.href='/user/login/';
            }
        },
        error: function(data){
            alert('请求失败')
        }
    });
}

$(document).ready(function(){
    $.ajax({
        url:'/user/user/',
        type:'GET',
        dataType:'json',
        success:function(data) {
            $('#user-avatar').attr('src',data.user.avatar);
            $('#user-name').html(data.user.name);
            $('#user-mobile').text(data.user.phone);
        },
        error:function(data){
            alert('请求失败')
        }
    });
});
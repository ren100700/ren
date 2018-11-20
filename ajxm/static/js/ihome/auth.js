function showSuccessMsg() {
    $('.popup_con').fadeIn('fast', function() {
        setTimeout(function(){
            $('.popup_con').fadeOut('fast',function(){}); 
        },1000) 
    });
}

$.get('/user/auth1/',function (data) {
    $('#real-name').val(data.id_name);
    $('#id-card').val(data.id_card);
    if(data.id_name!=null && data.id_name != '') {
        $('.btn-success').hide();
    }
});

$("#form-auth").submit(function(){
    $.ajax({
        url:'/user/auth1/',
        type:'PUT',
        dataType:'json',
        data:{id_name:$('#real-name').val(),id_card:$('#id-card').val()},
        success:function(data){
            if(data.code == '200'){
                $('.btn-success').hide();
                $('.error-msg').hide;
            }else{
                $('.error-msg').html('<i class="fa fa-exclamation-circle"></i>'+data.msg);
                $('.error-msg').show();
            }
        },
    })
    return false
});

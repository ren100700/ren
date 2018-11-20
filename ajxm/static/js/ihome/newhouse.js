function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

//查询地区、设施信息
$.get('/house/area_facility/',function (data) {
    //地区
    var area_html = ''
    for(var i=0; i<data.area.length; i++){
        area_html += '<option value="' + data.area[i].id + '">' + data.area[i].name + '</option>'
    }
    $('#area-id').html(area_html);
    //设施
    var facility_html_list = ''
    for(var i=0; i<data.facility.length; i++){
        var facility_html = '<li><div class="checkbox"><label><input type="checkbox" name="facility"'
        facility_html += ' value="' + data.facility[i].id + '">' + data.facility[i].name
        facility_html += '</label></div></li>'

        facility_html_list += facility_html
    }

    $('.house-facility-list').html(facility_html_list);

});


//为房屋表单绑定提交事件
$('#form-house-info').submit(function () {
    $('.error-msg text-center').hide();
    //验证内容是否填写
    alert($(this).serialize())
    $.post('/house/newhouse/',$(this).serialize(),function (data) {
        if(data.code== '200'){
            $('#form-house-info').hide();
            $('#form-house-image').show();
            $('#house-id').val(data.house_id);
        }else{
            $('.error-msg text-center').show().find('span').html(ret_map[data.code]);
        }
    });
    return false;
});

//为图片表单绑定事件
$('#form-house-image').submit(function () {
    alert('ok')
    $(this).ajaxSubmit({
        url: "/house/image/",
        type: "post",
        dataType: "json",
        success: function (data) {
            if (data.code == '200') {
                $('.house-image-cons').append('<img src="'+data.url+'"/>');
            }
        }
    });
    return false;
});
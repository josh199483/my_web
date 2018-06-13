/*
    作者: Howard
    日期: 2017/11/26

    說明:
        新增使用者、刪除使用者、修改使用者
*/

$(function () {
    // 新增使用者
    addUser();
    // 刪除使用者
    deleteUser();
    // 修改使用者
    updateUser();

    // 開始進行 ajax, 顯示讀取中, 畫面變黑
    $(document).ajaxStart(function () { // ajaxStart 
        $("#AJAX_READING").removeClass("hidden");
        $("#IMG_READING").removeClass("hidden");
    });


    // 結束 ajax, 畫面恢復原狀
    $(document).ajaxStop(function() { // ajaxStop 
        $("#AJAX_READING").addClass("hidden");
        $("#IMG_READING").addClass("hidden");
    });
});

// 2017/11/26 Howard
function addUser() { // 新增使用者
    $('#add_btn').click(function() {
        var userNameVal = $("#add_user_name").val();
        var passwordVal = $("#add_password").val();
        var confirmPasswordVal = $("#add_confirm_password").val();
        var userTypeVal = $("#add_user_type").val();
        var fullNameVal = $("#add_full_name").val();
        var phoneNumberVal = $("#add_phone_number").val();
        var emailVal = $("#add_email").val();
        $.ajax({
            type: 'POST',
            url: '/api/identity',
            data: {
                "userName":userNameVal,
                "password":passwordVal,
                "confirmPassword":confirmPasswordVal,
                "userType":userTypeVal,
                "fullName":fullNameVal,
                "phoneNumber":phoneNumberVal,
                "email":emailVal
            },
            cache: false
        }).done(function (msg) {
            if (msg.result != '新增成功') {
                swal(msg.result,'','error');
            }
            else {
                swal(msg.result,'','success');
                setTimeout(function(){location.reload();},1000);
            }
        });
    });
}

function deleteUser() { // 刪除使用者
    $('.delete_btn').click(function(ev) {
        var userNameVal = $(ev.target).parents("tr").children("td:first-child").html();
        swal({
            title: "確定刪除帳號?",
            text: "You will not be able to recover this account!",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "刪除!",
            closeOnConfirm: false
        },
        function () {
            $.ajax({
                type: 'DELETE',
                url: '/api/identity/' + userNameVal,
            }).done(function (msg) {
                swal(msg.result, '', 'success');
                setTimeout(function(){location.reload();},1000);
            });
        });
    });
}

function updateUser() { // 修改使用者
    $('.update_confirm_btn').click(function() {
        var userNameVal = $("#update_user_name").val();
        var passwordVal = $("#update_password").val();
        var confirmPasswordVal = $("#update_confirm_password").val();
        var userTypeVal = $("#update_user_type :selected").text();
        var fullNameVal = $("#update_full_name").val();
        var phoneNumberVal = $("#update_phone_number").val();
        var emailVal = $("#update_email").val();
        $.ajax({
            type: 'PUT',
            url: '/api/identity/' + userNameVal,
            data: {
                "password":passwordVal,
                "confirmPassword":confirmPasswordVal,
                "userType":userTypeVal,
                "fullName":fullNameVal,
                "phoneNumber":phoneNumberVal,
                "email":emailVal
            }
        }).done(function (msg) {
            if(msg.result != '更新成功') {
                swal(msg.result,'','error');
            }
            else {
                swal(msg.result, '','success');
                setTimeout(function(){location.reload();},1000);
            }
        });
    });
}
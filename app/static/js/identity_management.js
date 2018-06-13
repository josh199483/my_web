/*
    作者: Howard
    日期: 2017/11/26

    說明:
        查詢修改使用者、查詢使用者
*/

$(function () {
	// 查詢修改使用者
	selectUpdateUser();
	// 查詢使用者
	selectUser();
});

// 2017/11/26 Howard
function selectUpdateUser() { // 查詢修改使用者
	$(".update_btn").click(function (ev) {
		var data = $(ev.target).parents("tr").find("td");
		for (var i = 0; i < data.length; i++) {
			if (i === 1) {
				//使用者密碼，怎會放這??!!
				$(".update")[i].value = $(data[i]).html();
				$("#update_confirm_password").val($(data[i]).html());
			} else if (i === 2) {
				//使用者等級
				if($(data[i]).html() === 'admin'){
					$('#update_user_type').html('<option selected disabled>' + $(data[i]).text() + '</option>');
				}else {
					$('#update_user_type').html('<option selected disabled>' + $(data[i]).text() + '</option>');
					$('#update_user_type').append('<option>user</option><option>manager</option>');
				} 
			} else {
				try{
					$(".update")[i].value = $(data[i]).html();
				}catch(ex){
				}
			}
		}
	});
}

// 2017/11/26 Howard
function selectUser() { // 查詢使用者
	$("#user_table").click(function () {
		var path = '?';
		var userName = $("#search_user_name").val();
		var userType = $("#search_user_type").val();
		if (userName != '') {
			path += 'userName=' + userName + '&';
		}
		if (userType != 'all' && userType != null) {
			path += 'userType=' + userType + '&';
		}
		window.location.href = path;
	});
}

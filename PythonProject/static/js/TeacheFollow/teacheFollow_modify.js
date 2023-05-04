$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/TeacheFollow/update/" + $("#teacheFollow_followId_modify").val(),
		type : "get",
		data : {
			//followId : $("#teacheFollow_followId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (teacheFollow, response, status) {
			$.messager.progress("close");
			if (teacheFollow) { 
				$("#teacheFollow_followId_modify").val(teacheFollow.followId);
				$("#teacheFollow_followId_modify").validatebox({
					required : true,
					missingMessage : "请输入订阅id",
					editable: false
				});
				$("#teacheFollow_teacherObj_teacherNo_modify").combobox({
					url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"teacherNo",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#teacheFollow_teacherObj_teacherNo_modify").combobox("select", teacheFollow.teacherObjPri);
						//var data = $("#teacheFollow_teacherObj_teacherNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#teacheFollow_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						//}
					}
				});
				$("#teacheFollow_userObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#teacheFollow_userObj_user_name_modify").combobox("select", teacheFollow.userObjPri);
						//var data = $("#teacheFollow_userObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#teacheFollow_userObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#teacheFollow_followTime_modify").datetimebox({
					value: teacheFollow.followTime,
					required: true,
					showSeconds: true,
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#teacheFollowModifyButton").click(function(){ 
		if ($("#teacheFollowModifyForm").form("validate")) {
			$("#teacheFollowModifyForm").form({
			    url:"TeacheFollow/update/" + $("#teacheFollow_followId_modify").val(),
			    onSubmit: function(){
					if($("#teacheFollowEditForm").form("validate"))  {
	                	$.messager.progress({
							text : "正在提交数据中...",
						});
	                	return true;
	                } else {
	                    return false;
	                }
			    },
			    success:function(data){
			    	$.messager.progress("close");
                	var obj = jQuery.parseJSON(data);
                    if(obj.success){
                        $.messager.alert("消息","信息修改成功！");
                        $(".messager-window").css("z-index",10000);
                        //location.href="frontlist";
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    } 
			    }
			});
			//提交表单
			$("#teacheFollowModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

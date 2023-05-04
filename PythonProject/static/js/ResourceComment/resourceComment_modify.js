$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ResourceComment/update/" + $("#resourceComment_commentId_modify").val(),
		type : "get",
		data : {
			//commentId : $("#resourceComment_commentId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (resourceComment, response, status) {
			$.messager.progress("close");
			if (resourceComment) { 
				$("#resourceComment_commentId_modify").val(resourceComment.commentId);
				$("#resourceComment_commentId_modify").validatebox({
					required : true,
					missingMessage : "请输入评论id",
					editable: false
				});
				$("#resourceComment_resourceObj_resourceId_modify").combobox({
					url:"/Resource/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"resourceId",
					textField:"resourceName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#resourceComment_resourceObj_resourceId_modify").combobox("select", resourceComment.resourceObjPri);
						//var data = $("#resourceComment_resourceObj_resourceId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#resourceComment_resourceObj_resourceId_edit").combobox("select", data[0].resourceId);
						//}
					}
				});
				$("#resourceComment_teacherObj_teacherNo_modify").combobox({
					url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"teacherNo",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#resourceComment_teacherObj_teacherNo_modify").combobox("select", resourceComment.teacherObjPri);
						//var data = $("#resourceComment_teacherObj_teacherNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#resourceComment_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						//}
					}
				});
				$("#resourceComment_commentScore_modify").val(resourceComment.commentScore);
				$("#resourceComment_commentScore_modify").validatebox({
					required : true,
					validType : "number",
					missingMessage : "请输入评分",
					invalidMessage : "评分输入不对",
				});
				$("#resourceComment_content_modify").val(resourceComment.content);
				$("#resourceComment_content_modify").validatebox({
					required : true,
					missingMessage : "请输入评论内容",
				});
				$("#resourceComment_userObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#resourceComment_userObj_user_name_modify").combobox("select", resourceComment.userObjPri);
						//var data = $("#resourceComment_userObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#resourceComment_userObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#resourceComment_commentTime_modify").datetimebox({
					value: resourceComment.commentTime,
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

	$("#resourceCommentModifyButton").click(function(){ 
		if ($("#resourceCommentModifyForm").form("validate")) {
			$("#resourceCommentModifyForm").form({
			    url:"ResourceComment/update/" + $("#resourceComment_commentId_modify").val(),
			    onSubmit: function(){
					if($("#resourceCommentEditForm").form("validate"))  {
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
			$("#resourceCommentModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

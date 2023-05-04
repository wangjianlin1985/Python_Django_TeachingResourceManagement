$(function () {
	$("#resourceComment_commentScore").validatebox({
		required : true,
		validType : "number",
		missingMessage : '请输入评分',
		invalidMessage : '评分输入不对',
	});

	$("#resourceComment_content").validatebox({
		required : true, 
		missingMessage : '请输入评论内容',
	});

	$("#resourceComment_commentTime").datetimebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	//单击添加按钮
	$("#resourceCommentAddButton").click(function () {
		//验证表单 
		if(!$("#resourceCommentAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#resourceCommentAddForm").form({
			    url:"/ResourceComment/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#resourceCommentAddForm").form("validate"))  { 
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
                    //此处data={"Success":true}是字符串
                	var obj = jQuery.parseJSON(data); 
                    if(obj.success){ 
                        $.messager.alert("消息","保存成功！");
                        $(".messager-window").css("z-index",10000);
                        $("#resourceCommentAddForm").form("clear");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#resourceCommentAddForm").submit();
		}
	});

	//单击清空按钮
	$("#resourceCommentClearButton").click(function () { 
		//$("#resourceCommentAddForm").form("clear"); 
		location.reload()
	});
});

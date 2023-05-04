$(function () {
    //实例化老师介绍编辑器
    tinyMCE.init({
        selector: "#teacher_teacherDesc_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Teacher/update/" + $("#teacher_teacherNo_modify").val(),
		type : "get",
		data : {
			//teacherNo : $("#teacher_teacherNo_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (teacher, response, status) {
			$.messager.progress("close");
			if (teacher) { 
				$("#teacher_teacherNo_modify").val(teacher.teacherNo);
				$("#teacher_teacherNo_modify").validatebox({
					required : true,
					missingMessage : "请输入教师编号",
					editable: false
				});
				$("#teacher_password_modify").val(teacher.password);
				$("#teacher_password_modify").validatebox({
					required : true,
					missingMessage : "请输入登录密码",
				});
				$("#teacher_name_modify").val(teacher.name);
				$("#teacher_name_modify").validatebox({
					required : true,
					missingMessage : "请输入姓名",
				});
				$("#teacher_sex_modify").val(teacher.sex);
				$("#teacher_sex_modify").validatebox({
					required : true,
					missingMessage : "请输入性别",
				});
				$("#teacher_birthDate_modify").datebox({
					value: teacher.birthDate,
					required: true,
					showSeconds: true,
				});
				$("#teacher_teacherPhotoImgMod").attr("src", teacher.teacherPhoto);
				$("#teacher_zhicheng_modify").val(teacher.zhicheng);
				$("#teacher_zhicheng_modify").validatebox({
					required : true,
					missingMessage : "请输入职称",
				});
				$("#teacher_telephone_modify").val(teacher.telephone);
				$("#teacher_telephone_modify").validatebox({
					required : true,
					missingMessage : "请输入联系电话",
				});
				$("#teacher_comeDate_modify").datebox({
					value: teacher.comeDate,
					required: true,
					showSeconds: true,
				});
				$("#teacher_address_modify").val(teacher.address);
				tinyMCE.editors['teacher_teacherDesc_modify'].setContent(teacher.teacherDesc);
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#teacherModifyButton").click(function(){ 
		if ($("#teacherModifyForm").form("validate")) {
			$("#teacherModifyForm").form({
			    url:"Teacher/update/" + $("#teacher_teacherNo_modify").val(),
			    onSubmit: function(){
					if($("#teacherEditForm").form("validate"))  {
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
			$("#teacherModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

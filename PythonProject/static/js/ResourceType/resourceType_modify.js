$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/ResourceType/update/" + $("#resourceType_typeId_modify").val(),
		type : "get",
		data : {
			//typeId : $("#resourceType_typeId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (resourceType, response, status) {
			$.messager.progress("close");
			if (resourceType) { 
				$("#resourceType_typeId_modify").val(resourceType.typeId);
				$("#resourceType_typeId_modify").validatebox({
					required : true,
					missingMessage : "请输入类型id",
					editable: false
				});
				$("#resourceType_typeName_modify").val(resourceType.typeName);
				$("#resourceType_typeName_modify").validatebox({
					required : true,
					missingMessage : "请输入类型名称",
				});
				$("#resourceType_typeDesc_modify").val(resourceType.typeDesc);
				$("#resourceType_typeDesc_modify").validatebox({
					required : true,
					missingMessage : "请输入类型描述",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#resourceTypeModifyButton").click(function(){ 
		if ($("#resourceTypeModifyForm").form("validate")) {
			$("#resourceTypeModifyForm").form({
			    url:"ResourceType/update/" + $("#resourceType_typeId_modify").val(),
			    onSubmit: function(){
					if($("#resourceTypeEditForm").form("validate"))  {
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
			$("#resourceTypeModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

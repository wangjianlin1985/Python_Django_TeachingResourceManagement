$(function () {
    //实例化资源介绍编辑器
    tinyMCE.init({
        selector: "#resource_resourceDesc_modify",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Resource/update/" + $("#resource_resourceId_modify").val(),
		type : "get",
		data : {
			//resourceId : $("#resource_resourceId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (resource, response, status) {
			$.messager.progress("close");
			if (resource) { 
				$("#resource_resourceId_modify").val(resource.resourceId);
				$("#resource_resourceId_modify").validatebox({
					required : true,
					missingMessage : "请输入资源id",
					editable: false
				});
				$("#resource_resourceTypeObj_typeId_modify").combobox({
					url:"/ResourceType/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"typeId",
					textField:"typeName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#resource_resourceTypeObj_typeId_modify").combobox("select", resource.resourceTypeObjPri);
						//var data = $("#resource_resourceTypeObj_typeId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#resource_resourceTypeObj_typeId_edit").combobox("select", data[0].typeId);
						//}
					}
				});
				$("#resource_resourceName_modify").val(resource.resourceName);
				$("#resource_resourceName_modify").validatebox({
					required : true,
					missingMessage : "请输入资源名称",
				});
				$("#resource_resourcePhotoImgMod").attr("src", resource.resourcePhoto);
				tinyMCE.editors['resource_resourceDesc_modify'].setContent(resource.resourceDesc);
				if(resource.resourceFile.endsWith("file/NoFile.jpg")) $("#resource_resourceFileModA").html("暂无文件");
				$("#resource_resourceFileModA").attr("href", resource.resourceFile);
				$("#resource_teacherObj_teacherNo_modify").combobox({
					url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"teacherNo",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#resource_teacherObj_teacherNo_modify").combobox("select", resource.teacherObjPri);
						//var data = $("#resource_teacherObj_teacherNo_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#resource_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						//}
					}
				});
				$("#resource_uploadTime_modify").datetimebox({
					value: resource.uploadTime,
					required: true,
					showSeconds: true,
				});
				$("#resource_shenHeState_modify").val(resource.shenHeState);
				$("#resource_shenHeState_modify").validatebox({
					required : true,
					missingMessage : "请输入审核状态",
				});
				$("#resource_shenHeReply_modify").val(resource.shenHeReply);
				$("#resource_shenHeReply_modify").validatebox({
					required : true,
					missingMessage : "请输入审核回复",
				});
			} else {
				$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
				$(".messager-window").css("z-index",10000);
			}
		}
	});

  }

	$("#resourceModifyButton").click(function(){ 
		if ($("#resourceModifyForm").form("validate")) {
			$("#resourceModifyForm").form({
			    url:"Resource/update/" + $("#resource_resourceId_modify").val(),
			    onSubmit: function(){
					if($("#resourceEditForm").form("validate"))  {
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
			$("#resourceModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

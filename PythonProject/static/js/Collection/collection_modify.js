$(function () {
    setTimeout(ajaxModifyQuery,"100");
  function ajaxModifyQuery() {	
	$.ajax({
		url : "/Collection/update/" + $("#collection_collectionId_modify").val(),
		type : "get",
		data : {
			//collectionId : $("#collection_collectionId_modify").val(),
		},
		beforeSend : function () {
			$.messager.progress({
				text : "正在获取中...",
			});
		},
		success : function (collection, response, status) {
			$.messager.progress("close");
			if (collection) { 
				$("#collection_collectionId_modify").val(collection.collectionId);
				$("#collection_collectionId_modify").validatebox({
					required : true,
					missingMessage : "请输入收藏id",
					editable: false
				});
				$("#collection_resourceObj_resourceId_modify").combobox({
					url:"/Resource/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"resourceId",
					textField:"resourceName",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#collection_resourceObj_resourceId_modify").combobox("select", collection.resourceObjPri);
						//var data = $("#collection_resourceObj_resourceId_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#collection_resourceObj_resourceId_edit").combobox("select", data[0].resourceId);
						//}
					}
				});
				$("#collection_userObj_user_name_modify").combobox({
					url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
					method: "GET",
					valueField:"user_name",
					textField:"name",
					panelHeight: "auto",
					editable: false, //不允许手动输入 
					onLoadSuccess: function () { //数据加载完毕事件
						$("#collection_userObj_user_name_modify").combobox("select", collection.userObjPri);
						//var data = $("#collection_userObj_user_name_edit").combobox("getData"); 
						//if (data.length > 0) {
							//$("#collection_userObj_user_name_edit").combobox("select", data[0].user_name);
						//}
					}
				});
				$("#collection_collectTime_modify").datetimebox({
					value: collection.collectTime,
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

	$("#collectionModifyButton").click(function(){ 
		if ($("#collectionModifyForm").form("validate")) {
			$("#collectionModifyForm").form({
			    url:"Collection/update/" + $("#collection_collectionId_modify").val(),
			    onSubmit: function(){
					if($("#collectionEditForm").form("validate"))  {
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
			$("#collectionModifyForm").submit();
		} else {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		}
	});
});

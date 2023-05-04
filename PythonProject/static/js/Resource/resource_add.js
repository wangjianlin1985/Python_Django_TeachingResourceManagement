$(function () {
	//实例化资源介绍编辑器
    tinyMCE.init({
        selector: "#resource_resourceDesc",
        theme: 'advanced',
        language: "zh",
        strict_loading_mode: 1,
    });
	$("#resource_resourceName").validatebox({
		required : true, 
		missingMessage : '请输入资源名称',
	});

	$("#resource_uploadTime").datetimebox({
	    required : true, 
	    showSeconds: true,
	    editable: false
	});

	$("#resource_shenHeState").validatebox({
		required : true, 
		missingMessage : '请输入审核状态',
	});

	$("#resource_shenHeReply").validatebox({
		required : true, 
		missingMessage : '请输入审核回复',
	});

	//单击添加按钮
	$("#resourceAddButton").click(function () {
		if(tinyMCE.editors['resource_resourceDesc'].getContent() == "") {
			alert("请输入资源介绍");
			return;
		}
		//验证表单 
		if(!$("#resourceAddForm").form("validate")) {
			$.messager.alert("错误提示","你输入的信息还有错误！","warning");
			$(".messager-window").css("z-index",10000);
		} else {
			$("#resourceAddForm").form({
			    url:"/Resource/add",
				queryParams: {
			    	"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
			    onSubmit: function(){
					if($("#resourceAddForm").form("validate"))  { 
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
                        $("#resourceAddForm").form("clear");
                        tinyMCE.editors['resource_resourceDesc'].setContent("");
                    }else{
                        $.messager.alert("消息",obj.message);
                        $(".messager-window").css("z-index",10000);
                    }
			    }
			});
			//提交表单
			$("#resourceAddForm").submit();
		}
	});

	//单击清空按钮
	$("#resourceClearButton").click(function () { 
		//$("#resourceAddForm").form("clear"); 
		location.reload()
	});
});

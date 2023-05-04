var resource_manage_tool = null; 
$(function () { 
	initResourceManageTool(); //建立Resource管理对象
	resource_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#resource_manage").datagrid({
		url : '/Resource/list',
		queryParams: {
			"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
		},
		fit : true,
		fitColumns : true,
		striped : true,
		rownumbers : true,
		border : false,
		pagination : true,
		pageSize : 5,
		pageList : [5, 10, 15, 20, 25],
		pageNumber : 1,
		sortName : "resourceId",
		sortOrder : "desc",
		toolbar : "#resource_manage_tool",
		columns : [[
			{
				field : "resourceId",
				title : "资源id",
				width : 70,
			},
			{
				field : "resourceTypeObj",
				title : "资源类型",
				width : 140,
			},
			{
				field : "resourceName",
				title : "资源名称",
				width : 140,
			},
			{
				field : "resourcePhoto",
				title : "资源缩略图",
				width : "70px",
				height: "65px",
				formatter: function(val,row) {
					return "<img src='" + val + "' width='65px' height='55px' />";
				}
 			},
			{
				field : "resourceFile",
				title : "资料文件",
				width : "350px",
				formatter: function(val,row) {
 					if(val.endsWith("file/NoFile.jpg")) return "暂无文件";
					return "<a href='" + val + "' target='_blank' style='color:red;'>" + decodeURIComponent(val.substring(12)) + "</a>";
				}
 			},
			{
				field : "shenHeState",
				title : "审核状态",
				width : 140,
			},
			{
				field : "teacherObj",
				title : "上传老师",
				width : 140,
			},
			{
				field : "uploadTime",
				title : "上传日期",
				width : 140,
			},

			{
				field : "shenHeReply",
				title : "审核回复",
				width : 140,
			},
		]],
	});

	$("#resourceEditDiv").dialog({
		title : "修改管理",
		top: "10px",
		width : 1000,
		height : 600,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#resourceEditForm").form("validate")) {
					//验证表单 
					if(!$("#resourceEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#resourceEditForm").form({
						    url:"/Resource/update/" + $("#resource_resourceId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#resourceEditDiv").dialog("close");
			                        resource_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#resourceEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#resourceEditDiv").dialog("close");
				$("#resourceEditForm").form("reset"); 
			},
		}],
	});
});

function initResourceManageTool() {
	resource_manage_tool = {
		init: function() {
			$.ajax({
				url : "/ResourceType/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#resourceTypeObj_typeId_query").combobox({ 
					    valueField:"typeId",
					    textField:"typeName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{typeId:0,typeName:"不限制"});
					$("#resourceTypeObj_typeId_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/Teacher/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#teacherObj_teacherNo_query").combobox({ 
					    valueField:"teacherNo",
					    textField:"name",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{teacherNo:"",name:"不限制"});
					$("#teacherObj_teacherNo_query").combobox("loadData",data); 
				}
			});
			//实例化编辑器
			tinyMCE.init({
				selector: "#resource_resourceDesc_edit",
				theme: 'advanced',
				language: "zh",
				strict_loading_mode: 1,
			});
		},
		reload : function () {
			$("#resource_manage").datagrid("reload");
		},
		redo : function () {
			$("#resource_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#resource_manage").datagrid("options").queryParams;
			queryParams["resourceTypeObj.typeId"] = $("#resourceTypeObj_typeId_query").combobox("getValue");
			queryParams["resourceName"] = $("#resourceName").val();
			queryParams["teacherObj.teacherNo"] = $("#teacherObj_teacherNo_query").combobox("getValue");
			queryParams["uploadTime"] = $("#uploadTime").datebox("getValue"); 
			queryParams["shenHeState"] = $("#shenHeState").val();
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#resource_manage").datagrid("options").queryParams=queryParams; 
			$("#resource_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#resourceQueryForm").form({
			    url:"/Resource/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#resourceQueryForm").submit();
		},
		remove : function () {
			var rows = $("#resource_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var resourceIds = [];
						for (var i = 0; i < rows.length; i ++) {
							resourceIds.push(rows[i].resourceId);
						}
						$.ajax({
							type : "POST",
							url : "/Resource/deletes",
							data : {
								resourceIds : resourceIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#resource_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#resource_manage").datagrid("loaded");
									$("#resource_manage").datagrid("load");
									$("#resource_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#resource_manage").datagrid("loaded");
									$("#resource_manage").datagrid("load");
									$("#resource_manage").datagrid("unselectAll");
									$.messager.alert("消息",data.message);
								}
							},
						});
					}
				});
			} else {
				$.messager.alert("提示", "请选择要删除的记录！", "info");
			}
		},
		edit : function () {
			var rows = $("#resource_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/Resource/update/" + rows[0].resourceId,
					type : "get",
					data : {
						//resourceId : rows[0].resourceId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (resource, response, status) {
						$.messager.progress("close");
						if (resource) { 
							$("#resourceEditDiv").dialog("open");
							$("#resource_resourceId_edit").val(resource.resourceId);
							$("#resource_resourceId_edit").validatebox({
								required : true,
								missingMessage : "请输入资源id",
								editable: false
							});
							$("#resource_resourceTypeObj_typeId_edit").combobox({
								url:"/ResourceType/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"typeId",
							    textField:"typeName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#resource_resourceTypeObj_typeId_edit").combobox("select", resource.resourceTypeObjPri);
									//var data = $("#resource_resourceTypeObj_typeId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#resource_resourceTypeObj_typeId_edit").combobox("select", data[0].typeId);
						            //}
								}
							});
							$("#resource_resourceName_edit").val(resource.resourceName);
							$("#resource_resourceName_edit").validatebox({
								required : true,
								missingMessage : "请输入资源名称",
							});
							$("#resource_resourcePhotoImg").attr("src", resource.resourcePhoto);
							tinyMCE.editors['resource_resourceDesc_edit'].setContent(resource.resourceDesc);
							if(resource.resourceFile.endsWith("file/NoFile.jpg")) $("#resource_resourceFileA").html("暂无文件");
							else $("#resource_resourceFileA").html(decodeURIComponent(resource.resourceFile.substring(12)));
							$("#resource_resourceFileA").attr("href", resource.resourceFile);
							$("#resource_teacherObj_teacherNo_edit").combobox({
								url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"teacherNo",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#resource_teacherObj_teacherNo_edit").combobox("select", resource.teacherObjPri);
									//var data = $("#resource_teacherObj_teacherNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#resource_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						            //}
								}
							});
							$("#resource_uploadTime_edit").datetimebox({
								value: resource.uploadTime,
							    required: true,
							    showSeconds: true,
							});
							$("#resource_shenHeState_edit").val(resource.shenHeState);
							$("#resource_shenHeState_edit").validatebox({
								required : true,
								missingMessage : "请输入审核状态",
							});
							$("#resource_shenHeReply_edit").val(resource.shenHeReply);
							$("#resource_shenHeReply_edit").validatebox({
								required : true,
								missingMessage : "请输入审核回复",
							});
						} else {
							$.messager.alert("获取失败！", "未知错误导致失败，请重试！", "warning");
						}
					}
				});
			} else if (rows.length == 0) {
				$.messager.alert("警告操作！", "编辑记录至少选定一条数据！", "warning");
			}
		},
	};
}

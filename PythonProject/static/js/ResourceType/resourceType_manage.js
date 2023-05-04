var resourceType_manage_tool = null; 
$(function () { 
	initResourceTypeManageTool(); //建立ResourceType管理对象
	resourceType_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#resourceType_manage").datagrid({
		url : '/ResourceType/list',
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
		sortName : "typeId",
		sortOrder : "desc",
		toolbar : "#resourceType_manage_tool",
		columns : [[
			{
				field : "typeId",
				title : "类型id",
				width : 70,
			},
			{
				field : "typeName",
				title : "类型名称",
				width : 140,
			},
			{
				field : "typeDesc",
				title : "类型描述",
				width : 140,
			},
		]],
	});

	$("#resourceTypeEditDiv").dialog({
		title : "修改管理",
		top: "50px",
		width : 700,
		height : 515,
		modal : true,
		closed : true,
		iconCls : "icon-edit-new",
		buttons : [{
			text : "提交",
			iconCls : "icon-edit-new",
			handler : function () {
				if ($("#resourceTypeEditForm").form("validate")) {
					//验证表单 
					if(!$("#resourceTypeEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#resourceTypeEditForm").form({
						    url:"/ResourceType/update/" + $("#resourceType_typeId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#resourceTypeEditDiv").dialog("close");
			                        resourceType_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#resourceTypeEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#resourceTypeEditDiv").dialog("close");
				$("#resourceTypeEditForm").form("reset"); 
			},
		}],
	});
});

function initResourceTypeManageTool() {
	resourceType_manage_tool = {
		init: function() {
		},
		reload : function () {
			$("#resourceType_manage").datagrid("reload");
		},
		redo : function () {
			$("#resourceType_manage").datagrid("unselectAll");
		},
		search: function() {
			$("#resourceType_manage").datagrid("options").queryParams=queryParams; 
			$("#resourceType_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#resourceTypeQueryForm").form({
			    url:"/ResourceType/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#resourceTypeQueryForm").submit();
		},
		remove : function () {
			var rows = $("#resourceType_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var typeIds = [];
						for (var i = 0; i < rows.length; i ++) {
							typeIds.push(rows[i].typeId);
						}
						$.ajax({
							type : "POST",
							url : "/ResourceType/deletes",
							data : {
								typeIds : typeIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#resourceType_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#resourceType_manage").datagrid("loaded");
									$("#resourceType_manage").datagrid("load");
									$("#resourceType_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#resourceType_manage").datagrid("loaded");
									$("#resourceType_manage").datagrid("load");
									$("#resourceType_manage").datagrid("unselectAll");
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
			var rows = $("#resourceType_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/ResourceType/update/" + rows[0].typeId,
					type : "get",
					data : {
						//typeId : rows[0].typeId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (resourceType, response, status) {
						$.messager.progress("close");
						if (resourceType) { 
							$("#resourceTypeEditDiv").dialog("open");
							$("#resourceType_typeId_edit").val(resourceType.typeId);
							$("#resourceType_typeId_edit").validatebox({
								required : true,
								missingMessage : "请输入类型id",
								editable: false
							});
							$("#resourceType_typeName_edit").val(resourceType.typeName);
							$("#resourceType_typeName_edit").validatebox({
								required : true,
								missingMessage : "请输入类型名称",
							});
							$("#resourceType_typeDesc_edit").val(resourceType.typeDesc);
							$("#resourceType_typeDesc_edit").validatebox({
								required : true,
								missingMessage : "请输入类型描述",
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

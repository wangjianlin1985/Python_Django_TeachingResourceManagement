var collection_manage_tool = null; 
$(function () { 
	initCollectionManageTool(); //建立Collection管理对象
	collection_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#collection_manage").datagrid({
		url : '/Collection/list',
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
		sortName : "collectionId",
		sortOrder : "desc",
		toolbar : "#collection_manage_tool",
		columns : [[
			{
				field : "collectionId",
				title : "收藏id",
				width : 70,
			},
			{
				field : "resourceObj",
				title : "收藏的资源",
				width : 140,
			},
			{
				field : "userObj",
				title : "收藏用户",
				width : 140,
			},
			{
				field : "collectTime",
				title : "收藏时间",
				width : 140,
			},
		]],
	});

	$("#collectionEditDiv").dialog({
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
				if ($("#collectionEditForm").form("validate")) {
					//验证表单 
					if(!$("#collectionEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#collectionEditForm").form({
						    url:"/Collection/update/" + $("#collection_collectionId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#collectionEditDiv").dialog("close");
			                        collection_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#collectionEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#collectionEditDiv").dialog("close");
				$("#collectionEditForm").form("reset"); 
			},
		}],
	});
});

function initCollectionManageTool() {
	collection_manage_tool = {
		init: function() {
			$.ajax({
				url : "/Resource/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#resourceObj_resourceId_query").combobox({ 
					    valueField:"resourceId",
					    textField:"resourceName",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{resourceId:0,resourceName:"不限制"});
					$("#resourceObj_resourceId_query").combobox("loadData",data); 
				}
			});
			$.ajax({
				url : "/UserInfo/listAll",
				data: {
					"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
				},
				type : "get",
				success : function (data, response, status) {
					$("#userObj_user_name_query").combobox({ 
					    valueField:"user_name",
					    textField:"name",
					    panelHeight: "200px",
				        editable: false, //不允许手动输入 
					});
					data.splice(0,0,{user_name:"",name:"不限制"});
					$("#userObj_user_name_query").combobox("loadData",data); 
				}
			});
		},
		reload : function () {
			$("#collection_manage").datagrid("reload");
		},
		redo : function () {
			$("#collection_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#collection_manage").datagrid("options").queryParams;
			queryParams["resourceObj.resourceId"] = $("#resourceObj_resourceId_query").combobox("getValue");
			queryParams["userObj.user_name"] = $("#userObj_user_name_query").combobox("getValue");
			queryParams["collectTime"] = $("#collectTime").datebox("getValue"); 
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#collection_manage").datagrid("options").queryParams=queryParams; 
			$("#collection_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#collectionQueryForm").form({
			    url:"/Collection/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#collectionQueryForm").submit();
		},
		remove : function () {
			var rows = $("#collection_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var collectionIds = [];
						for (var i = 0; i < rows.length; i ++) {
							collectionIds.push(rows[i].collectionId);
						}
						$.ajax({
							type : "POST",
							url : "/Collection/deletes",
							data : {
								collectionIds : collectionIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#collection_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#collection_manage").datagrid("loaded");
									$("#collection_manage").datagrid("load");
									$("#collection_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#collection_manage").datagrid("loaded");
									$("#collection_manage").datagrid("load");
									$("#collection_manage").datagrid("unselectAll");
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
			var rows = $("#collection_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/Collection/update/" + rows[0].collectionId,
					type : "get",
					data : {
						//collectionId : rows[0].collectionId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (collection, response, status) {
						$.messager.progress("close");
						if (collection) { 
							$("#collectionEditDiv").dialog("open");
							$("#collection_collectionId_edit").val(collection.collectionId);
							$("#collection_collectionId_edit").validatebox({
								required : true,
								missingMessage : "请输入收藏id",
								editable: false
							});
							$("#collection_resourceObj_resourceId_edit").combobox({
								url:"/Resource/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"resourceId",
							    textField:"resourceName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#collection_resourceObj_resourceId_edit").combobox("select", collection.resourceObjPri);
									//var data = $("#collection_resourceObj_resourceId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#collection_resourceObj_resourceId_edit").combobox("select", data[0].resourceId);
						            //}
								}
							});
							$("#collection_userObj_user_name_edit").combobox({
								url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"user_name",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#collection_userObj_user_name_edit").combobox("select", collection.userObjPri);
									//var data = $("#collection_userObj_user_name_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#collection_userObj_user_name_edit").combobox("select", data[0].user_name);
						            //}
								}
							});
							$("#collection_collectTime_edit").datetimebox({
								value: collection.collectTime,
							    required: true,
							    showSeconds: true,
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

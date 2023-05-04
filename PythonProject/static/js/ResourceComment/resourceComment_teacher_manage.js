var resourceComment_manage_tool = null; 
$(function () { 
	initResourceCommentManageTool(); //建立ResourceComment管理对象
	resourceComment_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#resourceComment_manage").datagrid({
		url : '/ResourceComment/teacherList',
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
		sortName : "commentId",
		sortOrder : "desc",
		toolbar : "#resourceComment_manage_tool",
		columns : [[
			{
				field : "commentId",
				title : "评论id",
				width : 70,
			},
			{
				field : "resourceObj",
				title : "被评资源",
				width : 140,
			},
			{
				field : "commentScore",
				title : "评分",
				width : 70,
			},
			{
				field : "content",
				title : "评论内容",
				width : 140,
			},
			{
				field : "userObj",
				title : "评论用户",
				width : 140,
			},
			{
				field : "commentTime",
				title : "评论时间",
				width : 140,
			},
		]],
	});

	$("#resourceCommentEditDiv").dialog({
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
				if ($("#resourceCommentEditForm").form("validate")) {
					//验证表单 
					if(!$("#resourceCommentEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#resourceCommentEditForm").form({
						    url:"/ResourceComment/update/" + $("#resourceComment_commentId_edit").val(),
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
						    	console.log(data);
			                	var obj = jQuery.parseJSON(data);
			                    if(obj.success){
			                        $.messager.alert("消息","信息修改成功！");
			                        $("#resourceCommentEditDiv").dialog("close");
			                        resourceComment_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#resourceCommentEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#resourceCommentEditDiv").dialog("close");
				$("#resourceCommentEditForm").form("reset"); 
			},
		}],
	});
});

function initResourceCommentManageTool() {
	resourceComment_manage_tool = {
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
			$("#resourceComment_manage").datagrid("reload");
		},
		redo : function () {
			$("#resourceComment_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#resourceComment_manage").datagrid("options").queryParams;
			queryParams["resourceObj.resourceId"] = $("#resourceObj_resourceId_query").combobox("getValue");
			queryParams["teacherObj.teacherNo"] = $("#teacherObj_teacherNo_query").combobox("getValue");
			queryParams["userObj.user_name"] = $("#userObj_user_name_query").combobox("getValue");
			queryParams["commentTime"] = $("#commentTime").datebox("getValue"); 
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#resourceComment_manage").datagrid("options").queryParams=queryParams; 
			$("#resourceComment_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#resourceCommentQueryForm").form({
			    url:"/ResourceComment/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#resourceCommentQueryForm").submit();
		},
		remove : function () {
			var rows = $("#resourceComment_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var commentIds = [];
						for (var i = 0; i < rows.length; i ++) {
							commentIds.push(rows[i].commentId);
						}
						$.ajax({
							type : "POST",
							url : "/ResourceComment/deletes",
							data : {
								commentIds : commentIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#resourceComment_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#resourceComment_manage").datagrid("loaded");
									$("#resourceComment_manage").datagrid("load");
									$("#resourceComment_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#resourceComment_manage").datagrid("loaded");
									$("#resourceComment_manage").datagrid("load");
									$("#resourceComment_manage").datagrid("unselectAll");
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
			var rows = $("#resourceComment_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/ResourceComment/update/" + rows[0].commentId,
					type : "get",
					data : {
						//commentId : rows[0].commentId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (resourceComment, response, status) {
						$.messager.progress("close");
						if (resourceComment) { 
							$("#resourceCommentEditDiv").dialog("open");
							$("#resourceComment_commentId_edit").val(resourceComment.commentId);
							$("#resourceComment_commentId_edit").validatebox({
								required : true,
								missingMessage : "请输入评论id",
								editable: false
							});
							$("#resourceComment_resourceObj_resourceId_edit").combobox({
								url:"/Resource/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"resourceId",
							    textField:"resourceName",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#resourceComment_resourceObj_resourceId_edit").combobox("select", resourceComment.resourceObjPri);
									//var data = $("#resourceComment_resourceObj_resourceId_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#resourceComment_resourceObj_resourceId_edit").combobox("select", data[0].resourceId);
						            //}
								}
							});
							$("#resourceComment_teacherObj_teacherNo_edit").combobox({
								url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"teacherNo",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#resourceComment_teacherObj_teacherNo_edit").combobox("select", resourceComment.teacherObjPri);
									//var data = $("#resourceComment_teacherObj_teacherNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#resourceComment_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						            //}
								}
							});
							$("#resourceComment_commentScore_edit").val(resourceComment.commentScore);
							$("#resourceComment_commentScore_edit").validatebox({
								required : true,
								validType : "number",
								missingMessage : "请输入评分",
								invalidMessage : "评分输入不对",
							});
							$("#resourceComment_content_edit").val(resourceComment.content);
							$("#resourceComment_content_edit").validatebox({
								required : true,
								missingMessage : "请输入评论内容",
							});
							$("#resourceComment_userObj_user_name_edit").combobox({
								url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"user_name",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#resourceComment_userObj_user_name_edit").combobox("select", resourceComment.userObjPri);
									//var data = $("#resourceComment_userObj_user_name_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#resourceComment_userObj_user_name_edit").combobox("select", data[0].user_name);
						            //}
								}
							});
							$("#resourceComment_commentTime_edit").datetimebox({
								value: resourceComment.commentTime,
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

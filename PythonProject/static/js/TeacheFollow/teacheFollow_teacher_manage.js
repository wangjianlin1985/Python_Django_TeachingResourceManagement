var teacheFollow_manage_tool = null; 
$(function () { 
	initTeacheFollowManageTool(); //建立TeacheFollow管理对象
	teacheFollow_manage_tool.init(); //如果需要通过下拉框查询，首先初始化下拉框的值
	$("#teacheFollow_manage").datagrid({
		url : '/TeacheFollow/teacherList',
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
		sortName : "followId",
		sortOrder : "desc",
		toolbar : "#teacheFollow_manage_tool",
		columns : [[
			{
				field : "followId",
				title : "订阅id",
				width : 70,
			},

			{
				field : "userObj",
				title : "订阅人",
				width : 140,
			},
			{
				field : "followTime",
				title : "订阅时间",
				width : 140,
			},
		]],
	});

	$("#teacheFollowEditDiv").dialog({
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
				if ($("#teacheFollowEditForm").form("validate")) {
					//验证表单 
					if(!$("#teacheFollowEditForm").form("validate")) {
						$.messager.alert("错误提示","你输入的信息还有错误！","warning");
					} else {
						$("#teacheFollowEditForm").form({
						    url:"/TeacheFollow/update/" + $("#teacheFollow_followId_edit").val(),
						    onSubmit: function(){
								if($("#teacheFollowEditForm").form("validate"))  {
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
			                        $("#teacheFollowEditDiv").dialog("close");
			                        teacheFollow_manage_tool.reload();
			                    }else{
			                        $.messager.alert("消息",obj.message);
			                    } 
						    }
						});
						//提交表单
						$("#teacheFollowEditForm").submit();
					}
				}
			},
		},{
			text : "取消",
			iconCls : "icon-redo",
			handler : function () {
				$("#teacheFollowEditDiv").dialog("close");
				$("#teacheFollowEditForm").form("reset"); 
			},
		}],
	});
});

function initTeacheFollowManageTool() {
	teacheFollow_manage_tool = {
		init: function() {
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
			$("#teacheFollow_manage").datagrid("reload");
		},
		redo : function () {
			$("#teacheFollow_manage").datagrid("unselectAll");
		},
		search: function() {
			var queryParams = $("#teacheFollow_manage").datagrid("options").queryParams;
			queryParams["teacherObj.teacherNo"] = $("#teacherObj_teacherNo_query").combobox("getValue");
			queryParams["userObj.user_name"] = $("#userObj_user_name_query").combobox("getValue");
			queryParams["followTime"] = $("#followTime").datebox("getValue"); 
			queryParams["csrfmiddlewaretoken"] = $('input[name="csrfmiddlewaretoken"]').val();
			$("#teacheFollow_manage").datagrid("options").queryParams=queryParams; 
			$("#teacheFollow_manage").datagrid("load");
		},
		exportExcel: function() {
			$("#teacheFollowQueryForm").form({
			    url:"/TeacheFollow/OutToExcel?csrfmiddlewaretoken" + $('input[name="csrfmiddlewaretoken"]').val(),
			});
			//提交表单
			$("#teacheFollowQueryForm").submit();
		},
		remove : function () {
			var rows = $("#teacheFollow_manage").datagrid("getSelections");
			if (rows.length > 0) {
				$.messager.confirm("确定操作", "您正在要删除所选的记录吗？", function (flag) {
					if (flag) {
						var followIds = [];
						for (var i = 0; i < rows.length; i ++) {
							followIds.push(rows[i].followId);
						}
						$.ajax({
							type : "POST",
							url : "/TeacheFollow/deletes",
							data : {
								followIds : followIds.join(","),
								"csrfmiddlewaretoken": $('input[name="csrfmiddlewaretoken"]').val()
							},
							beforeSend : function () {
								$("#teacheFollow_manage").datagrid("loading");
							},
							success : function (data) {
								if (data.success) {
									$("#teacheFollow_manage").datagrid("loaded");
									$("#teacheFollow_manage").datagrid("load");
									$("#teacheFollow_manage").datagrid("unselectAll");
									$.messager.show({
										title : "提示",
										msg : data.message
									});
								} else {
									$("#teacheFollow_manage").datagrid("loaded");
									$("#teacheFollow_manage").datagrid("load");
									$("#teacheFollow_manage").datagrid("unselectAll");
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
			var rows = $("#teacheFollow_manage").datagrid("getSelections");
			if (rows.length > 1) {
				$.messager.alert("警告操作！", "编辑记录只能选定一条数据！", "warning");
			} else if (rows.length == 1) {
				$.ajax({
					url : "/TeacheFollow/update/" + rows[0].followId,
					type : "get",
					data : {
						//followId : rows[0].followId,
					},
					beforeSend : function () {
						$.messager.progress({
							text : "正在获取中...",
						});
					},
					success : function (teacheFollow, response, status) {
						$.messager.progress("close");
						if (teacheFollow) { 
							$("#teacheFollowEditDiv").dialog("open");
							$("#teacheFollow_followId_edit").val(teacheFollow.followId);
							$("#teacheFollow_followId_edit").validatebox({
								required : true,
								missingMessage : "请输入订阅id",
								editable: false
							});
							$("#teacheFollow_teacherObj_teacherNo_edit").combobox({
								url:"/Teacher/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"teacherNo",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#teacheFollow_teacherObj_teacherNo_edit").combobox("select", teacheFollow.teacherObjPri);
									//var data = $("#teacheFollow_teacherObj_teacherNo_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#teacheFollow_teacherObj_teacherNo_edit").combobox("select", data[0].teacherNo);
						            //}
								}
							});
							$("#teacheFollow_userObj_user_name_edit").combobox({
								url:"/UserInfo/listAll?csrfmiddlewaretoken=" + $('input[name="csrfmiddlewaretoken"]').val(),
								method: "GET",
							    valueField:"user_name",
							    textField:"name",
							    panelHeight: "auto",
						        editable: false, //不允许手动输入 
						        onLoadSuccess: function () { //数据加载完毕事件
									$("#teacheFollow_userObj_user_name_edit").combobox("select", teacheFollow.userObjPri);
									//var data = $("#teacheFollow_userObj_user_name_edit").combobox("getData"); 
						            //if (data.length > 0) {
						                //$("#teacheFollow_userObj_user_name_edit").combobox("select", data[0].user_name);
						            //}
								}
							});
							$("#teacheFollow_followTime_edit").datetimebox({
								value: teacheFollow.followTime,
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

from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ResourceComment.models import ResourceComment
from apps.Resource.models import Resource
from apps.Teacher.models import Teacher
from apps.UserInfo.models import UserInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台资源评论添加
    def get(self,request):
        resources = Resource.objects.all()  # 获取所有教学资源
        teachers = Teacher.objects.all()  # 获取所有老师
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'resources': resources,
            'teachers': teachers,
            'userInfos': userInfos,
        }

        # 使用模板
        return render(request, 'ResourceComment/resourceComment_frontAdd.html', context)

    def post(self, request):
        resourceComment = ResourceComment() # 新建一个资源评论对象然后获取参数
        resourceComment.resourceObj = Resource.objects.get(resourceId=request.POST.get('resourceComment.resourceObj.resourceId'))
        resourceComment.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resourceComment.teacherObj.teacherNo'))
        resourceComment.commentScore = float(request.POST.get('resourceComment.commentScore'))
        resourceComment.content = request.POST.get('resourceComment.content')
        resourceComment.userObj = UserInfo.objects.get(user_name=request.POST.get('resourceComment.userObj.user_name'))
        resourceComment.commentTime = request.POST.get('resourceComment.commentTime')
        resourceComment.save() # 保存资源评论信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})



class FrontUserAddView(BaseView):  # 前台资源评论添加
    def post(self, request):
        user_name = request.session.get('user_name')
        if user_name == None:
            return JsonResponse({'success': False, 'message': '请先登录网站'})

        resourceComment = ResourceComment() # 新建一个资源评论对象然后获取参数
        resourceComment.resourceObj = Resource.objects.get(resourceId=request.POST.get('resourceComment.resourceObj.resourceId'))
        resourceComment.teacherObj = resourceComment.resourceObj.teacherObj
        resourceComment.commentScore = float(request.POST.get('resourceComment.commentScore'))
        resourceComment.content = request.POST.get('resourceComment.content')
        resourceComment.userObj = UserInfo.objects.get(user_name=user_name)
        import datetime
        resourceComment.commentTime =  str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        resourceComment.save() # 保存资源评论信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})




class FrontModifyView(BaseView):  # 前台修改资源评论
    def get(self, request, commentId):
        context = {'commentId': commentId}
        return render(request, 'ResourceComment/resourceComment_frontModify.html', context)


class FrontListView(BaseView):  # 前台资源评论查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        commentTime = self.getStrParam(request, 'commentTime')
        # 然后条件组合查询过滤
        resourceComments = ResourceComment.objects.all().order_by('-commentTime')
        if resourceObj_resourceId != '0':
            resourceComments = resourceComments.filter(resourceObj=resourceObj_resourceId)
        if teacherObj_teacherNo != '':
            resourceComments = resourceComments.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            resourceComments = resourceComments.filter(userObj=userObj_user_name)
        if commentTime != '':
            resourceComments = resourceComments.filter(commentTime__contains=commentTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(resourceComments, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceComments_page = self.paginator.page(self.currentPage)

        # 获取所有教学资源
        resources = Resource.objects.all()
        # 获取所有老师
        teachers = Teacher.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'resources': resources,
            'teachers': teachers,
            'userInfos': userInfos,
            'resourceComments_page': resourceComments_page,
            'resourceObj_resourceId': int(resourceObj_resourceId),
            'teacherObj_teacherNo': teacherObj_teacherNo,
            'userObj_user_name': userObj_user_name,
            'commentTime': commentTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ResourceComment/resourceComment_frontquery_result.html', context)


class FrontUserListView(BaseView):  # 前台资源评论查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = request.session.get('user_name')
        commentTime = self.getStrParam(request, 'commentTime')
        # 然后条件组合查询过滤
        resourceComments = ResourceComment.objects.all().order_by('-commentTime')
        if resourceObj_resourceId != '0':
            resourceComments = resourceComments.filter(resourceObj=resourceObj_resourceId)
        if teacherObj_teacherNo != '':
            resourceComments = resourceComments.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            resourceComments = resourceComments.filter(userObj=userObj_user_name)
        if commentTime != '':
            resourceComments = resourceComments.filter(commentTime__contains=commentTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(resourceComments, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceComments_page = self.paginator.page(self.currentPage)

        # 获取所有教学资源
        resources = Resource.objects.all()
        # 获取所有老师
        teachers = Teacher.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'resources': resources,
            'teachers': teachers,
            'userInfos': userInfos,
            'resourceComments_page': resourceComments_page,
            'resourceObj_resourceId': int(resourceObj_resourceId),
            'teacherObj_teacherNo': teacherObj_teacherNo,
            'userObj_user_name': userObj_user_name,
            'commentTime': commentTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ResourceComment/resourceComment_userFrontquery_result.html', context)


class FrontShowView(View):  # 前台显示资源评论详情页
    def get(self, request, commentId):
        # 查询需要显示的资源评论对象
        resourceComment = ResourceComment.objects.get(commentId=commentId)
        context = {
            'resourceComment': resourceComment
        }
        # 渲染模板显示
        return render(request, 'ResourceComment/resourceComment_frontshow.html', context)


class ListAllView(View): # 前台查询所有资源评论
    def get(self,request):
        resourceComments = ResourceComment.objects.all()
        resourceCommentList = []
        for resourceComment in resourceComments:
            resourceCommentObj = {
                'commentId': resourceComment.commentId,
                'content': resourceComment.content,
            }
            resourceCommentList.append(resourceCommentObj)
        return JsonResponse(resourceCommentList, safe=False)


class UpdateView(BaseView):  # Ajax方式资源评论更新
    def get(self, request, commentId):
        # GET方式请求查询资源评论对象并返回资源评论json格式
        resourceComment = ResourceComment.objects.get(commentId=commentId)
        return JsonResponse(resourceComment.getJsonObj())

    def post(self, request, commentId):
        # POST方式提交资源评论修改信息更新到数据库
        resourceComment = ResourceComment.objects.get(commentId=commentId)
        resourceComment.resourceObj = Resource.objects.get(resourceId=request.POST.get('resourceComment.resourceObj.resourceId'))
        resourceComment.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resourceComment.teacherObj.teacherNo'))
        resourceComment.commentScore = float(request.POST.get('resourceComment.commentScore'))
        resourceComment.content = request.POST.get('resourceComment.content')
        resourceComment.userObj = UserInfo.objects.get(user_name=request.POST.get('resourceComment.userObj.user_name'))
        resourceComment.commentTime = request.POST.get('resourceComment.commentTime')
        resourceComment.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台资源评论添加
    def get(self,request):
        resources = Resource.objects.all()  # 获取所有教学资源
        teachers = Teacher.objects.all()  # 获取所有老师
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'resources': resources,
            'teachers': teachers,
            'userInfos': userInfos,
        }

        # 渲染显示模板界面
        return render(request, 'ResourceComment/resourceComment_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        resourceComment = ResourceComment() # 新建一个资源评论对象然后获取参数
        resourceComment.resourceObj = Resource.objects.get(resourceId=request.POST.get('resourceComment.resourceObj.resourceId'))
        resourceComment.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resourceComment.teacherObj.teacherNo'))
        resourceComment.commentScore = float(request.POST.get('resourceComment.commentScore'))
        resourceComment.content = request.POST.get('resourceComment.content')
        resourceComment.userObj = UserInfo.objects.get(user_name=request.POST.get('resourceComment.userObj.user_name'))
        resourceComment.commentTime = request.POST.get('resourceComment.commentTime')
        resourceComment.save() # 保存资源评论信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新资源评论
    def get(self, request, commentId):
        context = {'commentId': commentId}
        return render(request, 'ResourceComment/resourceComment_modify.html', context)


class ListView(BaseView):  # 后台资源评论列表
    def get(self, request):
        # 使用模板
        return render(request, 'ResourceComment/resourceComment_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        commentTime = self.getStrParam(request, 'commentTime')
        # 然后条件组合查询过滤
        resourceComments = ResourceComment.objects.all()
        if resourceObj_resourceId != '0':
            resourceComments = resourceComments.filter(resourceObj=resourceObj_resourceId)
        if teacherObj_teacherNo != '':
            resourceComments = resourceComments.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            resourceComments = resourceComments.filter(userObj=userObj_user_name)
        if commentTime != '':
            resourceComments = resourceComments.filter(commentTime__contains=commentTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(resourceComments, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceComments_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        resourceCommentList = []
        for resourceComment in resourceComments_page:
            resourceComment = resourceComment.getJsonObj()
            resourceCommentList.append(resourceComment)
        # 构造模板页面需要的参数
        resourceComment_res = {
            'rows': resourceCommentList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(resourceComment_res, json_dumps_params={'ensure_ascii':False})


class TeacherListView(BaseView):  # 后台资源评论列表
    def get(self, request):
        # 使用模板
        return render(request, 'ResourceComment/resourceComment_teacherQuery_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        teacherObj_teacherNo = request.session.get('teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        commentTime = self.getStrParam(request, 'commentTime')
        # 然后条件组合查询过滤
        resourceComments = ResourceComment.objects.all()
        if resourceObj_resourceId != '0':
            resourceComments = resourceComments.filter(resourceObj=resourceObj_resourceId)
        if teacherObj_teacherNo != '':
            resourceComments = resourceComments.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            resourceComments = resourceComments.filter(userObj=userObj_user_name)
        if commentTime != '':
            resourceComments = resourceComments.filter(commentTime__contains=commentTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(resourceComments, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceComments_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        resourceCommentList = []
        for resourceComment in resourceComments_page:
            resourceComment = resourceComment.getJsonObj()
            resourceCommentList.append(resourceComment)
        # 构造模板页面需要的参数
        resourceComment_res = {
            'rows': resourceCommentList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(resourceComment_res, json_dumps_params={'ensure_ascii':False})


class DeletesView(BaseView):  # 删除资源评论信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        commentIds = self.getStrParam(request, 'commentIds')
        commentIds = commentIds.split(',')
        count = 0
        try:
            for commentId in commentIds:
                ResourceComment.objects.get(commentId=commentId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出资源评论信息到excel并下载
    def get(self, request):
        # 收集查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        commentTime = self.getStrParam(request, 'commentTime')
        # 然后条件组合查询过滤
        resourceComments = ResourceComment.objects.all()
        if resourceObj_resourceId != '0':
            resourceComments = resourceComments.filter(resourceObj=resourceObj_resourceId)
        if teacherObj_teacherNo != '':
            resourceComments = resourceComments.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            resourceComments = resourceComments.filter(userObj=userObj_user_name)
        if commentTime != '':
            resourceComments = resourceComments.filter(commentTime__contains=commentTime)
        #将查询结果集转换成列表
        resourceCommentList = []
        for resourceComment in resourceComments:
            resourceComment = resourceComment.getJsonObj()
            resourceCommentList.append(resourceComment)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(resourceCommentList)
        # 设置要导入到excel的列
        columns_map = {
            'commentId': '评论id',
            'resourceObj': '被评资源',
            'teacherObj': '资源发布人',
            'commentScore': '评分',
            'content': '评论内容',
            'userObj': '评论用户',
            'commentTime': '评论时间',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'resourceComments.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="resourceComments.xlsx"'
        return response


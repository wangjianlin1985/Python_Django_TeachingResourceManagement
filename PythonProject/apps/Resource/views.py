from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Resource.models import Resource
from apps.ResourceComment.models import ResourceComment
from apps.ResourceType.models import ResourceType
from apps.Teacher.models import Teacher
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台教学资源添加
    def get(self,request):
        resourceTypes = ResourceType.objects.all()  # 获取所有资源类型
        teachers = Teacher.objects.all()  # 获取所有老师
        context = {
            'resourceTypes': resourceTypes,
            'teachers': teachers,
        }

        # 使用模板
        return render(request, 'Resource/resource_frontAdd.html', context)

    def post(self, request):
        resource = Resource() # 新建一个教学资源对象然后获取参数
        resource.resourceTypeObj = ResourceType.objects.get(typeId=request.POST.get('resource.resourceTypeObj.typeId'))
        resource.resourceName = request.POST.get('resource.resourceName')
        try:
            resource.resourcePhoto = self.uploadImageFile(request,'resource.resourcePhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        resource.resourceDesc = request.POST.get('resource.resourceDesc')
        resource.resourceFile = self.uploadCommonFile(request,'resource.resourceFile')
        resource.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resource.teacherObj.teacherNo'))
        resource.uploadTime = request.POST.get('resource.uploadTime')
        resource.shenHeState = request.POST.get('resource.shenHeState')
        resource.shenHeReply = request.POST.get('resource.shenHeReply')
        resource.save() # 保存教学资源信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改教学资源
    def get(self, request, resourceId):
        context = {'resourceId': resourceId}
        return render(request, 'Resource/resource_frontModify.html', context)


class FrontListView(BaseView):  # 前台教学资源查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        resourceTypeObj_typeId = self.getIntParam(request, 'resourceTypeObj.typeId')
        resourceName = self.getStrParam(request, 'resourceName')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        uploadTime = self.getStrParam(request, 'uploadTime')
        #shenHeState = self.getStrParam(request, 'shenHeState')
        shenHeState = '审核通过'
        # 然后条件组合查询过滤
        resources = Resource.objects.all()
        if resourceTypeObj_typeId != '0':
            resources = resources.filter(resourceTypeObj=resourceTypeObj_typeId)
        if resourceName != '':
            resources = resources.filter(resourceName__contains=resourceName)
        if teacherObj_teacherNo != '':
            resources = resources.filter(teacherObj=teacherObj_teacherNo)
        if uploadTime != '':
            resources = resources.filter(uploadTime__contains=uploadTime)
        if shenHeState != '':
            resources = resources.filter(shenHeState__contains=shenHeState)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(resources, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resources_page = self.paginator.page(self.currentPage)

        # 获取所有资源类型
        resourceTypes = ResourceType.objects.all()
        # 获取所有老师
        teachers = Teacher.objects.all()
        # 构造模板需要的参数
        context = {
            'resourceTypes': resourceTypes,
            'teachers': teachers,
            'resources_page': resources_page,
            'resourceTypeObj_typeId': int(resourceTypeObj_typeId),
            'resourceName': resourceName,
            'teacherObj_teacherNo': teacherObj_teacherNo,
            'uploadTime': uploadTime,
            'shenHeState': shenHeState,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Resource/resource_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示教学资源详情页
    def get(self, request, resourceId):
        # 查询需要显示的教学资源对象
        resource = Resource.objects.get(resourceId=resourceId)

        resourceComments = ResourceComment.objects.all().order_by('-commentTime')
        resourceComments = resourceComments.filter(resourceObj=resourceId)


        context = {
            'resource': resource,
            'resourceComments': resourceComments
        }
        # 渲染模板显示
        return render(request, 'Resource/resource_frontshow.html', context)


class ListAllView(View): # 前台查询所有教学资源
    def get(self,request):
        resources = Resource.objects.all()
        resourceList = []
        for resource in resources:
            resourceObj = {
                'resourceId': resource.resourceId,
                'resourceName': resource.resourceName,
            }
            resourceList.append(resourceObj)
        return JsonResponse(resourceList, safe=False)


class UpdateView(BaseView):  # Ajax方式教学资源更新
    def get(self, request, resourceId):
        # GET方式请求查询教学资源对象并返回教学资源json格式
        resource = Resource.objects.get(resourceId=resourceId)
        return JsonResponse(resource.getJsonObj())

    def post(self, request, resourceId):
        # POST方式提交教学资源修改信息更新到数据库
        resource = Resource.objects.get(resourceId=resourceId)
        resource.resourceTypeObj = ResourceType.objects.get(typeId=request.POST.get('resource.resourceTypeObj.typeId'))
        resource.resourceName = request.POST.get('resource.resourceName')
        try:
            resourcePhotoName = self.uploadImageFile(request, 'resource.resourcePhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if resourcePhotoName != 'img/NoImage.jpg':
            resource.resourcePhoto = resourcePhotoName
        resource.resourceDesc = request.POST.get('resource.resourceDesc')
        resourceFileName = self.uploadCommonFile(request, 'resource.resourceFile')
        if resourceFileName != 'file/NoFile.jpg':
            resource.resourceFile = resourceFileName
        resource.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resource.teacherObj.teacherNo'))
        resource.uploadTime = request.POST.get('resource.uploadTime')
        resource.shenHeState = request.POST.get('resource.shenHeState')
        resource.shenHeReply = request.POST.get('resource.shenHeReply')
        resource.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台教学资源添加
    def get(self,request):
        resourceTypes = ResourceType.objects.all()  # 获取所有资源类型
        teachers = Teacher.objects.all()  # 获取所有老师
        context = {
            'resourceTypes': resourceTypes,
            'teachers': teachers,
        }

        # 渲染显示模板界面
        return render(request, 'Resource/resource_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        resource = Resource() # 新建一个教学资源对象然后获取参数
        resource.resourceTypeObj = ResourceType.objects.get(typeId=request.POST.get('resource.resourceTypeObj.typeId'))
        resource.resourceName = request.POST.get('resource.resourceName')
        try:
            resource.resourcePhoto = self.uploadImageFile(request,'resource.resourcePhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        resource.resourceDesc = request.POST.get('resource.resourceDesc')
        resource.resourceFile = self.uploadCommonFile(request,'resource.resourceFile')
        resource.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('resource.teacherObj.teacherNo'))
        resource.uploadTime = request.POST.get('resource.uploadTime')
        resource.shenHeState = request.POST.get('resource.shenHeState')
        resource.shenHeReply = request.POST.get('resource.shenHeReply')
        resource.save() # 保存教学资源信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class TeacherAddView(BaseView):  # 后台教学资源添加
    def get(self,request):
        resourceTypes = ResourceType.objects.all()  # 获取所有资源类型
        teachers = Teacher.objects.all()  # 获取所有老师
        context = {
            'resourceTypes': resourceTypes,
            'teachers': teachers,
        }

        # 渲染显示模板界面
        return render(request, 'Resource/resource_teacherAdd.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        resource = Resource() # 新建一个教学资源对象然后获取参数
        resource.resourceTypeObj = ResourceType.objects.get(typeId=request.POST.get('resource.resourceTypeObj.typeId'))
        resource.resourceName = request.POST.get('resource.resourceName')
        try:
            resource.resourcePhoto = self.uploadImageFile(request,'resource.resourcePhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        resource.resourceDesc = request.POST.get('resource.resourceDesc')
        resource.resourceFile = self.uploadCommonFile(request,'resource.resourceFile')
        resource.teacherObj = Teacher.objects.get(teacherNo=request.session.get('teacherNo'))
        import datetime
        resource.uploadTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        resource.shenHeState = '待审核'
        resource.shenHeReply = '--'
        resource.save() # 保存教学资源信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})



class BackModifyView(BaseView):  # 后台更新教学资源
    def get(self, request, resourceId):
        context = {'resourceId': resourceId}
        return render(request, 'Resource/resource_modify.html', context)


class ListView(BaseView):  # 后台教学资源列表
    def get(self, request):
        # 使用模板
        return render(request, 'Resource/resource_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        resourceTypeObj_typeId = self.getIntParam(request, 'resourceTypeObj.typeId')
        resourceName = self.getStrParam(request, 'resourceName')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        uploadTime = self.getStrParam(request, 'uploadTime')
        shenHeState = self.getStrParam(request, 'shenHeState')
        # 然后条件组合查询过滤
        resources = Resource.objects.all()
        if resourceTypeObj_typeId != '0':
            resources = resources.filter(resourceTypeObj=resourceTypeObj_typeId)
        if resourceName != '':
            resources = resources.filter(resourceName__contains=resourceName)
        if teacherObj_teacherNo != '':
            resources = resources.filter(teacherObj=teacherObj_teacherNo)
        if uploadTime != '':
            resources = resources.filter(uploadTime__contains=uploadTime)
        if shenHeState != '':
            resources = resources.filter(shenHeState__contains=shenHeState)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(resources, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resources_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        resourceList = []
        for resource in resources_page:
            resource = resource.getJsonObj()
            resourceList.append(resource)
        # 构造模板页面需要的参数
        resource_res = {
            'rows': resourceList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(resource_res, json_dumps_params={'ensure_ascii':False})


class TeacherListView(BaseView):  # 后台教学资源列表
    def get(self, request):
        # 使用模板
        return render(request, 'Resource/resource_teacherQuery_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        resourceTypeObj_typeId = self.getIntParam(request, 'resourceTypeObj.typeId')
        resourceName = self.getStrParam(request, 'resourceName')
        teacherObj_teacherNo = request.session.get('teacherNo')
        uploadTime = self.getStrParam(request, 'uploadTime')
        shenHeState = self.getStrParam(request, 'shenHeState')
        # 然后条件组合查询过滤
        resources = Resource.objects.all()
        if resourceTypeObj_typeId != '0':
            resources = resources.filter(resourceTypeObj=resourceTypeObj_typeId)
        if resourceName != '':
            resources = resources.filter(resourceName__contains=resourceName)
        if teacherObj_teacherNo != '':
            resources = resources.filter(teacherObj=teacherObj_teacherNo)
        if uploadTime != '':
            resources = resources.filter(uploadTime__contains=uploadTime)
        if shenHeState != '':
            resources = resources.filter(shenHeState__contains=shenHeState)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(resources, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resources_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        resourceList = []
        for resource in resources_page:
            resource = resource.getJsonObj()
            resourceList.append(resource)
        # 构造模板页面需要的参数
        resource_res = {
            'rows': resourceList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(resource_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除教学资源信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        resourceIds = self.getStrParam(request, 'resourceIds')
        resourceIds = resourceIds.split(',')
        count = 0
        try:
            for resourceId in resourceIds:
                Resource.objects.get(resourceId=resourceId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出教学资源信息到excel并下载
    def get(self, request):
        # 收集查询参数
        resourceTypeObj_typeId = self.getIntParam(request, 'resourceTypeObj.typeId')
        resourceName = self.getStrParam(request, 'resourceName')
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        uploadTime = self.getStrParam(request, 'uploadTime')
        shenHeState = self.getStrParam(request, 'shenHeState')
        # 然后条件组合查询过滤
        resources = Resource.objects.all()
        if resourceTypeObj_typeId != '0':
            resources = resources.filter(resourceTypeObj=resourceTypeObj_typeId)
        if resourceName != '':
            resources = resources.filter(resourceName__contains=resourceName)
        if teacherObj_teacherNo != '':
            resources = resources.filter(teacherObj=teacherObj_teacherNo)
        if uploadTime != '':
            resources = resources.filter(uploadTime__contains=uploadTime)
        if shenHeState != '':
            resources = resources.filter(shenHeState__contains=shenHeState)
        #将查询结果集转换成列表
        resourceList = []
        for resource in resources:
            resource = resource.getJsonObj()
            resourceList.append(resource)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(resourceList)
        # 设置要导入到excel的列
        columns_map = {
            'resourceId': '资源id',
            'resourceTypeObj': '资源类型',
            'resourceName': '资源名称',
            'teacherObj': '上传老师',
            'uploadTime': '上传日期',
            'shenHeState': '审核状态',
            'shenHeReply': '审核回复',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'resources.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="resources.xlsx"'
        return response


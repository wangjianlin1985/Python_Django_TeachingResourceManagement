from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.ResourceType.models import ResourceType
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台资源类型添加
    def get(self,request):

        # 使用模板
        return render(request, 'ResourceType/resourceType_frontAdd.html')

    def post(self, request):
        resourceType = ResourceType() # 新建一个资源类型对象然后获取参数
        resourceType.typeName = request.POST.get('resourceType.typeName')
        resourceType.typeDesc = request.POST.get('resourceType.typeDesc')
        resourceType.save() # 保存资源类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改资源类型
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'ResourceType/resourceType_frontModify.html', context)


class FrontListView(BaseView):  # 前台资源类型查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        # 然后条件组合查询过滤
        resourceTypes = ResourceType.objects.all()
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(resourceTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceTypes_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'resourceTypes_page': resourceTypes_page,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'ResourceType/resourceType_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示资源类型详情页
    def get(self, request, typeId):
        # 查询需要显示的资源类型对象
        resourceType = ResourceType.objects.get(typeId=typeId)
        context = {
            'resourceType': resourceType
        }
        # 渲染模板显示
        return render(request, 'ResourceType/resourceType_frontshow.html', context)


class ListAllView(View): # 前台查询所有资源类型
    def get(self,request):
        resourceTypes = ResourceType.objects.all()
        resourceTypeList = []
        for resourceType in resourceTypes:
            resourceTypeObj = {
                'typeId': resourceType.typeId,
                'typeName': resourceType.typeName,
            }
            resourceTypeList.append(resourceTypeObj)
        return JsonResponse(resourceTypeList, safe=False)


class UpdateView(BaseView):  # Ajax方式资源类型更新
    def get(self, request, typeId):
        # GET方式请求查询资源类型对象并返回资源类型json格式
        resourceType = ResourceType.objects.get(typeId=typeId)
        return JsonResponse(resourceType.getJsonObj())

    def post(self, request, typeId):
        # POST方式提交资源类型修改信息更新到数据库
        resourceType = ResourceType.objects.get(typeId=typeId)
        resourceType.typeName = request.POST.get('resourceType.typeName')
        resourceType.typeDesc = request.POST.get('resourceType.typeDesc')
        resourceType.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台资源类型添加
    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'ResourceType/resourceType_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        resourceType = ResourceType() # 新建一个资源类型对象然后获取参数
        resourceType.typeName = request.POST.get('resourceType.typeName')
        resourceType.typeDesc = request.POST.get('resourceType.typeDesc')
        resourceType.save() # 保存资源类型信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新资源类型
    def get(self, request, typeId):
        context = {'typeId': typeId}
        return render(request, 'ResourceType/resourceType_modify.html', context)


class ListView(BaseView):  # 后台资源类型列表
    def get(self, request):
        # 使用模板
        return render(request, 'ResourceType/resourceType_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        # 然后条件组合查询过滤
        resourceTypes = ResourceType.objects.all()
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(resourceTypes, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        resourceTypes_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        resourceTypeList = []
        for resourceType in resourceTypes_page:
            resourceType = resourceType.getJsonObj()
            resourceTypeList.append(resourceType)
        # 构造模板页面需要的参数
        resourceType_res = {
            'rows': resourceTypeList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(resourceType_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除资源类型信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        typeIds = self.getStrParam(request, 'typeIds')
        typeIds = typeIds.split(',')
        count = 0
        try:
            for typeId in typeIds:
                ResourceType.objects.get(typeId=typeId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出资源类型信息到excel并下载
    def get(self, request):
        # 收集查询参数
        # 然后条件组合查询过滤
        resourceTypes = ResourceType.objects.all()
        #将查询结果集转换成列表
        resourceTypeList = []
        for resourceType in resourceTypes:
            resourceType = resourceType.getJsonObj()
            resourceTypeList.append(resourceType)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(resourceTypeList)
        # 设置要导入到excel的列
        columns_map = {
            'typeId': '类型id',
            'typeName': '类型名称',
            'typeDesc': '类型描述',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'resourceTypes.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="resourceTypes.xlsx"'
        return response


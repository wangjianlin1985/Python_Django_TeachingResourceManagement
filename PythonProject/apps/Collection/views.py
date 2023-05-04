from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Collection.models import Collection
from apps.Resource.models import Resource
from apps.UserInfo.models import UserInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台资源收藏添加
    def get(self,request):
        resources = Resource.objects.all()  # 获取所有教学资源
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'resources': resources,
            'userInfos': userInfos,
        }

        # 使用模板
        return render(request, 'Collection/collection_frontAdd.html', context)

    def post(self, request):
        collection = Collection() # 新建一个资源收藏对象然后获取参数
        collection.resourceObj = Resource.objects.get(resourceId=request.POST.get('collection.resourceObj.resourceId'))
        collection.userObj = UserInfo.objects.get(user_name=request.POST.get('collection.userObj.user_name'))
        collection.collectTime = request.POST.get('collection.collectTime')
        collection.save() # 保存资源收藏信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontUserAddView(BaseView):  # 前台资源收藏添加
    def post(self, request):
        user_name = request.session.get('user_name')
        if user_name == None:
            return JsonResponse({'success': False, 'message': '请先登录网站'})
        collection = Collection() # 新建一个资源收藏对象然后获取参数
        collection.resourceObj = Resource.objects.get(resourceId=request.POST.get('collection.resourceObj.resourceId'))
        collection.userObj = UserInfo.objects.get(user_name=user_name)
        import datetime
        collection.collectTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 判断是否已经收藏过资源
        sql = "select *  from t_collection where resourceObj=" + str(collection.resourceObj.resourceId) + " and userObj='" + user_name + "'"
        # print(sql)
        collections = Collection.objects.raw(sql)
        conflictCount = len(collections)
        print("冲突记录数:", conflictCount)
        if conflictCount > 0:
            return JsonResponse({'success': False, 'message': '你已经收藏过这个资源了！'})

        collection.save() # 保存资源收藏信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})



class FrontModifyView(BaseView):  # 前台修改资源收藏
    def get(self, request, collectionId):
        context = {'collectionId': collectionId}
        return render(request, 'Collection/collection_frontModify.html', context)


class FrontListView(BaseView):  # 前台资源收藏查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        collectTime = self.getStrParam(request, 'collectTime')
        # 然后条件组合查询过滤
        collections = Collection.objects.all()
        if resourceObj_resourceId != '0':
            collections = collections.filter(resourceObj=resourceObj_resourceId)
        if userObj_user_name != '':
            collections = collections.filter(userObj=userObj_user_name)
        if collectTime != '':
            collections = collections.filter(collectTime__contains=collectTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(collections, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        collections_page = self.paginator.page(self.currentPage)

        # 获取所有教学资源
        resources = Resource.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'resources': resources,
            'userInfos': userInfos,
            'collections_page': collections_page,
            'resourceObj_resourceId': int(resourceObj_resourceId),
            'userObj_user_name': userObj_user_name,
            'collectTime': collectTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Collection/collection_frontquery_result.html', context)


class FrontUserListView(BaseView):  # 前台资源收藏查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        userObj_user_name = request.session.get('user_name')
        collectTime = self.getStrParam(request, 'collectTime')
        # 然后条件组合查询过滤
        collections = Collection.objects.all()
        if resourceObj_resourceId != '0':
            collections = collections.filter(resourceObj=resourceObj_resourceId)
        if userObj_user_name != '':
            collections = collections.filter(userObj=userObj_user_name)
        if collectTime != '':
            collections = collections.filter(collectTime__contains=collectTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(collections, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        collections_page = self.paginator.page(self.currentPage)

        # 获取所有教学资源
        resources = Resource.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'resources': resources,
            'userInfos': userInfos,
            'collections_page': collections_page,
            'resourceObj_resourceId': int(resourceObj_resourceId),
            'userObj_user_name': userObj_user_name,
            'collectTime': collectTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Collection/collection_userFrontquery_result.html', context)



class FrontShowView(View):  # 前台显示资源收藏详情页
    def get(self, request, collectionId):
        # 查询需要显示的资源收藏对象
        collection = Collection.objects.get(collectionId=collectionId)
        context = {
            'collection': collection
        }
        # 渲染模板显示
        return render(request, 'Collection/collection_frontshow.html', context)


class ListAllView(View): # 前台查询所有资源收藏
    def get(self,request):
        collections = Collection.objects.all()
        collectionList = []
        for collection in collections:
            collectionObj = {
                'collectionId': collection.collectionId,
            }
            collectionList.append(collectionObj)
        return JsonResponse(collectionList, safe=False)


class UpdateView(BaseView):  # Ajax方式资源收藏更新
    def get(self, request, collectionId):
        # GET方式请求查询资源收藏对象并返回资源收藏json格式
        collection = Collection.objects.get(collectionId=collectionId)
        return JsonResponse(collection.getJsonObj())

    def post(self, request, collectionId):
        # POST方式提交资源收藏修改信息更新到数据库
        collection = Collection.objects.get(collectionId=collectionId)
        collection.resourceObj = Resource.objects.get(resourceId=request.POST.get('collection.resourceObj.resourceId'))
        collection.userObj = UserInfo.objects.get(user_name=request.POST.get('collection.userObj.user_name'))
        collection.collectTime = request.POST.get('collection.collectTime')
        collection.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台资源收藏添加
    def get(self,request):
        resources = Resource.objects.all()  # 获取所有教学资源
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'resources': resources,
            'userInfos': userInfos,
        }

        # 渲染显示模板界面
        return render(request, 'Collection/collection_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        collection = Collection() # 新建一个资源收藏对象然后获取参数
        collection.resourceObj = Resource.objects.get(resourceId=request.POST.get('collection.resourceObj.resourceId'))
        collection.userObj = UserInfo.objects.get(user_name=request.POST.get('collection.userObj.user_name'))
        collection.collectTime = request.POST.get('collection.collectTime')
        collection.save() # 保存资源收藏信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新资源收藏
    def get(self, request, collectionId):
        context = {'collectionId': collectionId}
        return render(request, 'Collection/collection_modify.html', context)


class ListView(BaseView):  # 后台资源收藏列表
    def get(self, request):
        # 使用模板
        return render(request, 'Collection/collection_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        collectTime = self.getStrParam(request, 'collectTime')
        # 然后条件组合查询过滤
        collections = Collection.objects.all()
        if resourceObj_resourceId != '0':
            collections = collections.filter(resourceObj=resourceObj_resourceId)
        if userObj_user_name != '':
            collections = collections.filter(userObj=userObj_user_name)
        if collectTime != '':
            collections = collections.filter(collectTime__contains=collectTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(collections, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        collections_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        collectionList = []
        for collection in collections_page:
            collection = collection.getJsonObj()
            collectionList.append(collection)
        # 构造模板页面需要的参数
        collection_res = {
            'rows': collectionList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(collection_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除资源收藏信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        collectionIds = self.getStrParam(request, 'collectionIds')
        collectionIds = collectionIds.split(',')
        count = 0
        try:
            for collectionId in collectionIds:
                Collection.objects.get(collectionId=collectionId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出资源收藏信息到excel并下载
    def get(self, request):
        # 收集查询参数
        resourceObj_resourceId = self.getIntParam(request, 'resourceObj.resourceId')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        collectTime = self.getStrParam(request, 'collectTime')
        # 然后条件组合查询过滤
        collections = Collection.objects.all()
        if resourceObj_resourceId != '0':
            collections = collections.filter(resourceObj=resourceObj_resourceId)
        if userObj_user_name != '':
            collections = collections.filter(userObj=userObj_user_name)
        if collectTime != '':
            collections = collections.filter(collectTime__contains=collectTime)
        #将查询结果集转换成列表
        collectionList = []
        for collection in collections:
            collection = collection.getJsonObj()
            collectionList.append(collection)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(collectionList)
        # 设置要导入到excel的列
        columns_map = {
            'collectionId': '收藏id',
            'resourceObj': '收藏的资源',
            'userObj': '收藏用户',
            'collectTime': '收藏时间',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'collections.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="collections.xlsx"'
        return response


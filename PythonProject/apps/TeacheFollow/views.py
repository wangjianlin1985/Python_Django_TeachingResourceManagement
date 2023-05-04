from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.TeacheFollow.models import TeacheFollow
from apps.Teacher.models import Teacher
from apps.UserInfo.models import UserInfo
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台老师订阅添加
    def get(self,request):
        teachers = Teacher.objects.all()  # 获取所有老师
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'teachers': teachers,
            'userInfos': userInfos,
        }

        # 使用模板
        return render(request, 'TeacheFollow/teacheFollow_frontAdd.html', context)

    def post(self, request):
        teacheFollow = TeacheFollow() # 新建一个老师订阅对象然后获取参数
        teacheFollow.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('teacheFollow.teacherObj.teacherNo'))
        teacheFollow.userObj = UserInfo.objects.get(user_name=request.POST.get('teacheFollow.userObj.user_name'))
        teacheFollow.followTime = request.POST.get('teacheFollow.followTime')
        teacheFollow.save() # 保存老师订阅信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})

class FrontUserAddView(BaseView):  # 前台老师订阅添加
    def post(self, request):
        user_name = request.session.get('user_name')
        if user_name == None:
            return JsonResponse({'success': False, 'message': '请先登录网站'})
        teacheFollow = TeacheFollow() # 新建一个老师订阅对象然后获取参数
        teacheFollow.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('teacheFollow.teacherObj.teacherNo'))
        teacheFollow.userObj = UserInfo.objects.get(user_name=user_name)
        import datetime
        teacheFollow.followTime = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # 判断是否已经订阅过老师
        sql = "select *  from t_TeacheFollow where teacherObj='" + teacheFollow.teacherObj.teacherNo  + "' and userObj='" + user_name + "'"
        # print(sql)
        teacheFollows = TeacheFollow.objects.raw(sql)
        conflictCount = len(teacheFollows)
        print("冲突记录数:", conflictCount)
        if conflictCount > 0:
            return JsonResponse({'success': False, 'message': '你已经订阅过这个老师了！'})


        teacheFollow.save() # 保存老师订阅信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})



class FrontModifyView(BaseView):  # 前台修改老师订阅
    def get(self, request, followId):
        context = {'followId': followId}
        return render(request, 'TeacheFollow/teacheFollow_frontModify.html', context)


class FrontListView(BaseView):  # 前台老师订阅查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        followTime = self.getStrParam(request, 'followTime')
        # 然后条件组合查询过滤
        teacheFollows = TeacheFollow.objects.all()
        if teacherObj_teacherNo != '':
            teacheFollows = teacheFollows.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            teacheFollows = teacheFollows.filter(userObj=userObj_user_name)
        if followTime != '':
            teacheFollows = teacheFollows.filter(followTime__contains=followTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(teacheFollows, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teacheFollows_page = self.paginator.page(self.currentPage)

        # 获取所有老师
        teachers = Teacher.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'teachers': teachers,
            'userInfos': userInfos,
            'teacheFollows_page': teacheFollows_page,
            'teacherObj_teacherNo': teacherObj_teacherNo,
            'userObj_user_name': userObj_user_name,
            'followTime': followTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'TeacheFollow/teacheFollow_frontquery_result.html', context)


class FrontUserListView(BaseView):  # 前台老师订阅查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name =  request.session.get('user_name')
        followTime = self.getStrParam(request, 'followTime')
        # 然后条件组合查询过滤
        teacheFollows = TeacheFollow.objects.all()
        if teacherObj_teacherNo != '':
            teacheFollows = teacheFollows.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            teacheFollows = teacheFollows.filter(userObj=userObj_user_name)
        if followTime != '':
            teacheFollows = teacheFollows.filter(followTime__contains=followTime)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(teacheFollows, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teacheFollows_page = self.paginator.page(self.currentPage)

        # 获取所有老师
        teachers = Teacher.objects.all()
        # 获取所有用户
        userInfos = UserInfo.objects.all()
        # 构造模板需要的参数
        context = {
            'teachers': teachers,
            'userInfos': userInfos,
            'teacheFollows_page': teacheFollows_page,
            'teacherObj_teacherNo': teacherObj_teacherNo,
            'userObj_user_name': userObj_user_name,
            'followTime': followTime,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'TeacheFollow/teacheFollow_userFrontquery_result.html', context)


class FrontShowView(View):  # 前台显示老师订阅详情页
    def get(self, request, followId):
        # 查询需要显示的老师订阅对象
        teacheFollow = TeacheFollow.objects.get(followId=followId)
        context = {
            'teacheFollow': teacheFollow
        }
        # 渲染模板显示
        return render(request, 'TeacheFollow/teacheFollow_frontshow.html', context)


class ListAllView(View): # 前台查询所有老师订阅
    def get(self,request):
        teacheFollows = TeacheFollow.objects.all()
        teacheFollowList = []
        for teacheFollow in teacheFollows:
            teacheFollowObj = {
                'followId': teacheFollow.followId,
            }
            teacheFollowList.append(teacheFollowObj)
        return JsonResponse(teacheFollowList, safe=False)


class UpdateView(BaseView):  # Ajax方式老师订阅更新
    def get(self, request, followId):
        # GET方式请求查询老师订阅对象并返回老师订阅json格式
        teacheFollow = TeacheFollow.objects.get(followId=followId)
        return JsonResponse(teacheFollow.getJsonObj())

    def post(self, request, followId):
        # POST方式提交老师订阅修改信息更新到数据库
        teacheFollow = TeacheFollow.objects.get(followId=followId)
        teacheFollow.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('teacheFollow.teacherObj.teacherNo'))
        teacheFollow.userObj = UserInfo.objects.get(user_name=request.POST.get('teacheFollow.userObj.user_name'))
        teacheFollow.followTime = request.POST.get('teacheFollow.followTime')
        teacheFollow.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台老师订阅添加
    def get(self,request):
        teachers = Teacher.objects.all()  # 获取所有老师
        userInfos = UserInfo.objects.all()  # 获取所有用户
        context = {
            'teachers': teachers,
            'userInfos': userInfos,
        }

        # 渲染显示模板界面
        return render(request, 'TeacheFollow/teacheFollow_add.html', context)

    def post(self, request):
        # POST方式处理图书添加业务
        teacheFollow = TeacheFollow() # 新建一个老师订阅对象然后获取参数
        teacheFollow.teacherObj = Teacher.objects.get(teacherNo=request.POST.get('teacheFollow.teacherObj.teacherNo'))
        teacheFollow.userObj = UserInfo.objects.get(user_name=request.POST.get('teacheFollow.userObj.user_name'))
        teacheFollow.followTime = request.POST.get('teacheFollow.followTime')
        teacheFollow.save() # 保存老师订阅信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新老师订阅
    def get(self, request, followId):
        context = {'followId': followId}
        return render(request, 'TeacheFollow/teacheFollow_modify.html', context)


class ListView(BaseView):  # 后台老师订阅列表
    def get(self, request):
        # 使用模板
        return render(request, 'TeacheFollow/teacheFollow_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        followTime = self.getStrParam(request, 'followTime')
        # 然后条件组合查询过滤
        teacheFollows = TeacheFollow.objects.all()
        if teacherObj_teacherNo != '':
            teacheFollows = teacheFollows.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            teacheFollows = teacheFollows.filter(userObj=userObj_user_name)
        if followTime != '':
            teacheFollows = teacheFollows.filter(followTime__contains=followTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(teacheFollows, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teacheFollows_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        teacheFollowList = []
        for teacheFollow in teacheFollows_page:
            teacheFollow = teacheFollow.getJsonObj()
            teacheFollowList.append(teacheFollow)
        # 构造模板页面需要的参数
        teacheFollow_res = {
            'rows': teacheFollowList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(teacheFollow_res, json_dumps_params={'ensure_ascii':False})


class TeacherListView(BaseView):  # 后台老师订阅列表
    def get(self, request):
        # 使用模板
        return render(request, 'TeacheFollow/teacheFollow_teacherQuery_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        teacherObj_teacherNo = request.session.get('teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        followTime = self.getStrParam(request, 'followTime')
        # 然后条件组合查询过滤
        teacheFollows = TeacheFollow.objects.all()
        if teacherObj_teacherNo != '':
            teacheFollows = teacheFollows.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            teacheFollows = teacheFollows.filter(userObj=userObj_user_name)
        if followTime != '':
            teacheFollows = teacheFollows.filter(followTime__contains=followTime)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(teacheFollows, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teacheFollows_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        teacheFollowList = []
        for teacheFollow in teacheFollows_page:
            teacheFollow = teacheFollow.getJsonObj()
            teacheFollowList.append(teacheFollow)
        # 构造模板页面需要的参数
        teacheFollow_res = {
            'rows': teacheFollowList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(teacheFollow_res, json_dumps_params={'ensure_ascii':False})


class DeletesView(BaseView):  # 删除老师订阅信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        followIds = self.getStrParam(request, 'followIds')
        followIds = followIds.split(',')
        count = 0
        try:
            for followId in followIds:
                TeacheFollow.objects.get(followId=followId).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出老师订阅信息到excel并下载
    def get(self, request):
        # 收集查询参数
        teacherObj_teacherNo = self.getStrParam(request, 'teacherObj.teacherNo')
        userObj_user_name = self.getStrParam(request, 'userObj.user_name')
        followTime = self.getStrParam(request, 'followTime')
        # 然后条件组合查询过滤
        teacheFollows = TeacheFollow.objects.all()
        if teacherObj_teacherNo != '':
            teacheFollows = teacheFollows.filter(teacherObj=teacherObj_teacherNo)
        if userObj_user_name != '':
            teacheFollows = teacheFollows.filter(userObj=userObj_user_name)
        if followTime != '':
            teacheFollows = teacheFollows.filter(followTime__contains=followTime)
        #将查询结果集转换成列表
        teacheFollowList = []
        for teacheFollow in teacheFollows:
            teacheFollow = teacheFollow.getJsonObj()
            teacheFollowList.append(teacheFollow)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(teacheFollowList)
        # 设置要导入到excel的列
        columns_map = {
            'followId': '订阅id',
            'teacherObj': '被订阅老师',
            'userObj': '订阅人',
            'followTime': '订阅时间',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'teacheFollows.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="teacheFollows.xlsx"'
        return response


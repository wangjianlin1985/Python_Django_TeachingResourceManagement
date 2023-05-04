from django.views.generic import View
from apps.BaseView import BaseView
from django.shortcuts import render
from django.core.paginator import Paginator
from apps.Teacher.models import Teacher
from django.http import JsonResponse
from django.http import FileResponse
from apps.BaseView import ImageFormatException
from django.conf import settings
import pandas as pd
import os


class FrontAddView(BaseView):  # 前台老师添加
    def primaryKeyExist(self, teacherNo):  # 判断主键是否存在
        try:
            Teacher.objects.get(teacherNo=teacherNo)
            return True
        except Teacher.DoesNotExist:
            return False

    def get(self,request):

        # 使用模板
        return render(request, 'Teacher/teacher_frontAdd.html')

    def post(self, request):
        teacherNo = request.POST.get('teacher.teacherNo') # 判断教师编号是否存在
        if self.primaryKeyExist(teacherNo):
            return JsonResponse({'success': False, 'message': '教师编号已经存在'})

        teacher = Teacher() # 新建一个老师对象然后获取参数
        teacher.teacherNo = teacherNo
        teacher.password = request.POST.get('teacher.password')
        teacher.name = request.POST.get('teacher.name')
        teacher.sex = request.POST.get('teacher.sex')
        teacher.birthDate = request.POST.get('teacher.birthDate')
        try:
            teacher.teacherPhoto = self.uploadImageFile(request,'teacher.teacherPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        teacher.zhicheng = request.POST.get('teacher.zhicheng')
        teacher.telephone = request.POST.get('teacher.telephone')
        teacher.comeDate = request.POST.get('teacher.comeDate')
        teacher.address = request.POST.get('teacher.address')
        teacher.teacherDesc = request.POST.get('teacher.teacherDesc')
        teacher.save() # 保存老师信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class FrontModifyView(BaseView):  # 前台修改老师
    def get(self, request, teacherNo):
        context = {'teacherNo': teacherNo}
        return render(request, 'Teacher/teacher_frontModify.html', context)


class FrontListView(BaseView):  # 前台老师查询列表
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        self.getCurrentPage(request)  # 获取当前要显示第几页
        # 下面获取查询参数
        teacherNo = self.getStrParam(request, 'teacherNo')
        name = self.getStrParam(request, 'name')
        birthDate = self.getStrParam(request, 'birthDate')
        zhicheng = self.getStrParam(request, 'zhicheng')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        teachers = Teacher.objects.all()
        if teacherNo != '':
            teachers = teachers.filter(teacherNo__contains=teacherNo)
        if name != '':
            teachers = teachers.filter(name__contains=name)
        if birthDate != '':
            teachers = teachers.filter(birthDate__contains=birthDate)
        if zhicheng != '':
            teachers = teachers.filter(zhicheng__contains=zhicheng)
        if telephone != '':
            teachers = teachers.filter(telephone__contains=telephone)
        # 对查询结果利用Paginator进行分页
        self.paginator = Paginator(teachers, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teachers_page = self.paginator.page(self.currentPage)

        # 构造模板需要的参数
        context = {
            'teachers_page': teachers_page,
            'teacherNo': teacherNo,
            'name': name,
            'birthDate': birthDate,
            'zhicheng': zhicheng,
            'telephone': telephone,
            'currentPage': self.currentPage,
            'totalPage': self.totalPage,
            'recordNumber': self.recordNumber,
            'startIndex': self.startIndex,
            'pageList': self.pageList,
        }
        # 渲染模板界面
        return render(request, 'Teacher/teacher_frontquery_result.html', context)


class FrontShowView(View):  # 前台显示老师详情页
    def get(self, request, teacherNo):
        # 查询需要显示的老师对象
        teacher = Teacher.objects.get(teacherNo=teacherNo)
        context = {
            'teacher': teacher
        }
        # 渲染模板显示
        return render(request, 'Teacher/teacher_frontshow.html', context)


class ListAllView(View): # 前台查询所有老师
    def get(self,request):
        teachers = Teacher.objects.all()
        teacherList = []
        for teacher in teachers:
            teacherObj = {
                'teacherNo': teacher.teacherNo,
                'name': teacher.name,
            }
            teacherList.append(teacherObj)
        return JsonResponse(teacherList, safe=False)


class UpdateView(BaseView):  # Ajax方式老师更新
    def get(self, request, teacherNo):
        # GET方式请求查询老师对象并返回老师json格式
        teacher = Teacher.objects.get(teacherNo=teacherNo)
        return JsonResponse(teacher.getJsonObj())

    def post(self, request, teacherNo):
        # POST方式提交老师修改信息更新到数据库
        teacher = Teacher.objects.get(teacherNo=teacherNo)
        teacher.password = request.POST.get('teacher.password')
        teacher.name = request.POST.get('teacher.name')
        teacher.sex = request.POST.get('teacher.sex')
        teacher.birthDate = request.POST.get('teacher.birthDate')
        try:
            teacherPhotoName = self.uploadImageFile(request, 'teacher.teacherPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        if teacherPhotoName != 'img/NoImage.jpg':
            teacher.teacherPhoto = teacherPhotoName
        teacher.zhicheng = request.POST.get('teacher.zhicheng')
        teacher.telephone = request.POST.get('teacher.telephone')
        teacher.comeDate = request.POST.get('teacher.comeDate')
        teacher.address = request.POST.get('teacher.address')
        teacher.teacherDesc = request.POST.get('teacher.teacherDesc')
        teacher.save()
        return JsonResponse({'success': True, 'message': '保存成功'})

class AddView(BaseView):  # 后台老师添加
    def primaryKeyExist(self, teacherNo):  # 判断主键是否存在
        try:
            Teacher.objects.get(teacherNo=teacherNo)
            return True
        except Teacher.DoesNotExist:
            return False

    def get(self,request):

        # 渲染显示模板界面
        return render(request, 'Teacher/teacher_add.html')

    def post(self, request):
        # POST方式处理图书添加业务
        teacherNo = request.POST.get('teacher.teacherNo') # 判断教师编号是否存在
        if self.primaryKeyExist(teacherNo):
            return JsonResponse({'success': False, 'message': '教师编号已经存在'})

        teacher = Teacher() # 新建一个老师对象然后获取参数
        teacher.teacherNo = teacherNo
        teacher.password = request.POST.get('teacher.password')
        teacher.name = request.POST.get('teacher.name')
        teacher.sex = request.POST.get('teacher.sex')
        teacher.birthDate = request.POST.get('teacher.birthDate')
        try:
            teacher.teacherPhoto = self.uploadImageFile(request,'teacher.teacherPhoto')
        except ImageFormatException as ife:
            return JsonResponse({'success': False, 'message': ife.error})
        teacher.zhicheng = request.POST.get('teacher.zhicheng')
        teacher.telephone = request.POST.get('teacher.telephone')
        teacher.comeDate = request.POST.get('teacher.comeDate')
        teacher.address = request.POST.get('teacher.address')
        teacher.teacherDesc = request.POST.get('teacher.teacherDesc')
        teacher.save() # 保存老师信息到数据库
        return JsonResponse({'success': True, 'message': '保存成功'})


class BackModifyView(BaseView):  # 后台更新老师
    def get(self, request, teacherNo):
        context = {'teacherNo': teacherNo}
        return render(request, 'Teacher/teacher_modify.html', context)

class BackSelfModifyView(BaseView):  # 后台更新老师
    def get(self, request):
        context = {'teacherNo': request.session.get('teacherNo')}
        return render(request, 'Teacher/teacher_modify.html', context)


class ListView(BaseView):  # 后台老师列表
    def get(self, request):
        # 使用模板
        return render(request, 'Teacher/teacher_query_result.html')

    def post(self, request):
        # 获取当前要显示第几页和每页几条数据
        self.getPageAndSize(request)
        # 收集查询参数
        teacherNo = self.getStrParam(request, 'teacherNo')
        name = self.getStrParam(request, 'name')
        birthDate = self.getStrParam(request, 'birthDate')
        zhicheng = self.getStrParam(request, 'zhicheng')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        teachers = Teacher.objects.all()
        if teacherNo != '':
            teachers = teachers.filter(teacherNo__contains=teacherNo)
        if name != '':
            teachers = teachers.filter(name__contains=name)
        if birthDate != '':
            teachers = teachers.filter(birthDate__contains=birthDate)
        if zhicheng != '':
            teachers = teachers.filter(zhicheng__contains=zhicheng)
        if telephone != '':
            teachers = teachers.filter(telephone__contains=telephone)
        # 利用Paginator对查询结果集分页
        self.paginator = Paginator(teachers, self.pageSize)
        # 计算总的页码数，要显示的页码列表，总记录等
        self.calculatePages()
        # 获取第page页的Page实例对象
        teachers_page = self.paginator.page(self.currentPage)
        # 查询的结果集转换为列表
        teacherList = []
        for teacher in teachers_page:
            teacher = teacher.getJsonObj()
            teacherList.append(teacher)
        # 构造模板页面需要的参数
        teacher_res = {
            'rows': teacherList,
            'total': self.recordNumber,
        }
        # 渲染模板页面显示
        return JsonResponse(teacher_res, json_dumps_params={'ensure_ascii':False})

class DeletesView(BaseView):  # 删除老师信息
    def get(self, request):
        return self.handle(request)

    def post(self, request):
        return self.handle(request)

    def handle(self, request):
        teacherNos = self.getStrParam(request, 'teacherNos')
        teacherNos = teacherNos.split(',')
        count = 0
        try:
            for teacherNo in teacherNos:
                Teacher.objects.get(teacherNo=teacherNo).delete()
                count = count + 1
            message = '%s条记录删除成功！' % count
            success = True
        except Exception as e:
            message = '数据库外键约束删除失败！'
            success = False
        return JsonResponse({'success': success, 'message': message})


class OutToExcelView(BaseView):  # 导出老师信息到excel并下载
    def get(self, request):
        # 收集查询参数
        teacherNo = self.getStrParam(request, 'teacherNo')
        name = self.getStrParam(request, 'name')
        birthDate = self.getStrParam(request, 'birthDate')
        zhicheng = self.getStrParam(request, 'zhicheng')
        telephone = self.getStrParam(request, 'telephone')
        # 然后条件组合查询过滤
        teachers = Teacher.objects.all()
        if teacherNo != '':
            teachers = teachers.filter(teacherNo__contains=teacherNo)
        if name != '':
            teachers = teachers.filter(name__contains=name)
        if birthDate != '':
            teachers = teachers.filter(birthDate__contains=birthDate)
        if zhicheng != '':
            teachers = teachers.filter(zhicheng__contains=zhicheng)
        if telephone != '':
            teachers = teachers.filter(telephone__contains=telephone)
        #将查询结果集转换成列表
        teacherList = []
        for teacher in teachers:
            teacher = teacher.getJsonObj()
            teacherList.append(teacher)
        # 利用pandas实现数据的导出功能
        pf = pd.DataFrame(teacherList)
        # 设置要导入到excel的列
        columns_map = {
            'teacherNo': '教师编号',
            'name': '姓名',
            'sex': '性别',
            'birthDate': '出生日期',
            'zhicheng': '职称',
            'telephone': '联系电话',
            'comeDate': '入职日期',
        }
        pf = pf[columns_map.keys()]
        pf.rename(columns=columns_map, inplace=True)
        # 将空的单元格替换为空字符
        pf.fillna('', inplace=True)
        #设定文件名和导出路径
        filename = 'teachers.xlsx'
        # 这个路径可以在settings中设置也可以直接手动输入
        root_path = settings.MEDIA_ROOT + '/output/'
        file_path = os.path.join(root_path, filename)
        pf.to_excel(file_path, encoding='utf-8', index=False)
        # 将生成的excel文件输出到网页下载
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="teachers.xlsx"'
        return response


from django.db import models
from tinymce.models import HTMLField


class Teacher(models.Model):
    teacherNo = models.CharField(max_length=30, default='', primary_key=True, verbose_name='教师编号')
    password = models.CharField(max_length=30, default='', verbose_name='登录密码')
    name = models.CharField(max_length=20, default='', verbose_name='姓名')
    sex = models.CharField(max_length=4, default='', verbose_name='性别')
    birthDate = models.CharField(max_length=20, default='', verbose_name='出生日期')
    teacherPhoto = models.ImageField(upload_to='img', max_length='100', verbose_name='老师照片')
    zhicheng = models.CharField(max_length=20, default='', verbose_name='职称')
    telephone = models.CharField(max_length=20, default='', verbose_name='联系电话')
    comeDate = models.CharField(max_length=20, default='', verbose_name='入职日期')
    address = models.CharField(max_length=80, default='', verbose_name='家庭地址')
    teacherDesc = HTMLField(max_length=5000, verbose_name='老师介绍')

    class Meta:
        db_table = 't_Teacher'
        verbose_name = '老师信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        teacher = {
            'teacherNo': self.teacherNo,
            'password': self.password,
            'name': self.name,
            'sex': self.sex,
            'birthDate': self.birthDate,
            'teacherPhoto': self.teacherPhoto.url,
            'zhicheng': self.zhicheng,
            'telephone': self.telephone,
            'comeDate': self.comeDate,
            'address': self.address,
            'teacherDesc': self.teacherDesc,
        }
        return teacher


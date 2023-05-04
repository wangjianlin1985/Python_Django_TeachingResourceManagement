from django.db import models
from apps.ResourceType.models import ResourceType
from apps.Teacher.models import Teacher
from tinymce.models import HTMLField


class Resource(models.Model):
    resourceId = models.AutoField(primary_key=True, verbose_name='资源id')
    resourceTypeObj = models.ForeignKey(ResourceType,  db_column='resourceTypeObj', on_delete=models.PROTECT, verbose_name='资源类型')
    resourceName = models.CharField(max_length=50, default='', verbose_name='资源名称')
    resourcePhoto = models.ImageField(upload_to='img', max_length='100', verbose_name='资源缩略图')
    resourceDesc = HTMLField(max_length=8000, verbose_name='资源介绍')
    resourceFile = models.FileField(upload_to='file', max_length='100', verbose_name='资料文件')
    teacherObj = models.ForeignKey(Teacher,  db_column='teacherObj', on_delete=models.PROTECT, verbose_name='上传老师')
    uploadTime = models.CharField(max_length=20, default='', verbose_name='上传日期')
    shenHeState = models.CharField(max_length=20, default='', verbose_name='审核状态')
    shenHeReply = models.CharField(max_length=800, default='', verbose_name='审核回复')

    class Meta:
        db_table = 't_Resource'
        verbose_name = '教学资源信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        resource = {
            'resourceId': self.resourceId,
            'resourceTypeObj': self.resourceTypeObj.typeName,
            'resourceTypeObjPri': self.resourceTypeObj.typeId,
            'resourceName': self.resourceName,
            'resourcePhoto': self.resourcePhoto.url,
            'resourceDesc': self.resourceDesc,
            'resourceFile': self.resourceFile.url,
            'teacherObj': self.teacherObj.name,
            'teacherObjPri': self.teacherObj.teacherNo,
            'uploadTime': self.uploadTime,
            'shenHeState': self.shenHeState,
            'shenHeReply': self.shenHeReply,
        }
        return resource


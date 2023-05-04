from django.db import models
from apps.Resource.models import Resource
from apps.Teacher.models import Teacher
from apps.UserInfo.models import UserInfo


class ResourceComment(models.Model):
    commentId = models.AutoField(primary_key=True, verbose_name='评论id')
    resourceObj = models.ForeignKey(Resource,  db_column='resourceObj', on_delete=models.PROTECT, verbose_name='被评资源')
    teacherObj = models.ForeignKey(Teacher,  db_column='teacherObj', on_delete=models.PROTECT, verbose_name='资源发布人')
    commentScore = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='评分')
    content = models.CharField(max_length=1000, default='', verbose_name='评论内容')
    userObj = models.ForeignKey(UserInfo,  db_column='userObj', on_delete=models.PROTECT, verbose_name='评论用户')
    commentTime = models.CharField(max_length=20, default='', verbose_name='评论时间')

    class Meta:
        db_table = 't_ResourceComment'
        verbose_name = '资源评论信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        resourceComment = {
            'commentId': self.commentId,
            'resourceObj': self.resourceObj.resourceName,
            'resourceObjPri': self.resourceObj.resourceId,
            'teacherObj': self.teacherObj.name,
            'teacherObjPri': self.teacherObj.teacherNo,
            'commentScore': self.commentScore,
            'content': self.content,
            'userObj': self.userObj.name,
            'userObjPri': self.userObj.user_name,
            'commentTime': self.commentTime,
        }
        return resourceComment


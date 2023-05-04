from django.db import models
from apps.Teacher.models import Teacher
from apps.UserInfo.models import UserInfo


class TeacheFollow(models.Model):
    followId = models.AutoField(primary_key=True, verbose_name='订阅id')
    teacherObj = models.ForeignKey(Teacher,  db_column='teacherObj', on_delete=models.PROTECT, verbose_name='被订阅老师')
    userObj = models.ForeignKey(UserInfo,  db_column='userObj', on_delete=models.PROTECT, verbose_name='订阅人')
    followTime = models.CharField(max_length=20, default='', verbose_name='订阅时间')

    class Meta:
        db_table = 't_TeacheFollow'
        verbose_name = '老师订阅信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        teacheFollow = {
            'followId': self.followId,
            'teacherObj': self.teacherObj.name,
            'teacherObjPri': self.teacherObj.teacherNo,
            'userObj': self.userObj.name,
            'userObjPri': self.userObj.user_name,
            'followTime': self.followTime,
        }
        return teacheFollow


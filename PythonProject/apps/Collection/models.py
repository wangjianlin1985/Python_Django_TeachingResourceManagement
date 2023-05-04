from django.db import models
from apps.Resource.models import Resource
from apps.UserInfo.models import UserInfo


class Collection(models.Model):
    collectionId = models.AutoField(primary_key=True, verbose_name='收藏id')
    resourceObj = models.ForeignKey(Resource,  db_column='resourceObj', on_delete=models.PROTECT, verbose_name='收藏的资源')
    userObj = models.ForeignKey(UserInfo,  db_column='userObj', on_delete=models.PROTECT, verbose_name='收藏用户')
    collectTime = models.CharField(max_length=20, default='', verbose_name='收藏时间')

    class Meta:
        db_table = 't_Collection'
        verbose_name = '资源收藏信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        collection = {
            'collectionId': self.collectionId,
            'resourceObj': self.resourceObj.resourceName,
            'resourceObjPri': self.resourceObj.resourceId,
            'userObj': self.userObj.name,
            'userObjPri': self.userObj.user_name,
            'collectTime': self.collectTime,
        }
        return collection


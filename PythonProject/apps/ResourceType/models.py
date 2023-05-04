from django.db import models


class ResourceType(models.Model):
    typeId = models.AutoField(primary_key=True, verbose_name='类型id')
    typeName = models.CharField(max_length=20, default='', verbose_name='类型名称')
    typeDesc = models.CharField(max_length=800, default='', verbose_name='类型描述')

    class Meta:
        db_table = 't_ResourceType'
        verbose_name = '资源类型信息'
        verbose_name_plural = verbose_name

    def getJsonObj(self):
        resourceType = {
            'typeId': self.typeId,
            'typeName': self.typeName,
            'typeDesc': self.typeDesc,
        }
        return resourceType


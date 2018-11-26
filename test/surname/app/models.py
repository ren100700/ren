from django.db import models

class Name(models.Model):

	name = models.CharField(max_length=100,verbose_name='名字')
	family_name = models.CharField(max_length=30,verbose_name='姓')

	class Meta:
		db_table = 'name'

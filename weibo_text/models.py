#coding:utf-8

from django.db import models
from datetime import datetime


class User(models.Model):
	uid = models.CharField(max_length=256)
	access_token = models.CharField(max_length=256)
	expires_in   = models.CharField(max_length=256)

class User_xinxi(models.Model):
	uid = models.CharField(max_length=256)
	user_name = models.CharField(max_length=256)
	add = models.CharField(max_length=256)
	followers_count = models.CharField(max_length=256)
	friends_count = models.CharField(max_length=256)

class Relation(models.Model):
	uid = models.CharField(max_length=256)
	rid = models.CharField(max_length=256)
	content = models.IntegerField()

class Group(models.Model):
	FICATION_CHOICE=(
		('leve1','购物'),
		('leve2','影视音乐'),
		('leve3','游戏'),
		('leve4','车行天下'),
		('leve5','动漫'),
		('leve6','考试/培训'),
		('leve7','体育联盟'),
		('leve8','职业交流'),
		('leve9','技术联盟'),
       		('leve10','老乡会'),
	    	('leve11','旅游'),
	  	('leve12','读书会'),
        	('leve13','生活休闲'),
        	('leve14','其他'),
	)

	CONTENT_CHOICE=(
		('leve1','50'),
		('leve2','100'),
		('leve3','200'),
	)
	name = models.CharField(max_length=512)
	fication = models.CharField(max_length=256,choices=FICATION_CHOICE)
	introduce = models.CharField(max_length=1024)
	master = models.CharField(max_length=256)
	content = models.CharField(max_length=10)
	max_content = models.CharField(max_length=10,choices=CONTENT_CHOICE)
	Create_time = models.DateTimeField(default=datetime.now, blank=True)

class G_u(models.Model):
	gid = models.CharField(max_length=20)
	uid = models.CharField(max_length=256)

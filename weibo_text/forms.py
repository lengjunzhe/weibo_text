#coding:utf-8
from django import forms

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


class Group_f(forms.Form):
        name = forms.CharField(max_length=512,label="群组名称")
	fication = forms.ChoiceField(choices=FICATION_CHOICE,label='选择分类')
        max_content = forms.ChoiceField(choices=CONTENT_CHOICE,label='最大人数')
        introduce = forms.CharField(label='群组简介',widget=forms.Textarea)

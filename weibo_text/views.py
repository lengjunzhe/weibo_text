#coding:utf-8

from weibo import APIClient
from django.shortcuts import render_to_response
from django.template import *
from django.http import HttpResponse
from django.template import RequestContext
from django.http import HttpResponseRedirect
import json

from weibo_text.models import *
from weibo_text.forms import *
from datetime import datetime

key = '3347048200'
secret = 'ef52a2fe2c3608ab3442d1fec2a931a6'
callback_url = 'http://192.168.2.107:8000/login'
l = []

def weibo_login(request):#获取CODE
	global key,secret,callback_url
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
	url = client.get_authorize_url()
	return render_to_response('index_1.html',{'url':url})

def weibo_login2(request):
	global key,secret,callback_url
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
	if 'code' in request.GET:#获取token
		code = request.GET['code']
		#print code
		r = client.request_access_token(code)
		access_token = r.access_token 
		expires_in = r.expires_in 
		client.set_access_token(access_token, expires_in)
		request.session['access_token'] = access_token
		request.session['expires_in']   = expires_in
		r1 = client.account.get_uid.get()
		uid = str(r1.uid)
		try:
			s = User.objects.get(uid=uid)
			s.access_token=access_token
			s.expires_in=expires_in
			s.save()
		except:
			p = User(uid=uid,access_token=access_token,expires_in=expires_in) 
                        p.save()
		#request.session['client']   = client
	return render_to_response('dc.html')

def weibo_index(request):#登录，将登录信息存库，获取登录者信息
	global key,secret,callback_url
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
	access_token = request.session['access_token']
	expires_in   = request.session['expires_in']
	#client   = request.session['client']
	client.set_access_token(access_token, expires_in)
	r1 = client.account.get_uid.get()
	uid = str(r1.uid)
	r2 = client.statuses.user_timeline.get()
	user_name = r2.statuses[0]['user']['screen_name']
	weibo_last = r2.statuses[0]['text']
	#r3 = client.users.show.get(uid='2786353221')
	return render_to_response('index.html',{'uid':uid,'user_name':user_name,'weibo_last':weibo_last})#,'r4':r3['status']['text']})

def friendships(request,uid):#关注
	global key,secret,callback_url,l
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
	access_token = request.session['access_token']
	expires_in   = request.session['expires_in']
	client.set_access_token(access_token, expires_in)
	client.friendships.create.post(uid=uid)
	return HttpResponse('关注成功！')

def user1(request):#将用户信息在页面中显示出来
	global l
	q = User.objects.all()
	access_token = request.session['access_token']
	#print access_token
	p = User.objects.get(access_token=access_token)
	for n in q:
		if int(n.uid) not in l:
			l.append(int(n.uid))
	l.remove(int(p.uid))
	print l
	return  render_to_response('user1.html',{'l':l,'access_token':access_token})

def allfollow(request):#一键关注
	global l,key,secret,callback_url
	print l
	l2 = []
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
        access_token = request.session['access_token']
        expires_in   = request.session['expires_in']
        client.set_access_token(access_token, expires_in)
	p = User.objects.get(access_token=access_token)
	for n in l:
		r = client.friendships.show.get(source_id=int(p.uid),target_id=int(n))
		print r
		if r['target']['followed_by'] ==  False:
			l2.append(int(n))
	print l2

	for m in l2:
		client.friendships.create.post(uid=m)
	a = len(l2)
	return render_to_response('follow.html',{'a':a})

def follow_byid(request):#互相关注
	global l,key,secret,callback_url

	if 'uid' in request.GET:
		uid = request.GET['uid']
	client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
        access_token = request.session['access_token']
        expires_in   = request.session['expires_in']
	q = User.objects.get(access_token=access_token)
        client.set_access_token(access_token, expires_in)
	try:	
		client.friendships.create.post(uid=uid)
	except:
		pass
	p = User.objects.get(uid=uid)
	access_token = p.access_token
        expires_in   = p.expires_in
        client.set_access_token(access_token, expires_in)
	try:
		 client.friendships.create.post(uid=q.uid)
	except:
		pass
	return HttpResponse(json.dumps({"id":uid}),mimetype='application/json')

def group_found(request):
	f = Group_f()
	return render_to_response('group(1).html', {'f': f},context_instance=RequestContext(request))

def group_show(request):
	global key,secret,callback_url,l
        client = APIClient(app_key=key,app_secret=secret,redirect_uri=callback_url)
        access_token = request.session['access_token']
        expires_in   = request.session['expires_in']
        client.set_access_token(access_token, expires_in)
        r = client.statuses.user_timeline.get()
	if request.method == 'POST':
		try:
			Group.objects.get(name=request.POST['text'])
		except:
                	q = Group(name=request.POST['text'],master=r.statuses[0]['user']['screen_name'],fication=request.POST['fication'],introduce=request.POST['message'],max_content=request.POST['max_content'],Create_time=datetime.now())
                	q.save()
               		p = G_u(gid=q.id,uid=r.statuses[0]['user']['id'])
                	p.save()
			return HttpResponseRedirect("/group/group_show/")
	q = Group.objects.all()
	q = list(q)
	q12 =[]
	for i in range(0,len(q),2):
		q12.append(q[i:i+2])
	return render_to_response('group_show_2.html', {'q12':q12})

def group_list(request,gid):
	g_l = []
	access_token = request.session['access_token']
	s = User.objects.get(access_token=access_token)
	try:
		r = G_u.objects.filter(gid=gid)
		for n in r:
			if int(n.uid) not in g_l:
				g_l.append(int(n.uid))
	except:
		pass
	try:
		G_u.objects.get(uid=s.uid)
		g_content = 1
	except:
		g_content = 0
	q = Group.objects.get(id=gid)
	name=q.name
	master = q.master
	introduce = q.introduce
	fication = q.get_fication_display()
	content = group_content(gid)
	max_content = q.get_max_content_display()
	Create_time = q.Create_time
	return render_to_response('group_show_1.html',{'l':g_l,'name':name,'master':master,'introduce':introduce,'fication':fication,'content':content,'max_content':max_content,'Create_time':Create_time,'access_token':access_token,'g_content':g_content,'group_id':gid,'myid':s.uid})

def group_append(request,gid):
        access_token = request.session['access_token']
        expires_in   = request.session['expires_in']
	r = User.objects.get(access_token=access_token)
	try:
		G_u.objects.get(gid=gid,uid=r.uid)
		return HttpResponse(json.dumps({"code":1}))
	except:
		s = G_u(gid=gid,uid=r.uid)
		s.save()
		return HttpResponse(json.dumps({"code":0}))

def group_content(gid):
	q = G_u.objects.filter(gid=gid)
	l1 = []
	for i in q:
		l1.append(int(i.uid))
	return len(l1)
def group_join(request,gid):
	access_token = request.session['access_token']
        expires_in   = request.session['expires_in']
        r = User.objects.get(access_token=access_token)
	myid = r.uid
	group_id =gid
	print gid
	return HttpResponse(json.dumps({"myid":myid,"group_id":group_id}),mimetype='application/json')
	

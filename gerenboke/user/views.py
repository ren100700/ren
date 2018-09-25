from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
	if request.method=='GET':
		return render(request,'index.html')


def share(request):
	if request.method=='GET':
		return render(request,'share.html')


def about(request):
	if request.method=='GET':
		return render(request,'about.html')


def gbook(request):
	if request.method=='GET':
		return render(request,'gbook.html')


def info(request):
	if request.method=='GET':
		return render(request,'info.html')


def list(request):
	if request.method=='GET':
		return render(request,'list.html')
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.core.paginator import Paginator

from app.models import Name
from surname.settings import PAGE_NUMBER


def index(request):
	if request.method == 'GET':
		page_number = int(request.GET.get('page',1))
		all_names = Name.objects.all()
		pages = Paginator(all_names,PAGE_NUMBER)
		page = pages.page(page_number)
		return render(request,'index.html',{'page':page})

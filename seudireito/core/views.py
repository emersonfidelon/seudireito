#coding=utf-8

from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    template_name = 'index.html'
    context = {
        'title': 'Seu Direito'
    }
    return render(request, template_name, context)

#!/usr/bin/python
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse


def index(request):
	return render(request, 'index.html')

def about(request):
	return render(request, 'about.html')

def upload(request):
	return render(request, 'upload.html')
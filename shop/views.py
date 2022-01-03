from django.shortcuts import render


def home_page(request):
	contex = {}
	return render(request, 'home_page.html', contex)
from django.shortcuts import render


def index(request, slug=None):
    return render(request, 'menus/index.html', {'slug': slug})

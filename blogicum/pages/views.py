from django.shortcuts import render


def about(request):
    return render(request, 'pages/about.html')


def rules(request):
    return render(request, 'pages/rules.html')


def not_found(request):
    return render(request, 'pages/404.html')


def forbidden(request):
    return render(request, 'pages/403csrf.html')


def server_error(request):
    return render(request, 'pages/500.html')

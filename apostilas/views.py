from django.http import Http404
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.messages import constants
from .models import *

def adicionar_apostilas(request):
    if request.method == 'GET':
        apostilas = Apostila.objects.filter(user=request.user)
        return render(request, 'adicionar_apostila.html', {'apostilas' : apostilas})

    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        arquivo = request.FILES['arquivo']

        apostila = Apostila(user=request.user, titulo=titulo, arquivo=arquivo)
        apostila.save()

        views_totais = ViewApostila.objects.filter(apostila__user = request.user).count()

        messages.add_message(request, constants.SUCCESS, 'Apostila adicionada com sucesso.')

        return redirect('/apostilas/adicionar_apostilas/')    


def apostila(request, id):
    apostila = Apostila.objects.get(id=id)

    view = ViewApostila(
        ip=request.META['REMOTE_ADDR'],
        apostila=apostila
    )
    view.save()

    views_unicas = ViewApostila.objects.filter(apostila=apostila).values('ip').distinct().count()
    views_totais = ViewApostila.objects.filter(apostila=apostila).count()

    return render(request, 'apostila.html', {'apostila' : apostila}, )



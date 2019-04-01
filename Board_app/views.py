from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    return render(request, 'Board_app/home.html',{'boards':boards})

def board_topics(request, id):
    try:
        board = Board.objects.get(pk=id)
    except:
        raise Http404
    return render(request, 'Board_app/topics.html', {'board':board})

def new_topic(request,id):
    board = get_object_or_404(Board, pk=id)
    user = User.objects.first()
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save()
            post = Post(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )
            return redirect("Board_app:topics",id=id)
    else:
        form = NewTopicForm()
    return render(request, 'Board_app/new_topic.html', {'board': board, 'form': form})
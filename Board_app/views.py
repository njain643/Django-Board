from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.http import HttpResponse, Http404
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib import messages
from .serializers import BoardSerializer
from rest_framework import generics

def home(request):
    boards = Board.objects.all()
    return render(request, 'Board_app/home.html',{'boards':boards})

def board_topics(request, id):
    try:
        board = Board.objects.get(pk=id)
        topics = board.topics.order_by('-last_updated').annotate(replies=Count('posts') - 1)
    except:
        raise Http404
    return render(request, 'Board_app/topics.html', {'board':board, 'topics':topics})

@login_required(login_url='/login/')
def new_topic(request,id):
    board = get_object_or_404(Board, pk=id)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = request.user
            topic.save()
            post = Post(
                message = form.cleaned_data.get('message'),
                topic = topic,
                created_by = request.user
            )
            post.save()
            return redirect("Board_app:topics",id=id)
    else:
        form = NewTopicForm()
    return render(request, 'Board_app/new_topic.html', {'board': board, 'form': form})

def topic_posts(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk = board_id, pk=topic_id)
    topic.views += 1
    topic.save()
    return render(request, 'Board_app/topic_post.html', {'topic': topic})

@login_required(login_url='/login/')
def reply_post(request, board_id, topic_id):
    topic = get_object_or_404(Topic, board__pk = board_id, pk=topic_id)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.message = form.cleaned_data.get('message')
            post.topic = topic
            post.created_by = request.user
            post.save()
            return redirect("Board_app:topic_posts", board_id = board_id, topic_id=topic_id)
    else:
        form = PostForm()
    return render(request, 'Board_app/reply_post.html', {'topic':topic,'form':form})

@login_required(login_url='/login/')
def myaccount(request):
    user = request.user
    if request.method == 'POST':
        if user.first_name != request.POST['fname'] or user.last_name != request.POST['lname']:
            try:
                user.first_name = request.POST['fname']
                user.last_name = request.POST['lname']
                user.save()
                messages.success(request, 'Saved successfully')
            except:
                messages.success(request, 'Something wrong!!!')
   
    return render(request, 'Board_app/myaccount.html', {'user':user,'userimage':MyAccount.objects.filter(user=request.user).order_by('uploaded_image_at').last().userimage})

def imageupload(request):
    if request.method == 'POST':
        myfile = request.FILES['myfile']
        myaccount = MyAccount(user = request.user, userimage = myfile)
        myaccount.save()

    return render(request, 'Board_app/myaccount.html',{'userimage':MyAccount.objects.filter(user=request.user).order_by('uploaded_image_at').last().userimage})

class ListBoardView(generics.ListAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
from django.urls import path
from . import views

app_name = 'Board_app'

urlpatterns=[
    path('<int:id>/',views.board_topics, name='topics'),
    path('<int:id>/new', views.new_topic, name="new_topic"),
    path('<int:board_id>/topic/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('<int:board_id>/topic/<int:topic_id>/reply/', views.reply_post, name='reply_post')
]

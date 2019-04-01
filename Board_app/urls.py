from django.urls import path
from . import views

app_name = 'Board_app'

urlpatterns=[
    path('<int:id>/',views.board_topics, name='topics'),
    path('<int:id>/new', views.new_topic, name="new_topic")
]

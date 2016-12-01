from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^poll/(?P<question_id>[0-9])/(?P<question_text>.+)', views.question_details),
]
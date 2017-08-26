from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

app_name="polls"
urlpatterns = [
    url(r'(?P<pk>\d+)/$', views.detail, name='poll_detail'),
    url(r'(?P<pk>\d+)/vote$', views.vote, name='poll_vote'),
    url(r'(?P<pk>\d+)/results$', views.results, name='poll_results'),
    url(r'^$',TemplateView.as_view(template_name='poll‌​s/index.html'),name='app_index'),
    url(r'^form$', views.form_test),
]

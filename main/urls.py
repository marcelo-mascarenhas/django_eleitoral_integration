from django.urls import path, include

from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("execucao", views.execution, name="execucao"),
  path("execucao/start_collector/", views.executeCollector, name="executeCollector"),
  path('django-rq/', include('django_rq.urls')),
  path("execucao/stop_collector/", views.stopCollector, name="stopCollector")
]
from django.urls import path, include

from . import views


urlpatterns = [
  path("", views.index, name="index"),
  path("execucao", views.execution, name="execucao"),
  path("execucao/start_collector/", views.executeCollector, name="executeCollector"),
  path("execucao/stop_collector/", views.stopCollector, name="stopCollector"),
  path("configuration", views.Configuration.as_view(), name="configuration"),
  path("analise", views.DataAnalysis.as_view(), name="analise"), 
  path(r"analise/plot/cloudWord/", views.GraphPlots.as_view(plot_type="cloudWord"), name="plotWC"),
  path(r"analise/plot/coOccur/", views.GraphPlots.as_view(plot_type="coOccurrence"), name="plotCO"),
  path(r"api/data/<score>", views.ListUsers.as_view(), name="api-data-hist1"),
]
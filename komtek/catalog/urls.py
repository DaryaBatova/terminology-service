from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^handbooks/$', views.HandbookListView.as_view(), name='handbooks'),
    url(r'^handbook/(?P<pk>\d+)$', views.HandbookDetailView.as_view(), name='handbook-detail'),
    url(r'^handbooks_all_versions/$', views.HandbookAllListView.as_view(), name='handbooks-all'),
    url(r'^handbook_all_versions/(?P<pk>\d+)$', views.HandbookVersionDetailView.as_view(), name='handbookversion-detail'),
]

urlpatterns += [
    url(r'^handbook_for_date/(?P<date>.+)/$', views.HandbooksListView.as_view())
]

urlpatterns += [
    path('elements/', views.ElementsListView.as_view())
]

urlpatterns += [
    path('elements_by_title/', views.ElementsByTitleListView.as_view())
]
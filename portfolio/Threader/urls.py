from django.urls import path

from . import views

app_name = 'Threader'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry/', views.InquiryView.as_view(), name="inquiry"),
    path('thread-list/', views.ThreadListView.as_view(), name="thread_list"),
    path('thread-detail/<int:pk>/',
         views.ThreadDetailView.as_view(), name="thread_detail"),
    path('thread-create/', views.ThreadCreateView.as_view(), name="thread_create"),
    path('thread-update/<int:pk>/',
         views.ThreadUpdateView.as_view(), name="thread_update"),
    path('thread-delete/<int:pk>/',
         views.ThreadDeleteView.as_view(), name="thread_delete"),
    path('thread-csv/',
         views.OutputCsv, name="thread_csv"),
    path('thread-cs/',
         views.OutputCsv, name="thread_cs"),
]

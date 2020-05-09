from django.urls import path
from . import views

urlpatterns =[
    path('', views.job_index),
    path('new', views.new_job),
    path('create_new_job', views.create_new_job),
    path('<int:job_id>', views.view_job),
    path('<int:job_id>/edit', views.edit_job),
    path('<int:job_id>/update', views.update_job),
    path('<int:job_id>/remove', views.remove_job)
]
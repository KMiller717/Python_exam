from django.shortcuts import render, redirect
from login_app.models import User
from django.contrib import messages
from .models import Job
# Create your views here.

def job_index(request):
    if not 'user_id' in request.session:
        messages.error(request, "Please log in to view this page")
        print(request.session)
        return redirect('/')
    
    context = {
        'users': User.objects.all(),
        'jobs': Job.objects.all()
    }
    return render(request, 'job_index.html', context)

def new_job(request):
    return render(request, 'new_job.html')

def create_new_job(request):
    errors = Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/job/new')
    
    user = User.objects.get(id=request.session['user_id'])
    
    job = Job.objects.create(title=request.POST['title'], location=request.POST['location'], description = request.POST['description'], creator=user)


    return redirect('/job')

def view_job(request, job_id):
    context = {
        'job' : Job.objects.get(id=job_id)
    }
    return render(request, 'view_job.html', context)

def edit_job(request, job_id):
    
    context = {
        'job': Job.objects.get(id=job_id)
    }
    return render(request, 'edit_job.html', context)

def update_job(request, job_id):
    errors = Job.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/job/{job_id}/edit')
    
    updated_job = Job.objects.get(id=job_id)
    updated_job.title = request.POST['title']
    updated_job.description = request.POST['description']
    updated_job.location = request.POST['description']
    updated_job.save()

    return redirect(f'/job')

def remove_job(request, job_id):
    job_delete = Job.objects.get(id=job_id)
    job_delete.delete()
    return redirect('/job')
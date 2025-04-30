from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from superadmin.models import UserProfile, Task, TaskDetails
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
# Create your views here.
def Homepage(request):
    return render(request, 'index.html')


def signup_view(request):
    return render(request, 'signup.html')


def is_superadmin(user):
    return user.is_superuser

def signin_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        
        if user is not None :
            login(request, user)
            if user.is_superuser:
                return redirect('superadmin_dashboard')  
            elif user.is_staff:
                return redirect('admin_dashboard')
            else:
                return redirect('user_dashboard')
        else:
            messages.error(request, "Invalid credentials or not a superadmin.")

    return render(request, 'login.html')

def superadmin_dashboard(request):
    return render(request, 'superuser/base.html')

def view_admins(request):
    admins = User.objects.filter(is_staff=True, is_superuser=False)  # Or use is_superuser=True if you want only superadmins
    return render(request, 'superuser/view_admins.html', {'admins': admins})

def view_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)  # Or use is_superuser=True if you want only superadmins
    return render(request, 'superuser/view_users.html', {'users': users})

@user_passes_test(lambda u: u.is_superuser)
def add_admin_view(request):
    errors = []
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        context = {
            'username': username,
            'email': email,
            'role': role,
        }

        if password1 != password2:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")
        if not username or not email or not password1 or not role :
            errors.append("All fields are required.")

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password1)

            # Assign based on role
            if role == 'superadmin':
                user.is_superuser = True
                user.is_staff = True
            elif role == 'admin':
                user.is_staff = True
            elif role == 'user':
                user.is_superuser = False
                user.is_staff = False
            user.save()

            UserProfile.objects.create(user=user, role=role)

            messages.success(request, f"{role.capitalize()} '{username}' created successfully.")
            return redirect('view_admins')

    context['errors'] = errors
    return render(request, 'superadmin/add_admins.html', context)

@user_passes_test(lambda u: u.is_superuser)
def delete_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id)
    admin.delete()
    messages.success(request, f"Admin '{admin.username}' has been deleted successfully.")
    return redirect('view_admins')

@user_passes_test(lambda u: u.is_superuser)
def update_admin(request, admin_id):
    admin = get_object_or_404(User, id=admin_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exclude(id=admin.id).exists():
            messages.error(request, "Username already exists.")
            return redirect('update_admin', admin_id=admin.id)
        
        if User.objects.filter(email=email).exclude(id=admin.id).exists():
            messages.error(request, "Email already exists.")
            return redirect('update_admin', admin_id=admin.id)
        
        admin.username = username
        admin.email = email

        # Update role (superadmin or admin)
        if role == 'superadmin':
            admin.is_superuser = True
            admin.is_staff = True
        elif role == 'admin':
            admin.is_superuser = False
            admin.is_staff = True
        elif role == 'user':
            admin.is_superuser = False
            admin.is_staff = False
        
        
        admin.save()
        
        messages.success(request, f"Admin '{admin.username}' updated successfully.")
        return redirect('view_admins')

    return render(request, 'superadmin/update_admin.html', {'admin': admin})


@user_passes_test(lambda u: u.is_superuser)
def add_users_view(request):
    errors = []
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')

        context = {
            'username': username,
            'email': email,
            'role': role,
        }

        if password1 != password2:
            errors.append("Passwords do not match.")
        if User.objects.filter(username=username).exists():
            errors.append("Username already exists.")
        if User.objects.filter(email=email).exists():
            errors.append("Email already registered.")
        if not username or not email or not password1 or not role :
            errors.append("All fields are required.")

        if not errors:
            user = User.objects.create_user(username=username, email=email, password=password1)

            if role == 'superadmin':
                user.is_superuser = True
                user.is_staff = True
            elif role == 'admin':
                user.is_staff = True
            elif role == 'user':
                user.is_superuser = False
                user.is_staff = False
            user.save()

            UserProfile.objects.create(user=user, role=role)

            messages.success(request, f"{role.capitalize()} '{username}' created successfully.")
            return redirect('view_users')

    context['errors'] = errors
    return render(request, 'superadmin/add_admins.html', context)


@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    messages.success(request, f"User '{user.username}' has been deleted successfully.")
    return redirect('view_users')


@user_passes_test(lambda u: u.is_superuser)
def update_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        role = request.POST.get('role')
        
        if User.objects.filter(username=username).exclude(id=user.id).exists():
            messages.error(request, "Username already exists.")
            return redirect('update_user', user_id=user.id)
        
        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.error(request, "Email already exists.")
            return redirect('update_user', user_id=user.id)
        
        user.username = username
        user.email = email

        if role == 'superadmin':
            user.is_superuser = True
            user.is_staff = True
        elif role == 'admin':
            user.is_superuser = False
            user.is_staff = True
        elif role == 'user':
            user.is_superuser = False
            user.is_staff = False
        
        
        user.save()
        
        messages.success(request, f"User '{user.username}' updated successfully.")
        return redirect('view_users')

    return render(request, 'superadmin/update_user.html', {'user': user})

def logout_view(request):
    logout(request)
    return redirect('home')


def admin_dashboard(request):
    return render(request, 'admin/base.html')

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        assigned_to_id = request.POST['assigned_to']
        due_date = request.POST['due_date']
        status = request.POST['status']
        completion_report = request.POST.get('completion_report', '')
        worked_hours = request.POST.get('worked_hours', 0)

        assigned_user = User.objects.get(id=assigned_to_id)

        TaskDetails.objects.create(
            title = title,
            description = description,
            assigned_to = assigned_user,
            created_by=request.user,
            due_date = due_date,
            status = status,
            completion_report = completion_report,
            worked_hours = worked_hours
        )
        return redirect('view_tasks')

    users = User.objects.filter(is_staff=False)
    return render(request, 'admin/add_task.html', {'users': users})
    
# @login_required
# def view_tasks(request):
#     if request.user.is_superuser:
#         tasks = TaskDetails.objects.all()  
#     elif request.user.is_staff:
#         tasks = TaskDetails.objects.filter(assigned_to=request.user)  
#     else:
#         tasks = TaskDetails.objects.filter(assigned_to=request.user)
#     return render(request, 'admin/view_task.html', {'tasks': tasks})



@login_required
def view_tasks(request):
    user = request.user

    if user.is_superuser:
        tasks = TaskDetails.objects.all()
        return render(request, 'superuser/view_task.html', {'tasks': tasks})
    elif user.is_staff:
        tasks = TaskDetails.objects.filter(created_by=user)
    else:
        tasks = TaskDetails.objects.filter(assigned_to=user)
    return render(request, 'admin/view_task.html', {'tasks': tasks})

def delete_task(request, id):
    task = get_object_or_404(TaskDetails, id=id)
    task.delete()  
    return redirect('view_tasks')

def update_task(request, id):
    task = get_object_or_404(TaskDetails, id=id)
    users = User.objects.filter(is_staff=False)

    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.description = request.POST.get('description', task.description)
        task.assigned_to_id = request.POST.get('assigned_to', task.assigned_to_id)
        task.due_date = request.POST.get('due_date', task.due_date)
        task.status = request.POST.get('status', task.status)
        task.worked_hours = request.POST.get('worked_hours', task.worked_hours)
        task.completion_report = request.POST.get('completion_report', task.completion_report)

        task.save()
        return redirect('view_tasks')  

    return render(request, 'admin/update_task.html', {'task': task, 'users': users})

def admin_view_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)  # Or use is_superuser=True if you want only superadmins
    return render(request, 'admin/admin_view_users.html', {'users': users})

@login_required
def manage_tasks(request):
    tasks = Task.objects.filter(assigned_to=request.user)
    return render(request, 'tasks/manage_tasks.html', {'tasks': tasks})

@login_required
def view_task_report(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.user.is_superuser:  
        return render(request, 'tasks/task_report.html', {'task': task})
    else:
        return HttpResponseForbidden("You are not authorized to view this report.")

def user_dashboard(request):
    return render(request, 'users/user_dashboard.html')

@login_required
def user_tasks(request):
    tasks = TaskDetails.objects.filter(assigned_to=request.user)
    return render(request, 'users/user_view_task.html', {'tasks': tasks})

@login_required
def update_user_task(request, task_id):
    task = get_object_or_404(TaskDetails, id=task_id, assigned_to=request.user)

    if request.method == 'POST':
        task.status = request.POST['status']
        task.completion_report = request.POST['completion_report']
        task.worked_hours = request.POST['worked_hours']
        task.save()
        return redirect('user_tasks')

    return render(request, 'users/user_update_task.html', {'task': task})

def view_completion_reports(request):
    if request.user.is_superuser:
        tasks = TaskDetails.objects.all()  
    elif request.user.is_staff:
        tasks = TaskDetails.objects.filter(status='Completed')
    else:
        # tasks = TaskDetails.objects.all()  

        tasks = TaskDetails.objects.filter(created_by = request.user,status='Completed' )  

    return render(request, 'admin/task_completion_report.html', {'tasks': tasks})


@login_required
def api_get_user_tasks(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    tasks = TaskDetails.objects.filter(assigned_to=request.user)
    data = list(tasks.values('id', 'title', 'description', 'status', 'due_date'))
    return JsonResponse({'tasks': data}, status=200)


@login_required
def api_update_task_status(request, task_id):
    if request.method != 'PUT':
        return JsonResponse({'error': 'Only PUT allowed'}, status=405)

    try:
        task = TaskDetails.objects.get(id=task_id, assigned_to=request.user)
    except TaskDetails.DoesNotExist:
        return JsonResponse({'error': 'Task not found or not assigned to you'}, status=404)

    try:
        body = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    new_status = body.get('status')
    report = body.get('completion_report')
    hours = body.get('worked_hours')

    if new_status == 'Completed':
        if not report or not hours:
            return JsonResponse({'error': 'Completion report and worked hours required to complete task'}, status=400)
        try:
            task.status = 'Completed'
            task.completion_report = report
            task.worked_hours = float(hours)
            task.completed_at = now()
            task.save()
        except ValueError:
            return JsonResponse({'error': 'Worked hours must be a valid number'}, status=400)
    else:
        task.status = new_status
        task.save()

    return JsonResponse({'message': 'Task updated successfully'}, status=200)

@login_required
def api_task_report(request, task_id):
    if request.method != 'GET':
        return JsonResponse({'error': 'Only GET allowed'}, status=405)

    if not (request.user.is_staff or request.user.is_superuser):
        return JsonResponse({'error': 'Access denied'}, status=403)

    try:
        task = TaskDetails.objects.get(id=task_id)
    except TaskDetails.DoesNotExist:
        return JsonResponse({'error': 'Task not found'}, status=404)

    if task.status != 'Completed':
        return JsonResponse({'error': 'Task is not completed yet'}, status=400)

    return JsonResponse({
        'title': task.title,
        'assigned_to': task.assigned_to.username,
        'completion_report': task.completion_report,
        'worked_hours': task.worked_hours,
        'completed_at': task.completed_at,
    }, status=200)

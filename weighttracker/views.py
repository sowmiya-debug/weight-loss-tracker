from django.shortcuts import render, redirect, get_object_or_404
from .forms import WeightEntryForm, SignUpForm
from .models import WeightEntry
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import date
from django.utils.timezone import now
from django.http import HttpResponse

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('weight_list')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def add_weight(request):
    today = timezone.now().date()

    start_date= now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date= now().replace(hour=23, minute=59, second=59, microsecond=999999)
    already_exists= WeightEntry.objects.filter(user=request.user,date_added__range=
                                       (start_date, end_date)).exists()
    """print(events_in_range)
    print( WeightEntry.objects.filter(user=request.user,date_added__range=(start_date,end_date)))
    already_exists = WeightEntry.objects.filter(user=request.user,date_added__date= today).exists()"""
    if already_exists:
        return render(request, 'weight_form.html', {'form':WeightEntryForm(),
            'error': 'You have already added weight today.'
        })

    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry= form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.date_added = today
            weight_entry.save()
            return redirect('weight_list')
    else:
        form = WeightEntryForm()
    return render(request, 'weight_form.html', {'form': form})

@login_required
def weight_list(request):
    weights = WeightEntry.objects.filter(user=request.user)

    if request.method =="POST":
     start= request.GET.get('start')+"00:00:00"
     end= request.GET.get('end')+"23:59:59"
     if start and end:
        weights = weights.filter(date_added__range=[start, end])

    paginator = Paginator(weights.order_by('-date_added'), 1)
    page = request.GET.get('page')
    weights_page = paginator.get_page(page)
    return render(request, 'weight_list.html', {'weights': weights_page})

@login_required
def edit_weight(request, pk):
    entry = WeightEntry.objects.get(pk=pk, user=request.user)
    if request.method == 'POST':
        form = WeightEntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('weight_list')
    else:
        form = WeightEntryForm(instance=entry)
    return render(request, 'weight_form.html', {'form': form})

@login_required
def delete_weight(request, pk):
    entry = get_object_or_404(WeightEntry,pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('weight_list')
    return render(request,'delete.html',{'entry':entry})

@login_required
def compare_weight(request):
    result=None
    if request.method == 'POST':
        
             from datetime import datetime
             start_str = request.POST.get('start_date')+" 00:00:00"
             end_str = request.POST.get('end_date')+" 23:59:59"

             start_date=datetime.strptime(start_str,"%Y-%m-%d %H:%M:%S")
             end_date=datetime.strptime(end_str,"%Y-%m-%d %H:%M:%S")

             print(start_date)
             print(end_date)
             weights=WeightEntry.objects.filter(user=request.user,date_added__range=(start_date,end_date)).order_by('date_added')
             print(weights)

             if weights.exists():
                 weight_diff=weights.last().weight-weights.first().weight
                 if weight_diff > 0:
                     result = "You  gained " + str(weight_diff) + " Kgs"
                 else:
                     result =  "You  lost " + str(weight_diff) + " Kgs" 
             else:
                 result= "no records found in that range."
       
    return render(request,'weight_compare.html',{'result':result})



    """today = timezone.now().date()
    yesterday = today - timezone.timedelta(days=1)

    today_entry = WeightEntry.objects.filter(user=user, date_added=today).first()
    yesterday_entry = WeightEntry.objects.filter(user=user, date_added=yesterday).first()

    if today_entry and yesterday_entry:
        diff = today_entry.weight - yesterday_entry.weight
        if diff > 0:
            message= "You gained {:.1f} kg".format(diff)
        elif diff < 0:
            message= "You lost {:.1f} kg".format(-diff)
        else:
            message= "No weight change"
    else:
     message= "Not enough data to compare"

    return HttpResponse(message)"""



"""@login_required
def add_weight(request):

    start= now().replace(hour=0, minute=0, second=0, microsecond=0)
    end= now().replace(hour=23, minute=59, second=59, microsecond=999999)

    existing = WeightEntry.objects.filter(user=request.user, date_added__range=(start, end))
    if existing.exists():
        return render(request, 'weight_form.html', {'message': 'You have already added weight for today.'})

    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('weight_list')
    else:
        form = WeightEntryForm()
    return render(request, 'weight_form.html', {'form': form})



"""
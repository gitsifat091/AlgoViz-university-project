# from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

def home(request):
    return redirect('dashboard' if request.user.is_authenticated else 'login')

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    sorting_algorithms = [
        ("Bubble Sort",    "🫧", "bubble_sort"),
        ("Selection Sort", "🎯", "selection_sort"),
        ("Insertion Sort", "📥", "insertion_sort"),
        ("Merge Sort",     "🔀", "merge_sort"),
        ("Quick Sort",     "⚡", "quick_sort"),
    ]
    algorithms = [
        ("A* Search", "🎯"),
    ]
    return render(request, 'accounts/dashboard.html', {
        'sorting_algorithms': sorting_algorithms,
        'algorithms': algorithms,
    })
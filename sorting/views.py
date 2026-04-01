# from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def bubble_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            steps.append({
                'array': arr[:],
                'comparing': [j, j+1],
                'sorted_from': n - i
            })
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({
                    'array': arr[:],
                    'swapped': [j, j+1],
                    'sorted_from': n - i
                })
    steps.append({'array': arr[:], 'done': True, 'sorted_from': 0})
    return steps

@login_required
def bubble_sort_view(request):
    steps = []
    initial = [5, 3, 8, 1, 9, 2]
    if request.method == 'POST':
        raw = request.POST.get('numbers', '')
        try:
            initial = [int(x.strip()) for x in raw.split(',') if x.strip()][:10]
        except:
            pass
    steps = bubble_sort_steps(initial)
    return render(request, 'sorting/bubble_sort.html', {
        'steps': json.dumps(steps),
        'initial': initial,
    })
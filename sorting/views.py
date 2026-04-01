import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# ─── Algorithm Logic ───────────────────────────────────────────

def bubble_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(n):
        for j in range(n - i - 1):
            steps.append({'array': arr[:], 'comparing': [j, j+1], 'sorted_from': n - i})
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                steps.append({'array': arr[:], 'swapped': [j, j+1], 'sorted_from': n - i})
    steps.append({'array': arr[:], 'done': True, 'sorted_from': 0})
    return steps


def selection_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            steps.append({'array': arr[:], 'comparing': [min_idx, j], 'min_idx': min_idx, 'sorted_until': i})
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            steps.append({'array': arr[:], 'swapped': [i, min_idx], 'sorted_until': i})
    steps.append({'array': arr[:], 'done': True})
    return steps


def insertion_sort_steps(arr):
    arr = arr[:]
    steps = []
    n = len(arr)
    for i in range(1, n):
        key = arr[i]
        j = i - 1
        steps.append({'array': arr[:], 'current': i, 'sorted_until': i})
        while j >= 0 and arr[j] > key:
            steps.append({'array': arr[:], 'comparing': [j, j+1], 'sorted_until': i})
            arr[j+1] = arr[j]
            j -= 1
            steps.append({'array': arr[:], 'shifting': j+1, 'sorted_until': i})
        arr[j+1] = key
        steps.append({'array': arr[:], 'placed': j+1, 'sorted_until': i+1})
    steps.append({'array': arr[:], 'done': True})
    return steps


def merge_sort_steps(arr):
    steps = []

    def merge_sort(arr, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid+1, right)
        merge(arr, left, mid, right)

    def merge(arr, left, mid, right):
        left_part = arr[left:mid+1]
        right_part = arr[mid+1:right+1]
        i = j = 0
        k = left
        while i < len(left_part) and j < len(right_part):
            steps.append({'array': arr[:], 'comparing': [left+i, mid+1+j], 'merging': list(range(left, right+1))})
            if left_part[i] <= right_part[j]:
                arr[k] = left_part[i]; i += 1
            else:
                arr[k] = right_part[j]; j += 1
            steps.append({'array': arr[:], 'placed': k, 'merging': list(range(left, right+1))})
            k += 1
        while i < len(left_part):
            arr[k] = left_part[i]; i += 1; k += 1
            steps.append({'array': arr[:], 'placed': k-1, 'merging': list(range(left, right+1))})
        while j < len(right_part):
            arr[k] = right_part[j]; j += 1; k += 1
            steps.append({'array': arr[:], 'placed': k-1, 'merging': list(range(left, right+1))})

    arr = arr[:]
    merge_sort(arr, 0, len(arr)-1)
    steps.append({'array': arr[:], 'done': True})
    return steps


def quick_sort_steps(arr):
    steps = []

    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi-1)
            quick_sort(arr, pi+1, high)

    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        steps.append({'array': arr[:], 'pivot': high, 'range': [low, high]})
        for j in range(low, high):
            steps.append({'array': arr[:], 'comparing': [j, high], 'pivot': high, 'range': [low, high]})
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                steps.append({'array': arr[:], 'swapped': [i, j], 'pivot': high, 'range': [low, high]})
        arr[i+1], arr[high] = arr[high], arr[i+1]
        steps.append({'array': arr[:], 'pivot_placed': i+1, 'range': [low, high]})
        return i+1

    arr = arr[:]
    quick_sort(arr, 0, len(arr)-1)
    steps.append({'array': arr[:], 'done': True})
    return steps


# ─── Helper ────────────────────────────────────────────────────

def parse_input(request, default):
    if request.method == 'POST':
        raw = request.POST.get('numbers', '')
        try:
            nums = [int(x.strip()) for x in raw.split(',') if x.strip()][:10]
            return nums if nums else default
        except:
            pass
    return default


DEFAULT = [5, 3, 8, 1, 9, 2, 4, 7]


# ─── Views ─────────────────────────────────────────────────────

@login_required
def bubble_sort_view(request):
    initial = parse_input(request, DEFAULT)
    steps = bubble_sort_steps(initial)
    return render(request, 'sorting/bubble_sort.html', {
        'steps': json.dumps(steps), 'initial': initial,
        'algo_name': 'BUBBLE SORT', 'algo_emoji': '🫧',
        'algo_desc': 'Repeatedly swaps adjacent elements if they are in wrong order.',
    })

@login_required
def selection_sort_view(request):
    initial = parse_input(request, DEFAULT)
    steps = selection_sort_steps(initial)
    return render(request, 'sorting/visualizer.html', {
        'steps': json.dumps(steps), 'initial': initial,
        'algo_name': 'SELECTION SORT', 'algo_emoji': '🎯',
        'algo_desc': 'Finds the minimum element and places it at the beginning each pass.',
    })

@login_required
def insertion_sort_view(request):
    initial = parse_input(request, DEFAULT)
    steps = insertion_sort_steps(initial)
    return render(request, 'sorting/visualizer.html', {
        'steps': json.dumps(steps), 'initial': initial,
        'algo_name': 'INSERTION SORT', 'algo_emoji': '📥',
        'algo_desc': 'Builds the sorted array one item at a time by inserting each element.',
    })

@login_required
def merge_sort_view(request):
    initial = parse_input(request, DEFAULT)
    steps = merge_sort_steps(initial)
    return render(request, 'sorting/visualizer.html', {
        'steps': json.dumps(steps), 'initial': initial,
        'algo_name': 'MERGE SORT', 'algo_emoji': '🔀',
        'algo_desc': 'Divides array in half, sorts each half, then merges them back together.',
    })

@login_required
def quick_sort_view(request):
    initial = parse_input(request, DEFAULT)
    steps = quick_sort_steps(initial)
    return render(request, 'sorting/visualizer.html', {
        'steps': json.dumps(steps), 'initial': initial,
        'algo_name': 'QUICK SORT', 'algo_emoji': '⚡',
        'algo_desc': 'Picks a pivot, partitions array around it, then recursively sorts partitions.',
    })
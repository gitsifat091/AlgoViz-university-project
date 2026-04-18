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
    
    
    
    # ─── Tree Traversal ────────────────────────────────────────────

def build_tree(values):
    """Build binary tree from list (level-order)"""
    if not values or values[0] is None:
        return {}
    nodes = {}
    for i, val in enumerate(values):
        if val is not None:
            left  = 2*i+1 if 2*i+1 < len(values) and values[2*i+1] is not None else None
            right = 2*i+2 if 2*i+2 < len(values) and values[2*i+2] is not None else None
            nodes[i] = {'val': val, 'left': left, 'right': right}
    return nodes


def inorder_steps(nodes, root=0):
    steps = []
    order = []
    def inorder(i):
        if i is None or i not in nodes:
            return
        inorder(nodes[i]['left'])
        order.append(i)
        steps.append({
            'current': i, 'visited': list(order),
            'highlight': list(order),
            'status': f'Inorder: Visit node {nodes[i]["val"]} (Left→Root→Right)',
            'done': False
        })
        inorder(nodes[i]['right'])
    inorder(root)
    steps.append({'current': None, 'visited': list(order), 'highlight': list(order),
                  'status': f'✅ Inorder Complete! Order: {[nodes[i]["val"] for i in order]}', 'done': True})
    return steps, order


def preorder_steps(nodes, root=0):
    steps = []
    order = []
    def preorder(i):
        if i is None or i not in nodes:
            return
        order.append(i)
        steps.append({
            'current': i, 'visited': list(order),
            'highlight': list(order),
            'status': f'Preorder: Visit node {nodes[i]["val"]} (Root→Left→Right)',
            'done': False
        })
        preorder(nodes[i]['left'])
        preorder(nodes[i]['right'])
    preorder(root)
    steps.append({'current': None, 'visited': list(order), 'highlight': list(order),
                  'status': f'✅ Preorder Complete! Order: {[nodes[i]["val"] for i in order]}', 'done': True})
    return steps, order


def postorder_steps(nodes, root=0):
    steps = []
    order = []
    def postorder(i):
        if i is None or i not in nodes:
            return
        postorder(nodes[i]['left'])
        postorder(nodes[i]['right'])
        order.append(i)
        steps.append({
            'current': i, 'visited': list(order),
            'highlight': list(order),
            'status': f'Postorder: Visit node {nodes[i]["val"]} (Left→Right→Root)',
            'done': False
        })
    postorder(root)
    steps.append({'current': None, 'visited': list(order), 'highlight': list(order),
                  'status': f'✅ Postorder Complete! Order: {[nodes[i]["val"] for i in order]}', 'done': True})
    return steps, order


def levelorder_steps(nodes, root=0):
    from collections import deque
    steps = []
    order = []
    queue = deque([root])
    while queue:
        i = queue.popleft()
        if i not in nodes:
            continue
        order.append(i)
        steps.append({
            'current': i, 'visited': list(order),
            'highlight': list(order),
            'queue': list(queue),
            'status': f'Level Order: Visit node {nodes[i]["val"]}',
            'done': False
        })
        if nodes[i]['left'] is not None:
            queue.append(nodes[i]['left'])
        if nodes[i]['right'] is not None:
            queue.append(nodes[i]['right'])
    steps.append({'current': None, 'visited': list(order), 'highlight': list(order),
                  'queue': [],
                  'status': f'✅ Level Order Complete! Order: {[nodes[i]["val"] for i in order]}', 'done': True})
    return steps, order


DEFAULT_TREE = [1, 2, 3, 4, 5, 6, 7]

def parse_tree_input(raw):
    result = []
    for x in raw.split(','):
        x = x.strip()
        if x.lower() in ('null', 'none', ''):
            result.append(None)
        else:
            try:
                result.append(int(x))
            except:
                pass
    return result if result else DEFAULT_TREE


@login_required
def tree_traversal_view(request):
    values = DEFAULT_TREE
    traversal = 'inorder'
    raw = '1,2,3,4,5,6,7'

    if request.method == 'POST':
        raw = request.POST.get('values', '1,2,3,4,5,6,7')
        traversal = request.POST.get('traversal', 'inorder')
        values = parse_tree_input(raw)[:15]

    nodes = build_tree(values)

    if traversal == 'preorder':
        steps, order = preorder_steps(nodes)
        algo_name = 'PREORDER'
        algo_desc = 'Root → Left → Right'
        color = '00C8FF'
    elif traversal == 'postorder':
        steps, order = postorder_steps(nodes)
        algo_name = 'POSTORDER'
        algo_desc = 'Left → Right → Root'
        color = 'FF8C42'
    elif traversal == 'levelorder':
        steps, order = levelorder_steps(nodes)
        algo_name = 'LEVEL ORDER'
        algo_desc = 'Level by Level (BFS)'
        color = 'a855f7'
    else:
        steps, order = inorder_steps(nodes)
        algo_name = 'INORDER'
        algo_desc = 'Left → Root → Right'
        color = '00D4A0'

    return render(request, 'sorting/tree_traversal.html', {
        'steps': json.dumps(steps),
        'nodes': json.dumps({str(k): v for k, v in nodes.items()}),
        'values': values,
        'raw': raw,
        'traversal': traversal,
        'algo_name': algo_name,
        'algo_desc': algo_desc,
        'algo_color': color,
        'final_order': json.dumps([nodes[i]['val'] for i in order]),
        'traversals': [
            ('inorder',    '🟢 Inorder',    '00D4A0'),
            ('preorder',   '🔵 Preorder',   '00C8FF'),
            ('postorder',  '🟠 Postorder',  'FF8C42'),
            ('levelorder', '🟣 Level Order','a855f7'),
        ],
    })
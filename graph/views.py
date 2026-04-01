# from django.shortcuts import render

# Create your views here.


import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from collections import deque


# ─── BFS Algorithm ─────────────────────────────────────────────

def bfs_steps(graph, start, node_count):
    steps = []
    visited = set()
    queue = deque([start])
    visited.add(start)
    parent = {start: None}

    steps.append({
        'visited': list(visited),
        'queue': list(queue),
        'current': None,
        'exploring_edge': None,
        'status': f'Start BFS from node {start}. Add {start} to queue.',
        'done': False
    })

    while queue:
        node = queue.popleft()
        steps.append({
            'visited': list(visited),
            'queue': list(queue),
            'current': node,
            'exploring_edge': None,
            'status': f'Dequeue node {node}. Process it.',
            'done': False
        })

        for neighbor in sorted(graph.get(node, [])):
            steps.append({
                'visited': list(visited),
                'queue': list(queue),
                'current': node,
                'exploring_edge': [node, neighbor],
                'status': f'Check edge {node} → {neighbor}',
                'done': False
            })
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
                parent[neighbor] = node
                steps.append({
                    'visited': list(visited),
                    'queue': list(queue),
                    'current': node,
                    'exploring_edge': [node, neighbor],
                    'status': f'Node {neighbor} not visited → enqueue it!',
                    'done': False
                })
            else:
                steps.append({
                    'visited': list(visited),
                    'queue': list(queue),
                    'current': node,
                    'exploring_edge': [node, neighbor],
                    'status': f'Node {neighbor} already visited → skip.',
                    'done': False
                })

    steps.append({
        'visited': list(visited),
        'queue': [],
        'current': None,
        'exploring_edge': None,
        'status': f'BFS Complete! Visited {len(visited)} nodes: {list(visited)}',
        'done': True
    })
    return steps


# ─── DFS Algorithm ─────────────────────────────────────────────

def dfs_steps(graph, start, node_count):
    steps = []
    visited = set()
    stack_trace = []

    def dfs(node, parent_node):
        visited.add(node)
        stack_trace.append(node)
        steps.append({
            'visited': list(visited),
            'stack': list(stack_trace),
            'current': node,
            'exploring_edge': [parent_node, node] if parent_node is not None else None,
            'status': f'Visit node {node}. Push to stack.',
            'done': False
        })

        for neighbor in sorted(graph.get(node, [])):
            steps.append({
                'visited': list(visited),
                'stack': list(stack_trace),
                'current': node,
                'exploring_edge': [node, neighbor],
                'status': f'Check edge {node} → {neighbor}',
                'done': False
            })
            if neighbor not in visited:
                dfs(neighbor, node)
            else:
                steps.append({
                    'visited': list(visited),
                    'stack': list(stack_trace),
                    'current': node,
                    'exploring_edge': [node, neighbor],
                    'status': f'Node {neighbor} already visited → backtrack.',
                    'done': False
                })

        stack_trace.pop()
        steps.append({
            'visited': list(visited),
            'stack': list(stack_trace),
            'current': node,
            'exploring_edge': None,
            'status': f'Done with node {node}. Pop from stack.',
            'done': False
        })

    dfs(start, None)
    steps.append({
        'visited': list(visited),
        'stack': [],
        'current': None,
        'exploring_edge': None,
        'status': f'DFS Complete! Visited order: {[s["current"] for s in steps if s.get("current") is not None and "Push" in s["status"]]}',
        'done': True
    })
    return steps


# ─── Parse Graph Input ─────────────────────────────────────────

def parse_graph(edges_str, node_count):
    graph = {i: [] for i in range(node_count)}
    edges = []
    for part in edges_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                a, b = part.split('-')
                a, b = int(a.strip()), int(b.strip())
                if 0 <= a < node_count and 0 <= b < node_count:
                    if b not in graph[a]: graph[a].append(b)
                    if a not in graph[b]: graph[b].append(a)
                    edges.append([a, b])
            except:
                pass
    return graph, edges


DEFAULT_EDGES = "0-1, 0-2, 1-3, 1-4, 2-5, 2-6"
DEFAULT_NODES = 7
DEFAULT_START = 0


# ─── Views ─────────────────────────────────────────────────────

@login_required
def bfs_view(request):
    edges_str = DEFAULT_EDGES
    node_count = DEFAULT_NODES
    start_node = DEFAULT_START

    if request.method == 'POST':
        edges_str  = request.POST.get('edges', DEFAULT_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_NODES)), 12)
        except: node_count = DEFAULT_NODES
        try: start_node = int(request.POST.get('start', DEFAULT_START))
        except: start_node = DEFAULT_START
        start_node = max(0, min(start_node, node_count - 1))

    graph, edges = parse_graph(edges_str, node_count)
    steps = bfs_steps(graph, start_node, node_count)

    return render(request, 'graph/graph_viz.html', {
        'steps': json.dumps(steps),
        'edges': json.dumps(edges),
        'node_count': node_count,
        'start_node': start_node,
        'edges_str': edges_str,
        'algo_name': 'BFS',
        'algo_full': 'BREADTH FIRST SEARCH',
        'algo_emoji': '🌊',
        'algo_desc': 'Explores all neighbors at current depth before moving to next level. Uses a Queue.',
        'data_structure': 'QUEUE',
        'ds_color': '00C8FF',
    })


@login_required
def dfs_view(request):
    edges_str = DEFAULT_EDGES
    node_count = DEFAULT_NODES
    start_node = DEFAULT_START

    if request.method == 'POST':
        edges_str  = request.POST.get('edges', DEFAULT_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_NODES)), 12)
        except: node_count = DEFAULT_NODES
        try: start_node = int(request.POST.get('start', DEFAULT_START))
        except: start_node = DEFAULT_START
        start_node = max(0, min(start_node, node_count - 1))

    graph, edges = parse_graph(edges_str, node_count)
    steps = dfs_steps(graph, start_node, node_count)

    return render(request, 'graph/graph_viz.html', {
        'steps': json.dumps(steps),
        'edges': json.dumps(edges),
        'node_count': node_count,
        'start_node': start_node,
        'edges_str': edges_str,
        'algo_name': 'DFS',
        'algo_full': 'DEPTH FIRST SEARCH',
        'algo_emoji': '🔍',
        'algo_desc': 'Explores as far as possible along each branch before backtracking. Uses a Stack.',
        'data_structure': 'STACK',
        'ds_color': '00D4A0',
    })
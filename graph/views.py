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
    
# ─── Dijkstra Algorithm ────────────────────────────────────────

def dijkstra_steps(graph_weighted, start, node_count):
    import heapq
    INF = float('inf')
    dist = {i: INF for i in range(node_count)}
    dist[start] = 0
    prev = {i: None for i in range(node_count)}
    visited = set()
    pq = [(0, start)]
    steps = []

    steps.append({
        'visited': [],
        'current': None,
        'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
        'exploring_edge': None,
        'relaxed_edge': None,
        'status': f'Initialize. dist[{start}]=0, all others=∞',
        'done': False
    })

    while pq:
        d, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        steps.append({
            'visited': list(visited),
            'current': node,
            'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
            'exploring_edge': None,
            'relaxed_edge': None,
            'status': f'Pick node {node} (dist={d}). Mark visited.',
            'done': False
        })

        for neighbor, weight in graph_weighted.get(node, []):
            if neighbor in visited:
                continue

            steps.append({
                'visited': list(visited),
                'current': node,
                'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                'exploring_edge': [node, neighbor, weight],
                'relaxed_edge': None,
                'status': f'Check edge {node}→{neighbor} (w={weight}). dist[{node}]+{weight} = {dist[node]+weight} vs dist[{neighbor}]={dist[neighbor] if dist[neighbor]!=INF else "∞"}',
                'done': False
            })

            new_dist = dist[node] + weight
            if new_dist < dist[neighbor]:
                dist[neighbor] = new_dist
                prev[neighbor] = node
                heapq.heappush(pq, (new_dist, neighbor))

                steps.append({
                    'visited': list(visited),
                    'current': node,
                    'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                    'exploring_edge': None,
                    'relaxed_edge': [node, neighbor],
                    'status': f'✅ Relaxed! dist[{neighbor}] updated to {new_dist}',
                    'done': False
                })

    steps.append({
        'visited': list(visited),
        'current': None,
        'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
        'exploring_edge': None,
        'relaxed_edge': None,
        'status': f'Dijkstra Complete! Shortest distances from node {start} found.',
        'done': True
    })
    return steps, dist, prev


def parse_weighted_graph(edges_str, node_count):
    graph = {i: [] for i in range(node_count)}
    edges = []
    for part in edges_str.split(','):
        part = part.strip()
        if '-' in part:
            try:
                if ':' in part:
                    edge, w = part.split(':')
                    weight = int(w.strip())
                else:
                    edge, weight = part, 1
                a, b = edge.split('-')
                a, b = int(a.strip()), int(b.strip())
                weight = abs(weight)
                if 0 <= a < node_count and 0 <= b < node_count:
                    graph[a].append((b, weight))
                    graph[b].append((a, weight))
                    edges.append([a, b, weight])
            except:
                pass
    return graph, edges


DEFAULT_WEIGHTED_EDGES = "0-1:4, 0-2:2, 1-3:5, 2-1:1, 2-3:8, 2-4:10, 3-4:2, 3-5:6, 4-5:3"
DEFAULT_W_NODES = 6


@login_required
def dijkstra_view(request):
    edges_str  = DEFAULT_WEIGHTED_EDGES
    node_count = DEFAULT_W_NODES
    start_node = 0

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_WEIGHTED_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_W_NODES)), 12)
        except: node_count = DEFAULT_W_NODES
        try: start_node = int(request.POST.get('start', 0))
        except: start_node = 0
        start_node = max(0, min(start_node, node_count - 1))

    graph, edges = parse_weighted_graph(edges_str, node_count)
    steps, dist, prev = dijkstra_steps(graph, start_node, node_count)

    return render(request, 'graph/dijkstra.html', {
        'steps':      json.dumps(steps),
        'edges':      json.dumps(edges),
        'node_count': node_count,
        'start_node': start_node,
        'edges_str':  edges_str,
        'algo_name':  'DIJKSTRA',
        'algo_emoji': '🗺️',
        'algo_desc':  "Finds shortest path from source to all nodes. Uses a Priority Queue (Min-Heap). Only works with non-negative weights.",
    })
    
# ─── Bellman-Ford Algorithm ────────────────────────────────────

def bellman_ford_steps(edges, start, node_count):
    INF = float('inf')
    dist = {i: INF for i in range(node_count)}
    dist[start] = 0
    prev = {i: None for i in range(node_count)}
    steps = []

    steps.append({
        'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
        'current_edge': None,
        'relaxed_edge': None,
        'iteration': 0,
        'visited': [start],
        'negative_cycle': False,
        'status': f'Initialize. dist[{start}]=0, all others=∞',
        'done': False
    })

    # N-1 iterations
    for i in range(node_count - 1):
        relaxed_any = False
        for a, b, w in edges:
            # Check a→b
            steps.append({
                'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                'current_edge': [a, b, w],
                'relaxed_edge': None,
                'iteration': i + 1,
                'visited': [k for k, v in dist.items() if v != INF],
                'negative_cycle': False,
                'status': f'Iteration {i+1} | Check {a}→{b} (w={w}): dist[{a}]{"=∞" if dist[a]==INF else "="+str(dist[a])} + {w}',
                'done': False
            })
            if dist[a] != INF and dist[a] + w < dist[b]:
                dist[b] = dist[a] + w
                prev[b] = a
                relaxed_any = True
                steps.append({
                    'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                    'current_edge': None,
                    'relaxed_edge': [a, b],
                    'iteration': i + 1,
                    'visited': [k for k, v in dist.items() if v != INF],
                    'negative_cycle': False,
                    'status': f'✅ Relaxed! dist[{b}] = {dist[b]}',
                    'done': False
                })

            # Check b→a (undirected)
            steps.append({
                'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                'current_edge': [b, a, w],
                'relaxed_edge': None,
                'iteration': i + 1,
                'visited': [k for k, v in dist.items() if v != INF],
                'negative_cycle': False,
                'status': f'Iteration {i+1} | Check {b}→{a} (w={w}): dist[{b}]{"=∞" if dist[b]==INF else "="+str(dist[b])} + {w}',
                'done': False
            })
            if dist[b] != INF and dist[b] + w < dist[a]:
                dist[a] = dist[b] + w
                prev[a] = b
                relaxed_any = True
                steps.append({
                    'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                    'current_edge': None,
                    'relaxed_edge': [b, a],
                    'iteration': i + 1,
                    'visited': [k for k, v in dist.items() if v != INF],
                    'negative_cycle': False,
                    'status': f'✅ Relaxed! dist[{a}] = {dist[a]}',
                    'done': False
                })

        if not relaxed_any:
            steps.append({
                'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                'current_edge': None,
                'relaxed_edge': None,
                'iteration': i + 1,
                'visited': [k for k, v in dist.items() if v != INF],
                'negative_cycle': False,
                'status': f'Iteration {i+1}: No relaxation. Early stop!',
                'done': False
            })
            break

    # Check negative cycle
    neg_cycle = False
    for a, b, w in edges:
        if dist[a] != INF and dist[a] + w < dist[b]:
            neg_cycle = True
            break
        if dist[b] != INF and dist[b] + w < dist[a]:
            neg_cycle = True
            break

    steps.append({
        'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
        'current_edge': None,
        'relaxed_edge': None,
        'iteration': node_count - 1,
        'visited': [k for k, v in dist.items() if v != INF],
        'negative_cycle': neg_cycle,
        'status': '⚠️ Negative cycle detected!' if neg_cycle else f'✅ Bellman-Ford Complete! Shortest distances from node {start} found.',
        'done': True
    })
    return steps


@login_required
def bellman_ford_view(request):
    edges_str  = DEFAULT_WEIGHTED_EDGES
    node_count = DEFAULT_W_NODES
    start_node = 0

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_WEIGHTED_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_W_NODES)), 12)
        except: node_count = DEFAULT_W_NODES
        try: start_node = int(request.POST.get('start', 0))
        except: start_node = 0
        start_node = max(0, min(start_node, node_count - 1))

    _, edges_list = parse_weighted_graph(edges_str, node_count)
    edges_for_bf = [[a, b, w] for a, b, w in edges_list]
    steps = bellman_ford_steps(edges_for_bf, start_node, node_count)

    return render(request, 'graph/bellman_ford.html', {
        'steps':      json.dumps(steps),
        'edges':      json.dumps(edges_list),
        'node_count': node_count,
        'start_node': start_node,
        'edges_str':  edges_str,
        'algo_desc':  'Relaxes ALL edges N-1 times. Works with negative weights. Detects negative cycles.',
    })
    
# ─── Floyd-Warshall Algorithm ──────────────────────────────────

def floyd_warshall_steps(node_count, edges):
    INF = float('inf')

    # Initialize distance matrix
    dist = [[INF]*node_count for _ in range(node_count)]
    for i in range(node_count):
        dist[i][i] = 0
    for a, b, w in edges:
        dist[a][b] = min(dist[a][b], w)
        dist[b][a] = min(dist[b][a], w)

    def mat_snapshot():
        return [[(-1 if v==INF else v) for v in row] for row in dist]

    steps = []
    steps.append({
        'matrix': mat_snapshot(),
        'k': -1, 'i': -1, 'j': -1,
        'relaxed': None,
        'current_edge': None,
        'status': 'Initialize distance matrix. Direct edges set, diagonal=0, rest=∞',
        'done': False
    })

    for k in range(node_count):
        steps.append({
            'matrix': mat_snapshot(),
            'k': k, 'i': -1, 'j': -1,
            'relaxed': None,
            'current_edge': None,
            'status': f'Using node {k} as intermediate vertex.',
            'done': False
        })
        for i in range(node_count):
            for j in range(node_count):
                if dist[i][k] == INF or dist[k][j] == INF:
                    continue
                steps.append({
                    'matrix': mat_snapshot(),
                    'k': k, 'i': i, 'j': j,
                    'relaxed': None,
                    'current_edge': [i, j],
                    'status': f'Check: dist[{i}][{j}] = {dist[i][j] if dist[i][j]!=INF else "∞"} vs dist[{i}][{k}]+dist[{k}][{j}] = {dist[i][k]}+{dist[k][j]} = {dist[i][k]+dist[k][j]}',
                    'done': False
                })
                new_dist = dist[i][k] + dist[k][j]
                if new_dist < dist[i][j]:
                    dist[i][j] = new_dist
                    dist[j][i] = new_dist
                    steps.append({
                        'matrix': mat_snapshot(),
                        'k': k, 'i': i, 'j': j,
                        'relaxed': [i, j],
                        'current_edge': None,
                        'status': f'✅ Updated dist[{i}][{j}] = {new_dist} (via node {k})',
                        'done': False
                    })

    steps.append({
        'matrix': mat_snapshot(),
        'k': node_count-1, 'i': -1, 'j': -1,
        'relaxed': None,
        'current_edge': None,
        'status': f'✅ Floyd-Warshall Complete! All-pairs shortest paths found.',
        'done': True
    })
    return steps


@login_required
def floyd_warshall_view(request):
    edges_str  = DEFAULT_WEIGHTED_EDGES
    node_count = DEFAULT_W_NODES

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_WEIGHTED_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_W_NODES)), 8)
        except: node_count = DEFAULT_W_NODES

    _, edges_list = parse_weighted_graph(edges_str, node_count)
    steps = floyd_warshall_steps(node_count, edges_list)

    return render(request, 'graph/floyd_warshall.html', {
        'steps':      json.dumps(steps),
        'edges':      json.dumps(edges_list),
        'node_count': node_count,
        'edges_str':  edges_str,
        'algo_desc':  'Finds shortest paths between ALL pairs of nodes. Uses dynamic programming. O(V³) time complexity.',
    })
    
# ─── Best First Search ─────────────────────────────────────────

def best_first_steps(graph, start, goal, heuristic, node_count):
    import heapq
    visited = set()
    pq = [(heuristic[start], start)]
    parent = {start: None}
    steps = []

    steps.append({
        'visited': [], 'current': None,
        'exploring_edge': None, 'frontier': [start],
        'goal_found': False,
        'status': f'Start Best First Search from {start} → Goal: {goal}. h({start})={heuristic[start]}',
        'done': False
    })

    while pq:
        h, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        steps.append({
            'visited': list(visited), 'current': node,
            'exploring_edge': None,
            'frontier': [n for _, n in pq],
            'goal_found': node == goal,
            'status': f'Pick node {node} (h={heuristic[node]}). {"🎯 GOAL FOUND!" if node==goal else "Process neighbors."}',
            'done': node == goal
        })

        if node == goal:
            break

        for neighbor in sorted(graph.get(node, [])):
            steps.append({
                'visited': list(visited), 'current': node,
                'exploring_edge': [node, neighbor],
                'frontier': [n for _, n in pq],
                'goal_found': False,
                'status': f'Check neighbor {neighbor}. h({neighbor})={heuristic.get(neighbor, 0)}',
                'done': False
            })
            if neighbor not in visited:
                parent[neighbor] = node
                heapq.heappush(pq, (heuristic.get(neighbor, 0), neighbor))
                steps.append({
                    'visited': list(visited), 'current': node,
                    'exploring_edge': [node, neighbor],
                    'frontier': [n for _, n in pq],
                    'goal_found': False,
                    'status': f'Add {neighbor} to frontier (h={heuristic.get(neighbor,0)})',
                    'done': False
                })

    if goal not in visited:
        steps.append({
            'visited': list(visited), 'current': None,
            'exploring_edge': None, 'frontier': [],
            'goal_found': False,
            'status': f'Goal {goal} not reachable!',
            'done': True
        })

    return steps, parent


# ─── UCS (Uniform Cost Search) ─────────────────────────────────

def ucs_steps(graph_weighted, start, goal, node_count):
    import heapq
    INF = float('inf')
    dist = {i: INF for i in range(node_count)}
    dist[start] = 0
    pq = [(0, start)]
    visited = set()
    parent = {start: None}
    steps = []

    steps.append({
        'visited': [], 'current': None,
        'exploring_edge': None,
        'frontier': [(0, start)],
        'goal_found': False,
        'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
        'status': f'Start UCS from {start} → Goal: {goal}. Cost[{start}]=0',
        'done': False
    })

    while pq:
        cost, node = heapq.heappop(pq)
        if node in visited:
            continue
        visited.add(node)

        steps.append({
            'visited': list(visited), 'current': node,
            'exploring_edge': None,
            'frontier': list(pq),
            'goal_found': node == goal,
            'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
            'status': f'Dequeue node {node} (cost={cost}). {"🎯 GOAL FOUND!" if node==goal else "Process neighbors."}',
            'done': node == goal
        })

        if node == goal:
            break

        for neighbor, weight in sorted(graph_weighted.get(node, [])):
            if neighbor in visited:
                continue
            new_cost = cost + weight
            steps.append({
                'visited': list(visited), 'current': node,
                'exploring_edge': [node, neighbor],
                'frontier': list(pq),
                'goal_found': False,
                'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                'status': f'Check {node}→{neighbor} (w={weight}). Total cost={new_cost} vs {dist[neighbor] if dist[neighbor]!=INF else "∞"}',
                'done': False
            })
            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(pq, (new_cost, neighbor))
                steps.append({
                    'visited': list(visited), 'current': node,
                    'exploring_edge': [node, neighbor],
                    'frontier': list(pq),
                    'goal_found': False,
                    'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
                    'status': f'✅ Updated cost[{neighbor}]={new_cost}. Added to frontier.',
                    'done': False
                })

    if goal not in visited:
        steps.append({
            'visited': list(visited), 'current': None,
            'exploring_edge': None, 'frontier': [],
            'goal_found': False,
            'dist': {k: (v if v != INF else -1) for k, v in dist.items()},
            'status': f'Goal {goal} not reachable!',
            'done': True
        })

    return steps


# ─── DLS (Depth Limited Search) ────────────────────────────────

def dls_steps(graph, start, goal, limit, node_count):
    steps = []
    found = [False]
    path = []

    steps.append({
        'visited': [], 'current': None, 'path': [],
        'exploring_edge': None, 'depth': 0, 'limit': limit,
        'goal_found': False,
        'status': f'Start DLS from {start} → Goal: {goal}. Depth limit: {limit}',
        'done': False
    })

    def dls_recursive(node, depth, visited_set, current_path):
        if found[0]:
            return
        visited_set.add(node)
        current_path.append(node)

        steps.append({
            'visited': list(visited_set), 'current': node,
            'path': list(current_path),
            'exploring_edge': None, 'depth': depth, 'limit': limit,
            'goal_found': node == goal,
            'status': f'Visit node {node} at depth {depth}/{limit}. {"🎯 GOAL FOUND!" if node==goal else ""}',
            'done': node == goal
        })

        if node == goal:
            found[0] = True
            return

        if depth >= limit:
            steps.append({
                'visited': list(visited_set), 'current': node,
                'path': list(current_path),
                'exploring_edge': None, 'depth': depth, 'limit': limit,
                'goal_found': False,
                'status': f'⛔ Depth limit {limit} reached at node {node}. Backtrack.',
                'done': False
            })
            current_path.pop()
            return

        for neighbor in sorted(graph.get(node, [])):
            if neighbor not in visited_set and not found[0]:
                steps.append({
                    'visited': list(visited_set), 'current': node,
                    'path': list(current_path),
                    'exploring_edge': [node, neighbor],
                    'depth': depth, 'limit': limit,
                    'goal_found': False,
                    'status': f'Explore edge {node}→{neighbor} (depth {depth+1}/{limit})',
                    'done': False
                })
                dls_recursive(neighbor, depth + 1, visited_set, current_path)

        if not found[0]:
            current_path.pop()
            steps.append({
                'visited': list(visited_set), 'current': node,
                'path': list(current_path),
                'exploring_edge': None, 'depth': depth, 'limit': limit,
                'goal_found': False,
                'status': f'Backtrack from node {node}.',
                'done': False
            })

    dls_recursive(start, 0, set(), [])

    if not found[0]:
        steps.append({
            'visited': [], 'current': None, 'path': [],
            'exploring_edge': None, 'depth': 0, 'limit': limit,
            'goal_found': False,
            'status': f'Goal {goal} not found within depth limit {limit}!',
            'done': True
        })

    return steps


# ─── Default heuristic helper ───────────────────────────────────
def default_heuristic(node_count, goal):
    # Simple heuristic: distance from goal (decreasing)
    return {i: abs(goal - i) for i in range(node_count)}


# ─── Views ─────────────────────────────────────────────────────

DEFAULT_GOAL = 5

@login_required
def best_first_view(request):
    edges_str  = DEFAULT_EDGES
    node_count = DEFAULT_NODES
    start_node = DEFAULT_START
    goal_node  = DEFAULT_GOAL

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_NODES)), 12)
        except: node_count = DEFAULT_NODES
        try: start_node = int(request.POST.get('start', DEFAULT_START))
        except: start_node = DEFAULT_START
        try: goal_node = int(request.POST.get('goal', DEFAULT_GOAL))
        except: goal_node = DEFAULT_GOAL
        start_node = max(0, min(start_node, node_count-1))
        goal_node  = max(0, min(goal_node,  node_count-1))

    graph, edges = parse_graph(edges_str, node_count)
    heuristic = default_heuristic(node_count, goal_node)
    steps, _ = best_first_steps(graph, start_node, goal_node, heuristic, node_count)

    return render(request, 'graph/search_viz.html', {
        'steps': json.dumps(steps), 'edges': json.dumps(edges),
        'node_count': node_count, 'start_node': start_node,
        'goal_node': goal_node, 'edges_str': edges_str,
        'heuristic': json.dumps(heuristic),
        'algo_name': 'BEST FIRST SEARCH', 'algo_emoji': '⭐',
        'algo_desc': 'Greedy search using heuristic h(n). Always picks the node closest to goal. Does NOT guarantee shortest path.',
        'show_heuristic': True, 'show_cost': False, 'show_depth': False,
        'has_goal': True,
    })


@login_required
def ucs_view(request):
    edges_str  = DEFAULT_WEIGHTED_EDGES
    node_count = DEFAULT_W_NODES
    start_node = DEFAULT_START
    goal_node  = DEFAULT_GOAL - 1

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_WEIGHTED_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_W_NODES)), 12)
        except: node_count = DEFAULT_W_NODES
        try: start_node = int(request.POST.get('start', DEFAULT_START))
        except: start_node = DEFAULT_START
        try: goal_node = int(request.POST.get('goal', DEFAULT_GOAL-1))
        except: goal_node = DEFAULT_GOAL-1
        start_node = max(0, min(start_node, node_count-1))
        goal_node  = max(0, min(goal_node,  node_count-1))

    graph_w, edges = parse_weighted_graph(edges_str, node_count)
    steps = ucs_steps(graph_w, start_node, goal_node, node_count)

    return render(request, 'graph/search_viz.html', {
        'steps': json.dumps(steps), 'edges': json.dumps(edges),
        'node_count': node_count, 'start_node': start_node,
        'goal_node': goal_node, 'edges_str': edges_str,
        'heuristic': json.dumps({}),
        'algo_name': 'UNIFORM COST SEARCH', 'algo_emoji': '💰',
        'algo_desc': 'Expands lowest cumulative cost node first. Guarantees shortest path. Like Dijkstra but stops at goal.',
        'show_heuristic': False, 'show_cost': True, 'show_depth': False,
        'has_goal': True,
    })


@login_required
def dls_view(request):
    edges_str  = DEFAULT_EDGES
    node_count = DEFAULT_NODES
    start_node = DEFAULT_START
    goal_node  = DEFAULT_GOAL
    depth_limit = 3

    if request.method == 'POST':
        edges_str = request.POST.get('edges', DEFAULT_EDGES)
        try: node_count = min(int(request.POST.get('nodes', DEFAULT_NODES)), 12)
        except: node_count = DEFAULT_NODES
        try: start_node = int(request.POST.get('start', DEFAULT_START))
        except: start_node = DEFAULT_START
        try: goal_node = int(request.POST.get('goal', DEFAULT_GOAL))
        except: goal_node = DEFAULT_GOAL
        try: depth_limit = min(int(request.POST.get('limit', 3)), 10)
        except: depth_limit = 3
        start_node = max(0, min(start_node, node_count-1))
        goal_node  = max(0, min(goal_node,  node_count-1))

    graph, edges = parse_graph(edges_str, node_count)
    steps = dls_steps(graph, start_node, goal_node, depth_limit, node_count)

    return render(request, 'graph/search_viz.html', {
        'steps': json.dumps(steps), 'edges': json.dumps(edges),
        'node_count': node_count, 'start_node': start_node,
        'goal_node': goal_node, 'edges_str': edges_str,
        'heuristic': json.dumps({}),
        'algo_name': 'DEPTH LIMITED SEARCH', 'algo_emoji': '📏',
        'algo_desc': 'DFS with a maximum depth limit. Avoids infinite loops. Incomplete if goal is beyond the limit.',
        'show_heuristic': False, 'show_cost': False, 'show_depth': True,
        'depth_limit': depth_limit,
        'has_goal': True,
    })
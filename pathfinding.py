from collections import deque
import heapq


class PathFinding:
    def __init__(self, game):
        self.game = game
        self.map = game.map.mini_map
        # Use only cardinal directions for better performance
        self.ways = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        # Add diagonals only if needed
        self.diagonal_ways = [(-1, -1), (1, -1), (1, 1), (-1, 1)]
        self.graph = {}
        self.path_cache = {}  # Cache for paths
        self.get_graph()

    def get_path(self, start, goal):
        # Check if path is in cache
        cache_key = (start, goal)
        if cache_key in self.path_cache:
            return self.path_cache[cache_key]

        # Make sure both start and goal are valid positions in the graph
        if start not in self.graph:
            # If start position is not in graph, find the closest valid position
            start = self.find_closest_valid_position(start)
        if goal not in self.graph:
            # If goal position is not in graph, find the closest valid position
            goal = self.find_closest_valid_position(goal)

        # Use A* for more efficient pathfinding
        path = self.a_star(start, goal)

        # Cache the result
        self.path_cache[cache_key] = path

        # Limit cache size
        if len(self.path_cache) > 100:
            # Remove oldest entries
            for _ in range(20):
                self.path_cache.pop(next(iter(self.path_cache)))

        return path

    def find_closest_valid_position(self, pos):
        # Find the closest position that exists in the graph
        x, y = pos
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                new_pos = (x + dx, y + dy)
                if new_pos in self.graph:
                    return new_pos
        # If no close position found, return a default position
        return next(iter(self.graph))

    def a_star(self, start, goal):
        """A* pathfinding algorithm for more efficient paths"""
        # Priority queue for A*
        open_set = [(0, start)]
        # Dictionary to store g scores (cost from start to current node)
        g_score = {start: 0}
        # Dictionary to store parent nodes for path reconstruction
        came_from = {}

        # Set of positions occupied by NPCs
        npc_positions = self.game.object_handler.npc_positions

        while open_set:
            # Get node with lowest f score (priority)
            _, current = heapq.heappop(open_set)

            # If we reached the goal, reconstruct and return the next step
            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                # Return the next step (second-to-last node in the path)
                if len(path) > 1:
                    return path[-2]
                return path[0]

            # Check neighbors
            for neighbor in self.graph.get(current, []):
                # Skip if occupied by an NPC
                if neighbor in npc_positions:
                    continue

                # Calculate tentative g score
                tentative_g = g_score[current] + 1

                # If we found a better path to this neighbor
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    # Update path and scores
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    # Calculate f score (g + heuristic)
                    f_score = tentative_g + self.heuristic(neighbor, goal)
                    # Add to open set
                    heapq.heappush(open_set, (f_score, neighbor))

        # If no path found, return the start position
        return start

    def heuristic(self, a, b):
        """Manhattan distance heuristic for A*"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def bfs(self, start, goal, graph):
        """Breadth-first search algorithm (kept for compatibility)"""
        queue = deque([start])
        visited = {start: None}

        while queue:
            cur_node = queue.popleft()
            if cur_node == goal:
                break
            next_nodes = graph[cur_node]

            for next_node in next_nodes:
                if next_node not in visited and next_node not in self.game.object_handler.npc_positions:
                    queue.append(next_node)
                    visited[next_node] = cur_node
        return visited

    def get_next_nodes(self, x, y):
        # Start with cardinal directions (more important)
        nodes = [(x + dx, y + dy) for dx, dy in self.ways
                if (x + dx, y + dy) not in self.game.map.world_map]

        # Add diagonal moves only if they don't cross walls
        for dx, dy in self.diagonal_ways:
            nx, ny = x + dx, y + dy
            # Check if diagonal move is valid (both adjacent cardinal moves must be valid)
            if ((nx, y) not in self.game.map.world_map and
                (x, ny) not in self.game.map.world_map and
                (nx, ny) not in self.game.map.world_map):
                nodes.append((nx, ny))

        return nodes

    def get_graph(self):
        # Clear existing graph
        self.graph = {}

        # Build graph based on current world map
        for y in range(len(self.map)):
            for x in range(len(self.map[0])):
                # Check if position is walkable (not in world_map)
                if (x, y) not in self.game.map.world_map:
                    self.graph[(x, y)] = self.graph.get((x, y), []) + self.get_next_nodes(x, y)

    def update_graph(self):
        # Update the graph when the world map changes (e.g., doors open)
        self.get_graph()
        # Clear path cache when graph changes
        self.path_cache.clear()
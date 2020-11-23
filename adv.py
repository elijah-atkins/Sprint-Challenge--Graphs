from room import Room
from player import Player
from world import World
import math
import random
from ast import literal_eval
from collections import deque

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
# room_graph = {
#   0: [(3, 5), {'n': 1, 's': 5, 'e': 3, 'w': 7}],
#   1: [(3, 6), {'s': 0, 'n': 2, 'e': 12, 'w': 15}],
#   2: [(3, 7), {'s': 1}],
#   3: [(4, 5), {'w': 0, 'e': 4}],
#   4: [(5, 5), {'w': 3}],
#   5: [(3, 4), {'n': 0, 's': 6}],
#   6: [(3, 3), {'n': 5, 'w': 11}],
#   7: [(2, 5), {'w': 8, 'e': 0}],
#   8: [(1, 5), {'e': 7}],
#   9: [(1, 4), {'n': 8, 's': 10}],
#   10: [(1, 3), {'n': 9, 'e': 11}],
#   11: [(2, 3), {'w': 10, 'e': 6}],
#   12: [(4, 6), {'w': 1, 'e': 13}],
#   13: [(5, 6), {'w': 12, 'n': 14}],
#   14: [(5, 7), {'s': 13}],
#   15: [(2, 6), {'e': 1, 'w': 16}],
#   16: [(1, 6), {'n': 17, 'e': 15}],
#   17: [(1, 7), {'s': 16}]
# }

world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# init a traversal graph
traversalGraph = {0: {'n': '?', 's': '?', 'w': '?', 'e': '?'}}

#Dictionary to find opposite direction
opposite_direction = {
    's': 'n',
    'n': 's',
    'e': 'w',
    'w': 'e'
}
visited = set()

while len(visited) < len(room_graph) -1:
    room_exits = traversalGraph[player.current_room.id]
    unexplored = []
    for direction in room_exits:
        if room_exits[direction] == '?':
            unexplored.append(direction)
    if unexplored:
        # add to traversal path

        connected_rooms = room_graph[player.current_room.id][1]
        available_choices = {}
        print(unexplored, connected_rooms)
        for room in unexplored:
            nextRoomDoors = len(room_graph[connected_rooms[room]][1])
            available_choices[room] = (nextRoomDoors)
        sorted_x = sorted(available_choices.items(), key=lambda kv: kv[1])        
        move = sorted_x[0][0]

        traversal_path.append(move)
        # save id
        previous_room_id = player.current_room.id
        # travel
        player.travel(move)
        # if not in graph add room
        if player.current_room.id not in traversalGraph:
            traversalGraph[player.current_room.id] = {}
            for direction in player.current_room.get_exits():
                traversalGraph[player.current_room.id][direction] = '?'

        traversalGraph[previous_room_id][move] = player.current_room.id
        traversalGraph[player.current_room.id][opposite_direction[move]] = previous_room_id
        
    else:
        
        queue = deque()
        queue.append(list(opposite_direction[traversal_path[-1]]))
        make_path = True
        print(f"DEAD END: {player.current_room.id}")
        while make_path:
            dequeued = queue.popleft()
            print(f"LENGTH OF PATH: {len(traversal_path)}")
            print(f"SHORTEST PATH: {dequeued}")
            last_move = dequeued[-1]
            for m in dequeued:
                player.travel(m)
            exits = traversalGraph[player.current_room.id]
            for exit in exits:
                if exits[exit] == '?':
                    make_path = False
                    print(f"LENGTH OF PATH afterExtend: {len(traversal_path)}")
                elif opposite_direction[exit] != last_move:
                    path_copy = list(dequeued)
                    path_copy.append(exit)
                    queue.append(path_copy)
            # reset player
            if make_path:
                for r_move in dequeued[::-1]:
                    player.travel(opposite_direction[r_move])
            else:
                # shortest path
                traversal_path.extend(dequeued)
            print(f"Player after reset: {player.current_room.id}")
    
    # add completed rooms to visited
    for room in traversalGraph:
        if room not in visited:
            qs = []
            for direction in traversalGraph[room]:
                if traversalGraph[room][direction] == '?':
                    qs.append(direction)
            if len(qs) == 0:
                visited.add(room)



'''
reverse_path = []
visited = {}
first attempt dft with 
-random direction selection 900 - 1002 moves
-remove last direction in list 997 moves
-remove first direction in list 998 moves 

while len(visited) < len(room_graph) - 1:

    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()
        #print("ADD ROOM TO VISITED", visited)
    if len(reverse_path) > 0:
        if reverse_path[-1]:
            #print("REVERSE PATH BEFORE", reverse_path)
            visited[player.current_room.id].remove(reverse_path[-1])
            #print("VISITED AFTER REMOVING PREV DIRECTION", visited)
        else:

            continue
    
    while len(visited[player.current_room.id]) == 0:
        previous_path = reverse_path.pop()
        traversal_path.append(previous_path)
        player.travel(previous_path)
        #print(str(player.current_room.id).zfill(3), end=" -> ")

    rand_direction = random.randint(0, len(visited[player.current_room.id])-1)
    #get the number of paths in a given room
    #len(room_graph[player.current_room.id][1]))

    #array of rooms connected to current room
    #print(list(room_graph[player.current_room.id][1].values()))
    
    next_direction = visited[player.current_room.id].pop()
    traversal_path.append(next_direction)
    reverse_path.append(opposite_direction[next_direction])
    #print("REVERSE PATH", reverse_path)
    player.travel(next_direction)
    #print("TRAVERSAL PATH", traversal_path)
    #print(str(player.current_room.id).zfill(3), end=" -> ")
    
'''


# pseudocode
# BFS(graph, startVert):
#   for v of graph.vertexes:
#     v.color = white
#   startVert.color = gray
#   queue.enqueue(startVert)
#   while !queue.isEmpty():
#     u = queue[0]  // Peek at head of queue, but do not dequeue!
#     for v of u.neighbors:
#       if v.color == white:
#         v.color = gray
#         queue.enqueue(v)
#     queue.dequeue()
#     u.color = black


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

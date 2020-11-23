from room import Room
from player import Player
from world import World
import math
import random
from ast import literal_eval

# Load world
world = World()

#Goals 
#make last move land on dead end

# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

opposite_direction = {
    's': 'n',
    'n': 's',
    'e': 'w',
    'w': 'e'
}

reverse_path = []

visited = {}
print(str(player.current_room.id).zfill(3), end=" -> ")
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
        print(str(player.current_room.id).zfill(3), end=" -- ")

    rand_direction = random.randint(0, len(visited[player.current_room.id])-1)
    #get the number of paths in a given room
    #len(room_graph[player.current_room.id][1]))

    #array of rooms connected to current room
    #print(list(room_graph[player.current_room.id][1].values()))
    
    next_direction = visited[player.current_room.id].pop(rand_direction)
    traversal_path.append(next_direction)
    reverse_path.append(opposite_direction[next_direction])
    #print("REVERSE PATH", reverse_path)
    player.travel(next_direction)
    #print("TRAVERSAL PATH", traversal_path)
    print(str(player.current_room.id).zfill(3), end=" -> ")
    

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

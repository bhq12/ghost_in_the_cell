import sys
import math
import copy

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

FACTORY_TYPE = "FACTORY"
TROOP_TYPE = "TROOP"

NEUTRAL_FACTORY = 0
OWNED_FACTORY = 1
ENEMY_FACTORY = -1

class Factory:
	def __init__(self, id):
		self.neighbours = dict()
		self.id = id
		self.owner = 0
		self.cyborg_count = 0
		self.production = 0
		
	def add_neighbour(self, neighbour, cost):
		self.neighbours[neighbour] = cost
		
	def __str__(self):
		rep = "factory - ID: " + str(self.id) + " neighbours: ["
		for neighbour in self.neighbours.keys():
			rep += " id " + str(neighbour.id)
			rep += "cost" + str(self.neighbours[neighbour]) + ","
		rep += "]"
		return rep
		
	def __repr__(self):
		rep = "factory - ID " + str(self.id)# + " neighbours: ["
		#for neighbour in self.neighbours.keys():
		#	rep += " id " + str(neighbour.id)
		#	rep += "cost" + str(self.neighbours[neighbour]) + ","
		#rep += "]"
		return rep

def find_shortest_paths(starting_factory):
	visited = {starting_factory : 0}
	
	path = {}
	
	nodes = set(factories.values())
	
	while nodes: 
		min_node = None
		for node in nodes:
			#print("node: " + str(node.id) + "visited:" + str(node in visited.keys()), file=sys.stderr)
			if node in visited.keys():
				if min_node is None:
					min_node = node
				elif visited[node] < visited[min_node]:
					min_node = node
		#print("min node: " + str(min_node), file=sys.stderr)
		if min_node is None:
			break

		nodes.remove(min_node)
		current_weight = visited[min_node]
		#print("min node: " + str(min_node), file=sys.stderr)
		#print("neighbs: " + str(min_node.neighbours.items()), file=sys.stderr)
		for edge, cost in min_node.neighbours.items():
			#print("edge: " + str(edge) + " cost: " + str(cost), file=sys.stderr)
			weight = current_weight + cost
			if edge not in visited or weight < visited[edge]:
				visited[edge] = weight
				path[edge] = min_node
				
	return visited, path

def initialise():
	factory_count = int(input())  # the number of factories
	for i in range(factory_count):
		factories[i] = Factory(i)
	link_count = int(input())  # the number of links between factories
	for i in range(link_count):
		factory_1, factory_2, distance = [int(j) for j in input().split()]
		#print("1: " + str(factory_1) + " 2: " + str(factory_2), file=sys.stderr)
		factories[factory_1].add_neighbour(factories[factory_2], distance)
		factories[factory_2].add_neighbour(factories[factory_1], distance)

		
def read_current_game_status():
	entity_count = int(input())	 # the number of entities (e.g. factories and troops)
	for i in range(entity_count):
		entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
		print("id: " + entity_id + " entity: " + entity_type, file=sys.stderr)
		entity_id = int(entity_id)
		arg_1 = int(arg_1)
		arg_2 = int(arg_2)
		arg_3 = int(arg_3)
		arg_4 = int(arg_4)
		arg_5 = int(arg_5)
		if entity_type == FACTORY_TYPE:
			fac = factories[entity_id]
			fac.owner = arg_1
			fac.cyborg_count = arg_2
			fac.production = arg_3
		if entity_type == TROOP_TYPE:
			#implement troops later
			do_nothing = True
	
factories = dict()
initialise()
owned_factories = set()
neutral_factories = set()
enemy_factories = set()

def seperate_factories():
	owned_factories = set()
	neutral_factories = set()
	enemy_factories = set()

	for fac in factories.values():
		if fac.owner == OWNED_FACTORY:
			owned_factories.add(fac)
		elif fac.owner == ENEMY_FACTORY:
			enemy_factories.add(fac)
		else:
			neutral_factories.add(fac)

print("factories: " + str(factories), file=sys.stderr)
# game loop
while True:
	read_current_game_status()
	
	
	
	
	print("owned: " + str(owned_factories), file=sys.stderr)
	print("neutral: " + str(neutral_factories), file=sys.stderr)
	print("enemy: " + str(enemy_factories), file=sys.stderr)
	
	largest_owned = factories[0]
	
	for fac in owned_factories:
		if fac.cyborg_count >= largest_owned.cyborg_count:
			largest_owned = fac
	
	visited, next_steps = find_shortest_paths(largest_owned)
	lowest_cost = None
	attacking_fac = None
	for fac, cost in visited.items():
		if fac in next_steps.keys() and fac not in owned_factories and (lowest_cost == None or cost < lowest_cost):
			attacking_fac = fac
			lowest_cost = cost
	
	print("attacking_fac " + str(attacking_fac), file=sys.stderr)
	print("next_steps " + str(next_steps), file=sys.stderr)
	
	next_step = next_steps[attacking_fac]
	
	print("MOVE " + str(largest_owned.id) + " " + str(attacking_fac.id) + " " + str(largest_owned.cyborg_count // 2))
	#print("shortest visited, paths: " + str(visited) + "||||" + str(next_steps), file=sys.stderr)
	#for f in factories.keys():
	#	print(owned_factories, file=sys.stderr)
	#	if f.owner == OWNED_FACTORY:
	#		owned_factories.append(f)

	print(owned_factories, file=sys.stderr)
	# Write an action using print
	# To debug: print >> sys.stderr, "Debug messages..."


	# Any valid action, such as "WAIT" or "MOVE source destination cyborgs"
	print("WAIT")

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

class Troop:
	def __init__(self, id, owner, source, destination, cyborg_count, turns_before_arrival):
		self.id = id
		self.owner = owner
		self.source = source
		self.destination = destination
		self.cyborg_count = cyborg_count
		self.turns_before_arrival = turns_before_arrival

class Factory:
	def __init__(self, id):
		self.neighbours = dict()
		self.id = id
		self.owner = 0
		self.cyborg_count = 0
		self.prev_cyborg_count = 0
		self.production = 0
		self.needs_help = False
		self.turns_to_help = 0
		self.important_count = 0
		self.unimportant_count = 0
		
	def add_neighbour(self, neighbour, cost):
		self.neighbours[neighbour] = cost
		
	def set_cyborg_count(self, count):
		self.prev_cyborg_count = self.cyborg_count
		self.cyborg_count = count
		if self.cyborg_count - self.prev_cyborg_count == 3:
			self.important_count += 1
		else:
			self.important_count = 0
		
		if self.cyborg_count - self.prev_cyborg_count == 0:
			self.unimportant_count += 1
		else:
			self.unimportant_count = 0
		
		if self.important_count >= 2:
			important_factories.add(self)
		if self.unimportant_count >= 4:
			unimportant_factories.add(self)
	
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
	global troops
	troops = set()
	entity_count = int(input()) # the number of entities (e.g. factories and troops)
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
			fac.prev_cyborg_count = fac.cyborg_count
			fac.cyborg_count = arg_2
			fac.set_cyborg_count(arg_2)
			fac.production = arg_3
		if entity_type == TROOP_TYPE:
			troops.add(Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5))
			#implement troops later
			do_nothing = True

def seperate_factories():
	global owned_factories
	global neutral_factories
	global enemy_factories
	
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
			
	print("neutral inside: " + str(neutral_factories), file=sys.stderr)

def plan_first_turn():
	#print("facs: " + str(factories), file=sys.stderr)
	#print("owned: " + str(owned_factories), file=sys.stderr)
	#print("neutral: " + str(neutral_factories), file=sys.stderr)
	#print("enemy: " + str(enemy_factories), file=sys.stderr)
	starting_factory = None
	for fac in owned_factories:
		starting_factory = fac
	move = ""
	
	print("starting_factory: " + str(starting_factory.id), file=sys.stderr)
	for neighbour in starting_factory.neighbours:
		print("neighbour: " + str(neighbour.id), file=sys.stderr)
		move += "MOVE " + str(starting_factory.id) + " " + str(neighbour.id) + " 1;"
	print(move[:-1])
	
def plan_factory_turn(factory):
	move = ""
	important_move = ""
	unimportant_move = ""
	for neighbour, cost in factory.neighbours.items():
		if neighbour not in owned_factories:
			
			if factory.cyborg_count > neighbour.cyborg_count + 2 * cost and neighbour not in unimportant_factories:
				move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 2 * cost)
			if factory.cyborg_count > neighbour.cyborg_count + 2 * cost and neighbour in important_factories:
				important_move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 2 * cost)
			if factory.cyborg_count > neighbour.cyborg_count + 2 * cost and neighbour in unimportant_factories:
				unimportant_move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 1 + cost)
			
	for neighbour, cost in factory.neighbours.items():
		if neighbour in owned_factories:
			if neighbour.needs_help and self.turns_to_help < cost and factory.cyborg_count > 5:
				move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " 5"
		
	
	targeting_troops = [t for t in troops if t.destination == factory]
	
	for t in targeting_troops:
		if t.cyborg_count > factory.cyborg_count - t.turns_before_arrival:
			move = ""
			factory.needs_help = True
		elif t.cyborg_count > factory.cyborg_count and t.turns_before_arrival == 1:
			for neighbour in factory.neighbours:
				if neighbour in owned_factories:
					move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(factory.cyborg_count)
		else:
			factory.needs_help = False
	
	if len(targeting_troops) == 0:
		factory.needs_help = False
	
	if important_move != "":
		return important_move
	elif move != "":
		return move
	else:
		return unimportant_move

def plan_turn():
	turn = ""
	for factory in owned_factories:
		move = plan_factory_turn(factory)
		if move != "":
			turn += move + ";"
	if turn != "":
		print(turn[:-1])
	else:
		print("WAIT")
	
factories = dict()
initialise()
owned_factories = set()
neutral_factories = set()
enemy_factories = set()
first_turn = True
troops = set()
important_factories = set()
unimportant_factories = set()

print("factories: " + str(factories), file=sys.stderr)

# game loop
while True:

	
	read_current_game_status()
	seperate_factories()
	print(important_factories, file=sys.stderr)
	if first_turn == True:
		plan_first_turn()
		first_turn = False
	else:
		plan_turn()

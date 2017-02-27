import sys
import math
import random

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
		self.diff = 0
		self.diff_count = 0
		self.production = 0
		
	def add_neighbour(self, neighbour, cost):
		self.neighbours[neighbour] = cost
		
	def set_cyborg_count(self, count):
		self.prev_cyborg_count = self.cyborg_count
		self.cyborg_count = count
		prev_diff = self.diff
		diff = self.cyborg_count - self.prev_cyborg_count
		if diff == prev_diff:
			self.diff_count += 1
		
		if self.diff_count >= 3:
			self.production = diff
		
		if diff >= 3:
			self.important_count += 1
		else:
			self.important_count = 0
		
		
		#detect 3-generators early
		if self.important_count >= 2:
			important_factories.add(self)
	
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
			fac.cyborg_count = arg_2
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
	cyborgs = starting_factory.cyborg_count
	print("starting_factory: " + str(starting_factory.id), file=sys.stderr)
	neighbour_count = len(starting_factory.neighbours)
	
	for neighbour in starting_factory.neighbours:
		print("neighbour: " + str(neighbour.id), file=sys.stderr)
		if cyborgs > neighbour.cyborg_count and neighbour.production != 0:
			move += "MOVE " + str(starting_factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 1) +";"
			cyborgs -= (neighbour.cyborg_count + 1)
	if move != "":
		print(move[:-1])
	else:
		print("WAIT")
	
	
def plan_factory_turn(factory):
	global bomb_count
	global bombed_factories
	global front_line
	global target
	move = ""
	move_priority = 0
	important_move = ""
	
	targeting_troops = [t for t in troops if t.destination == factory.id and t.owner == ENEMY_FACTORY]
	approaching_cyborgs = 0
	for t in troops:
		if t.destination == factory.id and t.owner == ENEMY_FACTORY:
			approaching_cyborgs += t.cyborg_count
	
	if approaching_cyborgs >= factory.cyborg_count:
		factory.needs_help = True
	else:
		factory.needs_help = False
	
	enemy_neighbours = False
	stronger_enemy_neighbours = False
	
	for neighbour, cost in factory.neighbours.items():
		if neighbour not in owned_factories:
			enemy = True
			if neighbour.cyborg_count + approaching_cyborgs > factory.cyborg_count - 10:
				stronger_enemy_neighbours = True
				
			
			if factory.cyborg_count > neighbour.cyborg_count + 2 * cost and neighbour.production != 0 and neighbour.production > move_priority and not factory.needs_help:
				move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 2 * cost)
				move_priority = neighbour.production
			if factory.cyborg_count > neighbour.cyborg_count + 3 * cost and neighbour.production == 3 and approaching_cyborgs < factory.cyborg_count and not factory.needs_help:
				attack_cyborg_count = (neighbour.cyborg_count + (3 * cost)) + 1
				important_move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(attack_cyborg_count)
			if neighbour in enemy_factories and neighbour.production >= 2 and bomb_count > 0 and neighbour not in bombed_factories:
				destination_troops = [t for t in troops if t.destination == factory.id and t.owner == OWNED_FACTORY]
				if len(destination_troops) > 0:
					important_move = "BOMB " + str(factory.id) + " " + str(neighbour.id)
					bomb_count -= 1
					bombed_factories.add(neighbour)
	
	for neighbour, cost in factory.neighbours.items():
		if neighbour in owned_factories:
			if neighbour.needs_help and not factory.needs_help and factory.cyborg_count > 15 and neighbour.production >= 2 and factory.neighbours[neighbour] < 5:
				important_move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " 5; MSG HELP_SENT" 
				#do_this = False
		
	if stronger_enemy_neighbours == False and factory.production >= 2:
		visited, paths = find_shortest_paths(factory)
		if target == factory:
			target = None
		
		for fac in factories.values():
			if (target is None or fac.production > target.production) and fac not in owned_factories:
				target = fac
		#if paths[target].production == 0 or paths[target] == factory:
		
		if paths[target].production == 0 and paths[target] != factory and not factory.needs_help:
			important_move = "MOVE " + str(factory.id) + " " + str(paths[target].id) + " 10"
		elif paths[target] != factory and not factory.needs_help:
			important_move = "MOVE " + str(factory.id) + " " + str(paths[target].id) + " " + str(factory.cyborg_count // 3)
			
	if enemy_neighbours == False:
		if target == factory:
			target = None
		visited, paths = find_shortest_paths(factory)
		if target is not None and paths[target] != factory and not factory.needs_help:
			important_move = "MOVE " + str(factory.id) + " " + str(paths[target].id) + " " + str(factory.cyborg_count // 2)
	
	if important_move != "":
		return important_move
	else:
		return move

	bomb_cooldown -= 1
	return move
def plan_turn():
	turn = ""
	for factory in owned_factories:
		move = plan_factory_turn(factory)
		if factory.production < 3 and factory.cyborg_count >= 20 and not factory.needs_help:
			move = "INC " + str(factory.id)

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
front_line = set()
first_turn = True
troops = set()
important_factories = set()
bomb_count = 2
bombed_factories = set()
target = None
print("factories: " + str(factories), file=sys.stderr)

iterator = 0
# game loop
while True:
	iterator += 1
	if iterator % 10 == 0:
		target = None
	read_current_game_status()
	seperate_factories()
	if first_turn == True:
		plan_first_turn()

		first_turn = False
	else:
		plan_turn()

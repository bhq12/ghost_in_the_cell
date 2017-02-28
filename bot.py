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
		self.attacking_troops = 0
		self.usable_cyborgs = 0
		
	def add_troop(self, troop):
	
		
		if troop.owner != self.owner:
			self.usable_cyborgs -= (troop.cyborg_count - self.production * troop.turns_before_arrival)
			self.attacking_troops += troop.cyborg_count
		else:
			self.usable_cyborgs += (troop.cyborg_count - self.production * troop.turns_before_arrival)
	
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
		rep = "factory - ID " + str(self.id) + "US " + str(self.usable_cyborgs)# + " neighbours: ["
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
	global largest_production
	troops = set()
	entity_count = int(input()) # the number of entities (e.g. factories and troops)
	for i in range(entity_count):
		entity_id, entity_type, arg_1, arg_2, arg_3, arg_4, arg_5 = input().split()
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
			fac.usable_cyborgs = arg_2
			fac.production = arg_3
			if fac.production > largest_production:
				largest_production = fac.production
		if entity_type == TROOP_TYPE:
			dest = arg_3
			new_troop = Troop(entity_id, arg_1, arg_2, arg_3, arg_4, arg_5) 
			troops.add(new_troop)
			factories[dest].add_troop(new_troop)

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
	
	neighbours = list(starting_factory.neighbours.keys())
	neighbours.sort(key=lambda x: x.production, reverse=True)
	
	for neighbour in neighbours:
		if neighbour.owner == ENEMY_FACTORY and neighbour.production >= largest_production - 1:
			move += "BOMB " + str(starting_factory.id) + " " + str(neighbour.id) + ";"
			bombed_factories.add(neighbour.id)
		
		print("neighbour: " + str(neighbour.id), file=sys.stderr)
		if cyborgs > neighbour.cyborg_count and neighbour.production != 0 and starting_factory.neighbours[neighbour] < 10:
			move += "MOVE " + str(starting_factory.id) + " " + str(neighbour.id) + " " + str(neighbour.cyborg_count + 1) +";"
			cyborgs -= (neighbour.cyborg_count + 1)
	if move != "":
		print(move[:-1])
	else:
		print("WAIT")

def plan_turn():
	turn = ""
	move = ""
	for factory in owned_factories:
		#move = plan_factory_turn(factory)
		move = improved_turn(factory)
		if factory.production < 3 and factory.usable_cyborgs >= 40 and factory.cyborg_count >= 25:
			move = "INC " + str(factory.id)

		if move != "" and factory.usable_cyborgs >= 5:
			turn += move + ";"
			
	if turn != "":
		print(turn[:-1])
	else:
		print("WAIT")
	
	
def improved_turn(factory):
	global bomb_count
	global bombed_factories
	#costs, next_steps = find_shortest_paths(factory)
	#print(str(factory.id) + " nexts: " + str(next_steps), file=sys.stderr)
	#print(str(factory.id) + " costs: " + str(costs), file=sys.stderr)
	
	move_troops = None
	move_fac = None
	
	factory_move_priority = None
	move = ""
	for neighbour, cost in factory.neighbours.items():
		#print("id: " + str(fac.id) + " borgs: " + str(fac.cyborg_count) + "usable: " + str(fac.usable_cyborgs), file=sys.stderr)
		if neighbour.owner != OWNED_FACTORY:
			#next_step = next_steps[fac]
			#smallest_cost = costs[fac]
			
			if neighbour.owner == NEUTRAL_FACTORY:
				overtake_borgs = neighbour.cyborg_count + 4
			else:
				overtake_borgs = neighbour.cyborg_count + neighbour.production * (cost + 1) + 3
			repayment_period = overtake_borgs / (neighbour.production + 0.01)
			
			move_priority = 100 * neighbour.production - cost #- repayment_period
			
			
			if repayment_period > 5 or (neighbour.owner == NEUTRAL_FACTORY and neighbour.attacking_troops >= factory.usable_cyborgs):
				move_priority = -1000000
			
			superior_move = (factory_move_priority is None or move_priority > factory_move_priority)
			
			
			if superior_move and factory.usable_cyborgs > overtake_borgs and neighbour.production != 0 and factory.attacking_troops <= factory.cyborg_count - 5:

				if overtake_borgs <= 0:
					overtake_borgs = 2
				factory_move_priority = move_priority
				move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(overtake_borgs)
				neighbour.cyborg_count += overtake_borgs
				print("MV: " + str(move_priority) + move, file=sys.stderr)
				move_fac = neighbour
				move_troops = Troop(None, OWNED_FACTORY, factory.id, neighbour.id, overtake_borgs, cost)
			
			if neighbour.production == largest_production and neighbour.owner == ENEMY_FACTORY and bomb_count > 0 and neighbour not in bombed_factories:
				factory_move_priority = 10000
				move = "BOMB " + str(factory.id) + " " + str(neighbour.id)
				bomb_count -= 1
				bombed_factories.add(neighbour)
			
		elif neighbour.owner == OWNED_FACTORY:
			if neighbour.usable_cyborgs <= 0:
				move_priority = 10 * neighbour.production - cost
				
				help_borgs = abs(neighbour.usable_cyborgs) + cost * neighbour.production
				
				repayment_period = help_borgs / (neighbour.production + 0.01)
				
				if repayment_period > 5:
					move_priority = 0
				
				superior_move = (factory_move_priority is None or move_priority > factory_move_priority)
				if superior_move and factory.usable_cyborgs > help_borgs + 10:
				
					move = "MOVE " + str(factory.id) + " " + str(neighbour.id) + " " + str(help_borgs)
					factory_move_priority = move_priority
					move_fac = neighbour
					move_troops = Troop(None, OWNED_FACTORY, factory.id, neighbour.id, help_borgs, cost)
	
	
	if factory.usable_cyborgs > 5:
		if move_fac is not None:
			move_fac.add_troop(move_troops)
		return move
	else:
		return ""
		

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
largest_production = 0


iterator = 0
# game loop
while True:
	iterator += 1
	if iterator % 10 == 0:
		target = None
	read_current_game_status()
	print("facs " + str(factories), file=sys.stderr)
	seperate_factories()
	if first_turn == True:
		plan_first_turn()
		#plan_turn()

		first_turn = False
	else:
		plan_turn()

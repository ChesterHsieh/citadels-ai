from random import randrange

class Color(object):
	def __init__(self,full_name):
		self.full_name=full_name
		self.display_name=full_name[0]

	def __str__(self):
		return self.display_name

class Game(object):
	RED=Color("Red")
	BLUE=Color("Blue")
	PURPLE=Color("Purple")
	YELLOW=Color("Yellow")
	GREEN=Color("Green")
	WHITE=Color("White")
	COLORS=[RED,BLUE,PURPLE,YELLOW,GREEN,WHITE]

	def str_2_color(color_str):
		for color in Game.COLORS:
			if color_str==color.full_name.lower():
				return color
		print("Could not find a match for color str "+color_str)
		return None

	def __init__(self,num_comp_players,num_human_players,special_cards):
		self.players=[]
		self.district_deck=[]
		self.class_draw=[]
		self.class_discard=[]

		self.add_standard_district_cards()

		self.add_standard_character_cards()

		for comp_slot in range(num_comp_players):
			self.players.append(Player("P"+str(comp_slot)))

		for a_player in self.players:
			a_player.bank_gives(2)

	def set_player_as_king(self,player_name):
		for a_player in self.players:
			if player_name==a_player.name:
				a_player.set_as_king()
			else:
				a_player.set_as_not_king()

	def choose_king_randomly(self):
		king_index = randrange(0,len(self.players))
		king=self.players[king_index]
		print(king.name)
		self.set_player_as_king(king.name)

	def add_standard_district_cards(self):
		with open("districtCards.csv") as f:
			for line in f:
				name,cost,color_str=line.split(",")
				constructed_card=DistrictCard(name.strip(),int(cost.strip()),Game.str_2_color(color_str.strip()))
				self.district_deck.append(constructed_card)

	def add_standard_character_cards(self):
		self.class_draw.append(CharacterCard("Assassin",1,Game.WHITE))
		self.class_draw.append(CharacterCard("Thief",2,Game.WHITE))
		self.class_draw.append(CharacterCard("Magician",3,Game.WHITE))
		self.class_draw.append(CharacterCard("King",4,Game.YELLOW))
		self.class_draw.append(CharacterCard("Bishop",5,Game.BLUE))
		self.class_draw.append(CharacterCard("Merchant",6,Game.GREEN))
		self.class_draw.append(CharacterCard("Architect",7,Game.WHITE))
		self.class_draw.append(CharacterCard("Warlord",8,Game.RED))


	def draw_district_cards(player,num):
		for i in range(num):
			player.get_district_card(self.district_deck.pop(0))

	def __str__(self):
		to_return="<The Game>\n"
		to_return+="  DDeck: ["+str(len(self.district_deck))+"]\n"
		to_return+="  CDeck: ["+str(len(self.class_draw))+"]\n"
		for i, a_player in enumerate(self.players):
			if a_player.is_king:
				to_return+="**"+str(a_player)+"**\n"
			else:
				to_return+="  "+str(a_player)+"\n"

		to_return+="</The Game>\n"
		return to_return



class Player(object):
	def __init__(self,name):
		self.gold=0
		self.district_hand=[]
		self.class_hand=[]
		self.district_played=[]
		self.name=name
		self.is_king=False

	def bank_gives(self,amount):
		self.gold+=amount

	def bank_takes(self,amount):
		if self.gold-amount<0:
			print("Not enough gold!")
		else:
			self.gold-=amount

	def get_district_card(self,card):
		self.district_hand.append(card)

	def set_as_king(self):
		self.is_king=True

	def set_as_not_king(self):
		self.is_king=False

	def __str__(self):
		return "<"+self.name+"  DHand: ["+str(len(self.district_hand))+"] CHand: "+str(self.class_hand)+" "+str(self.gold)+">"

class DistrictCard(object):
	def __init__(self,name,cost,color):
		self.name=name
		self.cost=cost
		self.color=color

	def __str__(self):
		return "<"+self.name+" "+str(self.cost)+" "+str(self.color)+">"

	def __repr__(self):
		return self.__str__()

class CharacterCard(object):
	def __init__(self,name,key,color):
		self.name=name
		self.key=key
		self.color=color
	
	def __str__(self):
		return self.name

if __name__ == "__main__":
	#deform to form a star
	the_game=Game(3,0,False)
	the_game.choose_king_randomly()
	# print(Game.str_2_color("red"))

	print(the_game)
	
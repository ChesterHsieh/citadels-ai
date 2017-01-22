from random import randrange
from operator import attrgetter

class Color(object):
	def __init__(self,full_name):
		self.full_name=full_name
		self.display_name=full_name[0]

	def __str__(self):
		return self.display_name

class Game(object):
	ASSASSIN=1
	THIEF=2
	MAGICIAN=3
	KING=4
	BISHOP=5
	MERCHANT=6
	ARCHITECT=7
	WARLORD=8

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
		self.computer_players=[]
		self.district_deck=[]
		self.character_deck=[]
		self.character_discard=[]
		self.PERM_TURN_ORDER=[]

		self.add_standard_district_cards()

		self.add_standard_character_cards()

		for comp_slot in range(num_comp_players):
			a_player=Player("P"+str(comp_slot))
			self.computer_players.append(a_player)
			self.players.append(a_player)

		for a_player in self.players:
			a_player.bank_gives(2)
			self.draw_district_cards(a_player,4)

	#this only happens once when character cards are originally chosen
	def calc_perm_turn_order(self):
		self.PERM_TURN_ORDER=sorted(self.character_deck,key=attrgetter("key"))

	def get_player_with_character(self,character):
		for a_player in self.players:
			if character in a_player.character_hand:
				return a_player
		return None

	def set_new_king(self):
		for a_player in self.players:
			for character in a_player.character_hand:
				if character==Game.KING:
					set_player_as_king(a_player.name)

	def set_player_as_king(self,player_name):
		for a_player in self.players:
			if player_name==a_player.name:
				a_player.set_as_king()
			else:
				a_player.set_as_not_king()

	def choose_king_randomly(self):
		king_index = randrange(0,len(self.players))
		king=self.players[king_index]
		self.set_player_as_king(king.name)

	def recalc_turn_order(self):
		before_king=[]
		king_and_after=[]
		is_before_king=True
		for player in self.players:
			if player.is_king:
				is_before_king=False
			if is_before_king:
				before_king.append(player)
			else:
				king_and_after.append(player)
		self.players=king_and_after+before_king


	def add_standard_district_cards(self):
		with open("districtCards.csv") as f:
			for line in f:
				name,cost,color_str=line.split(",")
				constructed_card=DistrictCard(name.strip(),int(cost.strip()),Game.str_2_color(color_str.strip()))
				self.district_deck.append(constructed_card)

	def add_standard_character_cards(self):
		self.character_deck.append(CharacterCard("Assassin",1,Game.WHITE))
		self.character_deck.append(CharacterCard("Thief",2,Game.WHITE))
		self.character_deck.append(CharacterCard("Magician",3,Game.WHITE))
		self.character_deck.append(CharacterCard("King",4,Game.YELLOW))
		self.character_deck.append(CharacterCard("Bishop",5,Game.BLUE))
		self.character_deck.append(CharacterCard("Merchant",6,Game.GREEN))
		self.character_deck.append(CharacterCard("Architect",7,Game.WHITE))
		self.character_deck.append(CharacterCard("Warlord",8,Game.RED))

	def collect_all_characters(self):
		temp_characters=[]
		for a_player in self.players:
			temp_characters+=a_player.character_played
			a_player.character_played=[]
		temp_characters+=self.character_discard
		self.character_discard=[]
		self.character_deck=temp_characters

	def draw_district_cards(self,player,num):
		to_return=[]
		for i in range(num):
			card=self.district_deck.pop(0)
			player.get_district_card(card)
			to_return.append(card)
		return to_return

	def draw_character_card(self,player):
			player.get_character_card(self.character_deck.pop(0))

	def flip_over_character_card(self):
		self.character_discard.append(self.character_deck.pop())

	def __str__(self):
		to_return="<The Game>\n"
		to_return+="  DDeck: ["+str(len(self.district_deck))+"]\n"
		to_return+="  CDeck: ["+str(len(self.character_deck))+"]\n"
		to_return+="  CDiscard: ["+str(len(self.character_discard))+"]\n"
		for i, a_player in enumerate(self.players):
			if a_player.is_king:
				to_return+="**"+str(a_player)+"**\n"
			else:
				to_return+="  "+str(a_player)+"\n"

		to_return+="</The Game>"
		return to_return


class Player(object):
	def __init__(self,name):
		self.gold=0
		self.district_hand=[]
		self.character_hand=[]
		self.district_played=[]
		self.character_played=[]
		self.name=name
		self.is_king=False
		self.brain=None

	def bank_gives(self,amount):
		self.gold+=amount

	def bank_takes(self,amount):
		if self.gold-amount<0:
			print("Not enough gold!")
		else:
			self.gold-=amount

	def build_district(self,card):
		self.bank_takes(card.cost)
		self.district_hand.remove(card)
		self.district_played.append(card)

	def play_character(self,card):
		self.character_hand.remove(card)
		self.character_played.append(card)

	def get_district_card(self,card):
		self.district_hand.append(card)

	def discard_district_card(self,card):
		self.district_hand.remove(card)

	def get_character_card(self,card):
		self.character_hand.append(card)

	def lose_district_card(self,card):
		index=None
		self.district_played.remove(card)
		return card

	def set_as_king(self):
		self.is_king=True

	def set_as_not_king(self):
		self.is_king=False

	def __str__(self):
		return "<"+self.name+"  DHand: ["+str(len(self.district_hand))+"] CHand: "+str(self.character_hand)+" "+str(self.gold)+" "+str(self.district_played)+">"

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
	
	def __repr__(self):
		return self.__str__()

	def __str__(self):
		return self.name

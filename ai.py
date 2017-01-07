from abc import ABCMeta, abstractmethod
import random
from core import *

class Brain(object):
	def __init__(self,game,player):
		self.player=player
		self.player.brain=self
		self.game=game

	def meta_choose_character(self):
		character=self.choose_character(self.game.character_deck)
		self.player.get_character_card(character)
		self.game.character_deck.remove(character)

	@abstractmethod
	#true for coin false for card
	def choose_card_or_coin(self,current_character):
		raise NotImplementedError

	@abstractmethod
	def choose_character(self,character_deck):
		raise NotImplementedError

	@abstractmethod
	def choose_district_discard(self,choices):
		raise NotImplementedError

	@abstractmethod
	def choose_build(self):
		raise NotImplementedError

class CompBrain(Brain):

	def choose_character(self,character_deck):
		return random.choice(character_deck)

	def choose_card_or_coin(self,current_character):
		if current_character==Game.ARCHITECT:
			return True
		if len(self.player.district_hand)<1:
			return False
		return True

	def choose_district_discard(self,choices):
		to_keep=choices
		to_discard=None
		for district in choices:
			if district.cost>self.player.gold+3:
				to_discard=district
				to_keep.remove(district)
				break
		if to_discard==None:
			to_discard=to_keep.pop()

	def choose_build(self):
		for district in self.player.district_hand:
			if district.cost<=self.player.gold:
				return district


def connect_ai_with_players(game):
	for comp_player in game.computer_players:
		CompBrain(game,comp_player)


if __name__ == "__main__":
	#deform to form a star
	the_game=Game(3,0,False)
	connect_ai_with_players(the_game)
	the_game.calc_perm_turn_order()
	the_game.choose_king_randomly()
	the_game.recalc_turn_order()
	the_game.flip_over_character_card()

	while(True):

		if len(the_game.players)>4:
			character_pick_rounds=1
		else:
			character_pick_rounds=2

		#evaluate character pick turn
		for character_pick_round in range(character_pick_rounds):		
			for player in the_game.players:
				player.brain.meta_choose_character()

		the_game.flip_over_character_card()

		print(the_game)

		#evaluate player order
		for character in the_game.PERM_TURN_ORDER:
			current_player=the_game.get_player_with_character(character)
			if current_player==None:
				continue
			#Player turn here:
			print(str(current_player)+" as "+str(character))
			if current_player.brain.choose_card_or_coin(character):
				current_player.bank_gives(2)
				print(" Took coins")
			else:
				drawn=the_game.draw_district_cards(current_player,2)
				discarded=current_player.brain.choose_district_discard(drawn)
				current_player.discard_district_card(discarded)
				print(" Drew "+str(drawn)+", discarded "+str(discarded))

			#Build Phase
			to_build=current_player.brain.choose_build()
			if to_build!=None:
				current_player.build_district(to_build)
				print(" Built "+str(to_build))

			#TODO: technically the character is played at the beginning of the turn, but we look at character in hand for stuff so can't do that yet
			current_player.play_character(character)

		#end of turn clean up
		#TODO: technically king is set when king character is evaluated, only recalc turn order later
		the_game.set_new_king()
		the_game.recalc_turn_order()

		the_game.collect_all_characters()

		print(the_game)
		input()
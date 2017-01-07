from abc import ABCMeta, abstractmethod
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
	def choose_character(self,character_deck):
		raise NotImplementedError

class CompBrain(Brain):

	def choose_character(self,character_deck):
		return character_deck[0]

def connect_ai_with_players(game):
	for comp_player in game.computer_players:
		CompBrain(game,comp_player)


if __name__ == "__main__":
	#deform to form a star
	the_game=Game(3,0,False)
	connect_ai_with_players(the_game)
	the_game.choose_king_randomly()
	the_game.recalc_turn_order()
	the_game.flip_over_character_card()

	if len(the_game.players)>4:
		character_pick_rounds=1
	else:
		character_pick_rounds=2

	for character_pick_round in range(character_pick_rounds):		
		for player in the_game.players:
			player.brain.meta_choose_character()

	the_game.flip_over_character_card()



	print(the_game)
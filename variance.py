# variance.py
# File mainly used to hold the definition of the strength of an audio feature
# Each variant is a range of numbers with upper and lower bounds
import random

strength_variants = ['low','low-medium','medium','medium-high','high']

#Difference between each of the levels
var_diff = 1/len(strength_variants)

class Variant:
	def __init__(self,type):
		self.type = type
		for index, v in enumerate(strength_variants):
			if (type == 'random'):
				self.upper_bound = 1
				self.lower_bound = 0
			if (type == v):
					# Setting upper and lower bound for the variant based on position in the strength_variants array
					# Add a little bit of randomness to the upper bounds for better randomness in playlist
					self.lower_bound = (index * var_diff)
					self.upper_bound = (self.lower_bound + var_diff) + random.uniform(0,.10)
					if (self.upper_bound > 1):
						self.upper_bound = 1
			if('_t' in type):
				# Tempo has different parameters: 50 >= tempo >= 200
				MAX_TEMPO = 200
				MIN_TEMPO = 50
				if ('random' in type):
					self.lower_bound = MIN_TEMPO
					self.upper_bound = MAX_TEMPO
				else:
					TEMPO_DIFF = (MAX_TEMPO - MIN_TEMPO) / len(strength_variants)
					self.lower_bound = MIN_TEMPO 
					self.upper_bound = (self.lower_bound + (index + 1) * TEMPO_DIFF)
				

				
				
					
	
# moods.py
import variance

# Definition of each mood
UPSET = {
	'name':'upset',
	'valence': variance.Variant('low'),
	'tempo': variance.Variant('low_t'),
	'danceability': variance.Variant('low-medium'),
	#'loudness': variance.Variant('low-medium'),
	'energy': variance.Variant('low'),
	#'acousticness':variance.Variant('random')
}

YEET = {
	'name':'yeet',
	'valence': variance.Variant('high'),
	'tempo': variance.Variant('high_t'),
	'danceability': variance.Variant('high'),
	#'loudness': variance.Variant('random'),
	#'energy': variance.Variant('medium'),
	#'acousticness':variance.Variant('low')
}

BORED = {
	'name':'bored',
	'valence': variance.Variant('random'),
	'tempo': variance.Variant('random_t'),
	'danceability': variance.Variant('random'),
	#'loudness': variance.Variant('medium'),
	#'energy': variance.Variant('medium'),
	#'acousticness':variance.Variant('medium')
}

# STATIC list of moods
mood_names = ['UPSET','YEET', 'BORED']
# STATIC definitions of moods
moods = [UPSET,YEET,BORED]
# STATIC audio features considered
audio_features = ['valence','danceability','tempo']

# Mood functions
def identify_mood(mood):
    for index,item in enumerate(mood_names):
		# When the correct mood_name is found, use that mood_name's index in moods to return correct object
        if(mood.strip().upper() == item):
            return moods[index]
    return None

def in_mood_range(mood,feature,track_data):
	if ((mood[feature].type).lower().strip() == 'random'):
		return True
	else:
		return mood[feature].lower_bound <= track_data[feature] <= mood[feature].upper_bound

def within_mood(mood,track_data):
	for feature in audio_features:
		if (not(in_mood_range(mood,feature,track_data))):
			return False
	return True

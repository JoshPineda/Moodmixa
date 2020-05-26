import sys
import random
import moods
import time
import spotipy
import spotipy.util as util

# Application details from Spotify
CLIENT_ID = "CLIENT_ID"
CLIENT_SECRET = "CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8888/callback"

# What this application needs to access from user to do function
SCOPE = 'user-library-read user-top-read playlist-modify-public user-follow-read'

# Adjectives that can be attached to any given mood
#ADJ_VAL = ['VERY','PRETTY','SEMI','A LIL']

# --- Boilerplate how-to-use --- #
if len(sys.argv) > 1:
	username = sys.argv[1]
	mood_input = sys.argv[2]

else:
	print("To use the program, enter in command line (in folder with spotify.py): \'python {} username mood\'".format(sys.argv[0]))
	sys.exit()
# --- End Boilerplate --- #

# User-Authentication done through Spotipy library
token = util.prompt_for_user_token(username, SCOPE, client_id = CLIENT_ID, client_secret = CLIENT_SECRET, redirect_uri = REDIRECT_URI)


# If we have token, allow authentication with spotify
if token:
	# Authenticate Spotipy
	def authenticate_spotify():
		print("...Connecting to Spotify")
		sp = spotipy.Spotify(auth=token)
		return sp
	# Helper Method: aggregate_top_artists
	# Helps to get the URI of the artist without repeating
	def Gather_URIS(artists_all_data, top_artists_name, top_artists_uri):
		#TODO: Find out what current_user_top_artists wants and gives back
		if (artists_all_data != None):
			artist_data = artists_all_data['items']
			for artist in artist_data:
				if(artist['name'] not in top_artists_name):
					top_artists_name.append(artist['name'])
					top_artists_uri.append(artist['uri'])

	def aggregate_top_artists(sp):
		print("...Getting Top Artists")
		top_artists_name = []
		top_artists_uri = []
		ranges = ["short_term","medium_term","long_term"]

		for r in ranges:
			# Get user's top artists from across short, medium, and long term ranges 
			# i.e Last 4 weeks, 6 months, and across all time (allows for balanced top artists)
			top_artists_all_data = sp.current_user_top_artists(limit=50, time_range = r)
			Gather_URIS(top_artists_all_data,top_artists_name,top_artists_uri)

			# Also aggregates the artists they currently follow
			followed_artists_all_data = sp.current_user_followed_artists(limit=50)
			followed_artists_data = followed_artists_all_data['artists']
			Gather_URIS(followed_artists_data,top_artists_name,top_artists_uri)

			# We return the uris because they are all we need
			# Top_artists_name is so that artists are not repeated
			return top_artists_uri

	# Take each of the top artists, get their top_tracks
	def aggregate_top_tracks(sp, top_artists_uri):
		print("...Getting Top tracks")
		top_tracks_uri = []
		for artist in top_artists_uri:
			top_tracks_all_data = sp.artist_top_tracks(artist)
			top_tracks_data = top_tracks_all_data["tracks"]
			for track_data in top_tracks_data:
				templst = []
				templst.append(''.join(list(track_data['uri'])))
				top_tracks_uri.append(templst)
		return top_tracks_uri

	def select_tracks(sp, top_tracks_uri,mood):
		print("...selecting tracks")
		selected_tracks_uri = []
		random.shuffle(top_tracks_uri)
		for tracks in list(top_tracks_uri):
			tracks_all_data = sp.audio_features(tracks)
			for track_data in tracks_all_data:
				try:
					if(moods.within_mood(mood,track_data)):
						selected_tracks_uri.append(track_data['uri'])
				except TypeError as te:
					continue
		return selected_tracks_uri


	def create_playlist(sp,selected_tracks_uri):
		print("...creating playlist")
		user_all_data = sp.current_user()
		user_id = user_all_data['id']
		
		playlist_all_data = sp.user_playlist_create(user_id,"{} mood mix".format(mood['name']))
		playlist_id = playlist_all_data['id']

		random.shuffle(selected_tracks_uri)
		sp.user_playlist_add_tracks(user_id,playlist_id,selected_tracks_uri[0:30])
					
	# Main Program workflow
	mood = moods.identify_mood(mood_input)
	if (mood):
		t0 = time.time()
		sp = authenticate_spotify()
		top_artists_uri = aggregate_top_artists(sp)
		top_tracks_uri = aggregate_top_tracks(sp,top_artists_uri)
		selected_tracks_uri = select_tracks(sp,top_tracks_uri,mood)
		print(selected_tracks_uri)
		create_playlist(sp,selected_tracks_uri)
		print("Playlist created! Enjoy :)")
		t1 = time.time()
		print("Total time = {}".format(t1-t0))
	else:
		print("Not a valid mood")
		

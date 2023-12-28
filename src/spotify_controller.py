import requests
# Define a class to control Spotify playback
class SpotifyController:
	# Constructor for the class
    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
        self.token_url = "https://accounts.spotify.com/api/token"
        self.base_url = "https://api.spotify.com/v1/me/player"
    # Method to authenticate with Spotify using the authorization code
    def authenticate(self, code):
		# Payload for the POST request to get the access token
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
			# Send a POST request to Spotify's token endpoint
            auth_response = requests.post(self.token_url, data=payload)
            auth_response.raise_for_status()
            # Parse the response to JSON and extract access and refresh tokens
            auth_response_data = auth_response.json()
            self.access_token = auth_response_data['access_token']
            self.refresh_token = auth_response_data['refresh_token']
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            print(auth_response.text)
            
    # Each method checks for the access token, sets the appropriate headers,
    # sends a request to the corresponding Spotify API endpoint,
    # and handles any exceptions that occur during the request.
            
    # Method to play music on Spotify
    def play_music(self):
		# Check if the access token is available
        if self.access_token:
			# Set the authorization header with the access token
            headers = {'Authorization': f'Bearer {self.access_token}'}
            try:
				# Send a PUT request to Spotify's play endpoint
                response = requests.put(f"{self.base_url}/play", headers=headers)
                print("Response:", response.json())
                # Raise an exception for HTTP errors
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
                print("Response text:", response.text)
        else:
            print("Access token is missing. Please authenticate first.")

    def pause_music(self):
        if self.access_token:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            try:
                response = requests.put(f"{self.base_url}/pause", headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Access token is missing. Please authenticate first.")

    def next_track(self):
        if self.access_token:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            try:
                response = requests.post(f"{self.base_url}/next", headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Access token is missing. Please authenticate first.")

    def previous_track(self):
        if self.access_token:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            try:
                response = requests.post(f"{self.base_url}/previous", headers=headers)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Access token is missing. Please authenticate first.")

    def set_volume(self, volume_level):
        if self.access_token:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            params = {'volume_percent': volume_level}
            try:
                response = requests.put(f"{self.base_url}/volume", headers=headers, params=params)
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Access token is missing. Please authenticate first.")

    def check_playback_state(self):
        if self.access_token:
            headers = {'Authorization': f'Bearer {self.access_token}'}
            try:
                response = requests.get(f"{self.base_url}/currently-playing", headers=headers)
                response.raise_for_status()
                return response.json()  # Returns the current playback state
            except requests.exceptions.RequestException as e:
                print(f"An error occurred: {e}")
        else:
            print("Access token is missing. Please authenticate first.")

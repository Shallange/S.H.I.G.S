import cv2
import mediapipe as mp
import os
import urllib.parse
import time 
import threading
from auth_server import run_server
from picamera2 import Picamera2
from spotify_controller import SpotifyController
from dotenv import load_dotenv
from gesture_recognition.detector import detect_gesture

# Time of the last registered gesture
last_gesture_time = 0
# Time to wait before recognizing the next gesture in seconds
gesture_cooldown = 1.5  
# Initialize current volume level
current_volume = 50

# Initialize MediaPipe Hands module for hand tracking 
mp_hands = mp.solutions.hands

#Initialize the MediaPipe hands object
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

#Function to retrive the Spotify authentication code from a file
def get_auth_code():
    try:
        with open('auth_code.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

#Function to authenticate with Spotify
def authenticate_spotify(spotify):
    authorization_code = None
    while not authorization_code:
	    authorization_code = get_auth_code()
	    time.sleep(1)  # Wait a bit before retrying
    if authorization_code:
	    spotify.authenticate(authorization_code)
	    return True
    else:
	    return False

#Function to find the position of hand landmarks
def findposition(frame, results, hand_no=0, draw=True):
    landmark_list = []
    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[hand_no]
        for id, lm in enumerate(hand.landmark):
            h, w, c = frame.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            landmark_list.append((id, cx, cy))
            if draw:
                cv2.circle(frame, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
    return landmark_list

#Function to draw hand landmarks on the frame
def findnameoflandmark(frame, results):
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
    return frame
    
# Load environment variables from a .env file 
load_dotenv()

# Retrieve Spotify credentials from enviorment variables
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')

# Validate that all necessary Spotify credentials are loaded
if not all([client_id, client_secret, redirect_uri]):
    raise ValueError("Spotify credentials not loaded from environment variables")

#Encode the redirect URI for use in the Spotify Authorization URL
encoded_redirect_uri = urllib.parse.quote(redirect_uri)

# Construct the authorization URL with necessary scopes
scopes = "user-modify-playback-state user-read-playback-state user-read-currently-playing"
encoded_scopes = urllib.parse.quote(scopes)
auth_url = f"https://accounts.spotify.com/authorize?client_id={client_id}&response_type=code&redirect_uri={encoded_redirect_uri}&scope={encoded_scopes}"

# Print the authorization URL to the console for user action
print("Please go to the following URL and authorize the app:")
print(auth_url)

# Initialize the SpotifyController with credentials
spotify = SpotifyController(client_id, client_secret, redirect_uri)

# Start the Flask server for authentication in a separate thread
flask_thread = threading.Thread(target=run_server, daemon=True)
flask_thread.start()

# Wait for the user to confirm they have authorized the app
input("Press Enter after authorizing the app.")

if authenticate_spotify(spotify):
    # Initialize Picamera2 for capturing images
    picam2 = Picamera2()
    picam2.start_preview()
    picam2.start()

    try:
        while True:
            # Capture an image from the camera
            frame = picam2.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process the frame with MediaPipe to find hand landmarks
            results = hands.process(frame)

            # Find the position of hand landmarks and draw them
            landmarks = findposition(frame, results)
            frame = findnameoflandmark(frame, results)

            # Detect gestures based on the landmarks
            gesture = detect_gesture(landmarks)  # Use the function from detector.py
            
            # Check if a gesture is detected
            if gesture:
                current_gesture = gesture
            else:
                current_gesture = None

            # Display the detected gesture on the screen
            if current_gesture:
                cv2.putText(frame, current_gesture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

                # Perform actions based on the detected gesture
                current_time = time.time()
                if current_time - last_gesture_time > gesture_cooldown:
                    last_gesture_time = current_time
                    
                    # Spotify control based on the gesture
                    if current_gesture == "play_music":
                        spotify.play_music()
                    elif current_gesture == "pause_music":
                        spotify.pause_music()
                    elif current_gesture == "next_song":
                        spotify.next_track()
                    elif current_gesture == "previous_song":
                        spotify.previous_track()
                    elif current_gesture == "increase_volume":
                        if current_volume < 100:
                            current_volume = min(current_volume + 10, 100)
                            spotify.set_volume(current_volume)
                    elif current_gesture == "decrease_volume":
                        if current_volume > 0:
                            current_volume = max(current_volume - 10, 0)
                            spotify.set_volume(current_volume)

            # Display the frame with the hand landmarks and gesture text
            cv2.imshow('Gesture Control', frame)
            # Break the loop if 'q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break

    finally:
        # Clean up resources on exit
        cv2.destroyAllWindows()
        picam2.stop()
        hands.close()

else:
    print("Failed to authenticate with Spotify.")



# Gesture-Controlled Spotify Player

## Table of Contents
- [Description](#description)
- [Features](#features)
- [Project File Structure](#project-file-structure)
- [Prerequisites](#prerequisites)
- [Setting Up Spotify Developer App](#setting-up-spotify-developer-app)
- [Installation](#installation)
- [Usage](#usage)
- [Mediapipe Hand Landmarks](#mediapipe-hand-landmarks)
- [Understanding Gesture Detection Conditions](#understanding-gesture-detection-conditions)
- [Gesture Commands](#gesture-commands)

## Description
This project provides a gesture-controlled interface for Spotify, allowing users to control music playback through hand gestures. It's particularly useful in situations where hands are occupied or dirty, such as in the kitchen, or for users with speech difficulties.

Watch a demonstration of the Gesture-Controlled Spotify Player here:
[Gesture-Controlled Spotify Player Demo](https://github.com/Shallange/S.H.I.G.S/assets/53408265/4797a283-7518-4134-845d-6f33afdbda71)

## Features
- Control Spotify playback using hand gestures.
- Recognize gestures like play, pause, next track, previous track, increase and decrease volume.
- Utilizes Flask for handling Spotify OAuth and MediaPipe for gesture recognition.

## Project File Structure


- **images**
  - [spotify_api.png](/images/spotify_api.png)
  - [hand-landmarks.png](/images/hand-landmarks.png)
  - [play_music.jpg](/images/play_music.jpg)
  - [pause_music.jpg](/images/pause_music.jpg)
  - [next_song.jpg](/images/next_song.jpg)
  - [previous_song.jpg](/images/previous_song.jpg)
  - [increase_volume.jpg](/images/increase_volume.jpg)
  - [decrease_volume.jpg](/images/decrease_volume.jpg)
- [README.md](/README.md)
- [requirements.txt](/requirements.txt)
- **src**
  - [auth_code.txt](/src/auth_code.txt)
  - [auth_server.py](/src/auth_server.py)
  - **gesture_recognition**
    - [detector.py](/src/gesture_recognition/detector.py)
    - [__init__.py](/src/gesture_recognition/__init__.py)
  - [main.py](/src/main.py)
  - [spotify_controller.py](/src/spotify_controller.py)



## Prerequisites
- Raspberry Pi 4 with Raspbian OS "Bookworm"
- Raspberry Pi Camera Module 3
- A running Spotify session
- Spotify Developer account (for API credentials)
- Internet connection
- Python 3 installed on Raspberry Pi

## Key Libraries Used

### MediaPipe
[MediaPipe](https://google.github.io/mediapipe/) is an open-source, cross-platform, customizable machine learning solution for live and streaming media. Developed by Google, it's designed to make on-device machine learning more accessible and easy to implement. In this project, we use MediaPipe for real-time hand tracking and gesture recognition. It provides a robust framework for detecting hand landmarks, enabling the Gesture-Controlled Spotify Player to accurately interpret various hand gestures for controlling music playback.

### OpenCV
[OpenCV (Open Source Computer Vision Library)](https://opencv.org/about/) is an open-source computer vision and machine learning software library. It's designed to provide a common infrastructure for computer vision applications and accelerate the use of machine perception in commercial products. In this project, OpenCV is utilized for image processing and capturing video frames from the Raspberry Pi Camera Module 3. This integration is crucial for detecting hand gestures in real-time.

### Picamera2
[Picamera2](https://www.raspberrypi.org/documentation/accessories/camera.html) is a Python library tailored for Raspberry Pi camera modules, enabling direct access to the camera hardware for capturing high-quality images and video streams. It provides a streamlined interface for efficient video data handling, crucial for applications requiring real-time video processing. In the Gesture-Controlled Spotify Player, picamera2 plays a pivotal role by capturing live video feeds that are essential for gesture recognition. The library's ability to handle real-time video capture with minimal latency is vital for the accurate and responsive interpretation of hand gestures. Its integration ensures that the system can efficiently process video inputs, making it an integral component of the project.


## Setting Up Spotify Developer App

To fully utilize the features of this Gesture-Controlled Spotify Player, you need to create an application on the Spotify Developer website. This is necessary to obtain the `Client ID` and `Client Secret` keys, essential for authenticating and interacting with the Spotify API.

### Steps to Create a Spotify Developer App:

1. Visit the [Spotify Developer Website](https://developer.spotify.com/).
2. Sign in with your Spotify account, or create one if you don't already have it.
3. Navigate to the Dashboard and create a new app.
4. Fill in the details:
   - **App Name:** Choose a name for your application.
   - **App Description:** Provide a brief description.
   - **Website:** (Optional) Your project or personal website.
   - **Redirect URI:** A URI where users can be redirected after authentication success or failure. This should match the URI in your project settings.
5. Agree to Spotify's Developer Terms of Service and Design Guidelines.
6. Once the app is created, you will receive your `Client ID` and `Client Secret`. Keep these confidential.

Remember, these credentials are essential for the authentication process in your Gesture-Controlled Spotify Player project.

- **Spotify API Usage Statistics**
  The following image displays a graph of the Spotify API usage statistics for this project. It shows the number of calls made to various endpoints (play, pause, next, previous, volume) over different dates.

  ![Spotify API Usage Statistics](images/spotify_api.png)


## Installation

1. Ensure the camera is activated in the Raspberry Pi settings. (Bookworm OS typically does this automatically.)
2. Clone the repository:
    ```bash
    git clone https://github.com/Shallange/S.H.I.G.S.git
    ``` 
3. Navigate to the project directory:
    ```bash
    cd S.H.I.G.S
    ```
4. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
     ```
5. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
     ``` 

## Usage
1. Run the main application:
    ```bash
    python src/main.py
     ```
2. Follow the instructions in the terminal to open the provided URL for authentication. **The Flask server will handle the authentication process**.

3. Once authenticated, the camera will start, and you can use hand gestures to control Spotify playback.

## Mediapipe Hand Landmarks
MediaPipe's hand tracking identifies key landmarks on the hand, representing important joints and contours. These landmarks are essential for accurately interpreting hand gestures.

- **Hand Landmarks**
The image below displays the specific landmarks MediaPipe identifies on a hand. Each marked point is crucial for understanding hand movements, enabling the Gesture-Controlled Spotify Player to accurately interpret and respond to gestures.
  ![Hand Landmarks](images/hand-landmarks.png)

## Understanding Gesture Detection Conditions

The gesture detection in this project relies on analyzing the positions of hand landmarks identified by MediaPipe. These landmarks are represented as coordinates in a three-dimensional space, where each coordinate consists of an x, y, and z value. In the code, these coordinates are accessed using indices `[0][1][2]`, corresponding to x, y, and z respectively.

### Coordinate System
- **X-coordinate (`[0]`):** Represents the horizontal position of the landmark on the image frame.
- **Y-coordinate (`[1]`):** Indicates the vertical position of the landmark.
- **Z-coordinate (`[2]`):** Provides the depth information of the landmark relative to the camera.

### Gesture Detection Logic
The gesture detection logic uses these coordinates to determine the relative positions of different landmarks. For example:
- **Thumb Folded:** Identified by comparing the y-coordinate of the thumb tip (`landmarks[4][2]`) with the y-coordinate of its lower joint (`landmarks[3][2]`). If the tip's y-coordinate is greater, it indicates a folded thumb.
- **Palm Orientation:** Determined by comparing the x-coordinates of specific landmarks to determine if the palm is facing up, down, or sideways.

### Conditions for Specific Gestures
- **Play Music Gesture:** Detected when the thumb and all other fingers are folded.
- **Pause Music Gesture:** Identified when the palm's y-coordinate is higher than other landmarks, indicating an open palm facing upwards.
- **Next and Previous Song Gestures:** Detected based on the orientation of the palm and the back of the hand.

This approach allows the system to interpret complex hand gestures in real-time, enabling intuitive control over Spotify playback.

## Gesture Commands

- **Play Music**
  ![Play Music](images/play_music.jpg)

- **Pause Music**
  ![Pause Music](images/pause_music.jpg)

- **Next Song**
  ![Next Song](images/next_song.jpg)

- **Previous Song**
  ![Previous Song](images/previous_song.jpg)

- **Increase Volume**
  ![Increase Volume](images/increase_volume.jpg)

- **Decrease Volume**
  ![Decrease Volume](images/decrease_volume.jpg)






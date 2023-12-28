def detect_gesture(landmarks):
    gesture = None

    if landmarks:
        # Check if thumb and other fingers are folded (for play music)
        thumb_folded = landmarks[4][2] > landmarks[3][2]
        other_fingers_folded = all(landmarks[i][2] > landmarks[i - 3][2] for i in [8, 12, 16, 20])

        # Check if palm is higher than other landmarks (for pause music)
        palm_higher = all(landmarks[0][2] < landmarks[i][2] for i in range(1, 21))

        # Check if palm is horizontal (for previous song)
        palm_horizontal = landmarks[5][1] < landmarks[17][1] and landmarks[9][1] < landmarks[13][1]

        # Check if back of hand is horizontal (for next song)
        back_of_hand_horizontal = landmarks[5][1] > landmarks[17][1] and landmarks[9][1] > landmarks[13][1]
        
        

        # Closed Hand for Play Music
        if thumb_folded and other_fingers_folded and not palm_higher:
            gesture = "play_music"

        # Palm Higher for Pause Music
        elif palm_higher:
            gesture = "pause_music"

        # Open Palm Horizontal (Right Hand) for Previous Song
        elif all(landmarks[i][2] < landmarks[i - 2][2] for i in [8, 12, 16, 20]) and palm_horizontal:
            gesture = "previous_song"

        # Open Hand Showing Back for Next Song
        elif all(landmarks[i][2] < landmarks[i - 2][2] for i in [8, 12, 16, 20]) and back_of_hand_horizontal:
            gesture = "next_song"

        # Decrease Volume: Index finger extended
        elif landmarks[8][2] < landmarks[6][2] and all(landmarks[i][2] > landmarks[i - 2][2] for i in [12, 16, 20]):
            gesture = "decrease_volume"

        # Increase Volume: Index and Middle fingers extended
        elif landmarks[8][2] < landmarks[6][2] and landmarks[12][2] < landmarks[10][2] and all(landmarks[i][2] > landmarks[i - 2][2] for i in [16, 20]):
            gesture = "increase_volume"

    return gesture

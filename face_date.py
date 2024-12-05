import cv2
import time
import pymysql
from deepface import DeepFace

# Database settings
db_settings = {
    "host": "localhost",  # Database host
    "user": "root",       # Database user
    "password": "",       # Database password
    "db": "face_detect",  # Database name
}

# Get current date in the format YYYY_MM_DD
current_date = time.strftime("%Y_%m_%d", time.localtime())
table_name = current_date

# SQL query to create a table for the current date if it doesn't exist
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,  # Unique ID for each entry
    emotion VARCHAR(255),              # Detected emotion
    date DATE,                         # Current date
    time TIME                          # Current time
)
"""

try:
    # Connect to the database and create the table
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()
except Exception as ex:
    print(f"Database error: {ex}")
    conn = None  # Ensure conn is None if the connection fails

# Open the camera for real-time video capture
cap = cv2.VideoCapture(0)

# Check if the camera is accessible
if not cap.isOpened():
    print("Cannot open camera")
    exit()

try:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Cannot receive frame")
            break
        
        # Resize the frame to reduce processing time
        img = cv2.resize(frame, (384, 240))
        try:
            # Analyze the image for emotions
            emotion = DeepFace.analyze(img, actions=['emotion'])
            current_time = time.strftime("%H:%M:%S", time.localtime())  # Get current time

            # Extract the dominant emotion from the analysis result
            dominant_emotion = emotion[0].get('dominant_emotion', 'Unknown')
            print(dominant_emotion, current_date, current_time)

            # Insert the emotion analysis result into the database
            if conn:
                with conn.cursor() as cursor:
                    command = f"INSERT INTO {table_name} (emotion, date, time) VALUES (%s, %s, %s)"
                    cursor.execute(command, (dominant_emotion, current_date, current_time))
                conn.commit()
        except Exception as e:
            # Handle errors from DeepFace analysis
            print(f"DeepFace error: {e}")
        
        # Display the video frame with the camera feed
        cv2.imshow('face', img)
        key = cv2.waitKey(30)  # Wait for a key press for 30ms
        if key == 27:  # Esc key to exit
            break
finally:
    # Close the database connection if it's open
    if conn:
        conn.close()
    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

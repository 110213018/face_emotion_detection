# Real-Time Facial Emotion Detection and Logging System

This project is a real-time facial emotion detection system that utilizes the **DeepFace** library for emotion analysis and stores the results in a MySQL database. It captures video feed from a webcam, detects the dominant emotion, and logs the data (emotion, date, and time) into a database table created specifically for the current day.

## Features

- **Real-Time Emotion Analysis**: Uses `DeepFace` to analyze emotions in video frames.
- **Database Integration**: Logs detected emotions into a MySQL database, with a new table created daily.
- **Customizable Table Schema**: Automatically creates a table for each day to store the results.
- **Simple UI**: Displays the video feed with real-time processing.

## Requirements

### Python Libraries

- OpenCV (`cv2`)
- DeepFace
- PyMySQL

Install the required libraries using pip:

```bash
pip install opencv-python deepface pymysql

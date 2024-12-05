import cv2
import time
import pymysql
from deepface import DeepFace

"""
將表情分析結果匯到當日 table
"""

# database setting
db_settings = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "db": "face_detect",
}

# get current date
current_date = time.strftime("%Y_%m_%d", time.localtime())

table_name = current_date

# create table
create_table_query = f"""
CREATE TABLE IF NOT EXISTS {table_name} (
    id INT AUTO_INCREMENT PRIMARY KEY,
    emotion VARCHAR(255),
    date DATE,
    time TIME
)
"""

try:
    conn = pymysql.connect(**db_settings)
    with conn.cursor() as cursor:
        cursor.execute(create_table_query)
    conn.commit()
except Exception as ex:
    print(ex)
# finally:
#     conn.close()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()
while True:
    ret, frame = cap.read()  # whether get the img and frame sucessfully
    if not ret:
        print("Cannot receive frame")
        break
    img = cv2.resize(frame,(384,240))  # if sucess, frame size change to (384, 240) 
    try:
        emotion = DeepFace.analyze(img, actions=['emotion'])
        current_time = time.strftime("%H:%M:%S", time.localtime())

        print(emotion[0]['dominant_emotion'])  # get the value of dominant_emotion of the first dictionary
        # print(emotion)                       # the probability and dominant_emotion of every emotion
        print("{}".format(current_date))       # current date
        print("{}".format(current_time))       # current time

        with conn.cursor() as cursor:
            command = f"INSERT INTO {table_name} (emotion, date, time) VALUES (%s, %s, %s)"
            cursor.execute(command, (emotion[0]['dominant_emotion'], current_date, current_time))
        conn.commit()
    except:
        pass
    cv2.imshow('face', img) # show detect screen
    key = cv2.waitKey(30)
    print("pressed key:",key)
    if key == 27:  # Esc
        break

# close database's connection
conn.close()

cap.release()
cv2.destroyAllWindows()
import cv2  # 導入 OpenCV 庫
import time  # 導入時間模組
import pymysql  # 導入 pymysql 用於與 MySQL 數據庫進行交互
from deepface import DeepFace  # 導入 DeepFace 用於人臉情緒分析

"""
將表情分析結果匯到 test
"""

# 資料庫設定
db_settings = {
    "host": "localhost",  # 主機地址
    "user": "root",  # 用戶名
    "password": "",  # 密碼（請輸入您的數據庫密碼）
    "db": "face_detect",  # 數據庫名稱
}

# 打開攝像頭
cap = cv2.VideoCapture(0)

# 檢查攝像頭是否成功打開
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# 建立 Connection 物件
conn = pymysql.connect(**db_settings)

while True:
    # 讀取影像幀
    ret, frame = cap.read()

    # 如果無法讀取到影像, 則退出迴圈
    if not ret:
        print("Cannot receive frame")
        break

    # 調整影像大小
    img = cv2.resize(frame, (384, 240))

    try:
        # 分析人臉情緒
        emotion = DeepFace.analyze(img, actions=['emotion'])

        # 獲取當前日期和時間
        current_date = time.strftime("%Y-%m-%d", time.localtime())
        current_time = time.strftime("%H:%M:%S", time.localtime())

        # 輸出情緒、日期和時間
        print(emotion[0]['dominant_emotion'])
        print(emotion[0]['face_confidence']) # 
        print("{}".format(current_date))
        print("{}".format(current_time))

        # 建立 Cursor 物件
        with conn.cursor() as cursor:
            # 新增資料SQL語法
            command = "INSERT INTO test(emotion, face_confidence, date, time) VALUES(%s, %s, %s, %s)"
            # 執行 SQL 語句
            cursor.execute(command, (emotion[0]['dominant_emotion'], emotion[0]['face_confidence'], current_date, current_time))

        # 提交
        conn.commit()
    except:
        pass

    # 檢查鍵盤輸入
    key = cv2.waitKey(30)
    if key == 27:  # 如果按下 Esc 鍵，退出迴圈
        break

# 關閉連接
conn.close()

# 釋放鏡頭資源
cap.release()

# 關閉所有視窗
cv2.destroyAllWindows()

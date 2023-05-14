import cv2
import streamlit as st
import numpy as np
from PIL import Image

# 얼굴 인식을 위한 캐스케이드 분류기 로드
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")


def detect_faces(image):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 얼굴 인식
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

    # 얼굴 영역에 사각형 그리기
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

    return image


st.title("Webcam Face Detection")

# 웹캠 영상을 처리할 이미지 자리 표시자 생성
frame_placeholder = st.empty()

# 웹캠 열기
cap = cv2.VideoCapture(0)

while True:
    # 웹캠에서 프레임 캡처
    ret, frame = cap.read()

    # 얼굴 인식을 위해 프레임 처리
    if ret:
        frame = detect_faces(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = Image.fromarray(frame)

        # 처리된 프레임을 스트림리트 이미지 자리 표시자에 표시
        frame_placeholder.image(frame, use_column_width=True)
    else:
        break

cap.release()

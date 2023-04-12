import numpy as np
import streamlit as st
import cv2
from PIL import Image, ImageEnhance
import numpy
import os

@st.cache_data
def load_image(img):
    im = Image.open(img)
    return im


face_cascade = cv2.CascadeClassifier('frecog/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('frecog/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('frecog/haarcascade_smile.xml')


def detect_faces(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.cvtColor(new_img,1)
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return img, faces


def detect_eyes(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.cvtColor(new_img,1)
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)
    for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    return img


def detect_smiles(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.cvtColor(new_img,1)
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    # Detect Smiles
    smiles = smile_cascade.detectMultiScale(gray, 1.1, 4)
    # Draw rectangle around the Smiles
    for (x, y, w, h) in smiles:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return img


def cartoonize_image(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.cvtColor(new_img,1)
    gray = cv2.cvtColor(new_img, cv2.COLOR_BGR2GRAY)
    # Edges
    gray = cv2.medianBlur(gray, 5)
    edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    #Color
    color = cv2.bilateralFilter(img, 9, 300, 300)
    #Cartoon
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    return cartoon


def cannize_image(our_image):
    new_img = np.array(our_image.convert('RGB'))
    img = cv2.cvtColor(new_img,1)
    img = cv2.GaussianBlur(img, (11, 11), 0)
    canny = cv2.Canny(img, 100, 150)
    return canny

def main():
    st.title('Face Detection App')
    st.text('Build with Streamlit and OpenCV')

    activities = ['Detection', 'About']
    choice = st.sidebar.selectbox('Select Activity', activities)

    if choice == 'Detection':
        st.subheader('Face Detection')

        image_file = st.file_uploader('Upload Image', type=['jpg','png','jpeg'])
        if image_file is not None:
            st.text('Original Image')
            st.image(load_image(image_file))

            enhance_type = st.sidebar.radio('Enhance Type',
                                            ['Original','Gray-Scale','Contrast','Brightness','Blurring'])
            if enhance_type == 'Original':
                st.text('Original Image')
                st.image(load_image(image_file))
            elif enhance_type == 'Gray-Scale':
                st.text('Gray-Scale Image')
                st.image(load_image(image_file).convert('L'))
            elif enhance_type == 'Contrast':
                c_rate = st.sidebar.slider('Contrast', 0.5, 3.5)
                enhancer = ImageEnhance.Contrast(load_image(image_file))
                enhance_image = enhancer.enhance(c_rate)
                st.text('Contrast Changed Image')
                st.image(enhance_image)
            elif enhance_type == 'Brightness':
                c_rate = st.sidebar.slider('Brightness', 0.5, 3.5)
                enhancer = ImageEnhance.Brightness(load_image(image_file))
                enhance_image = enhancer.enhance(c_rate)
                st.text('Brightness Changed Image')
                st.image(enhance_image)
            elif enhance_type == 'Blurring':
                blu_rate = st.sidebar.slider('Blurring', 0.5, 3.5)
                o_image = np.array(load_image(image_file).convert('RGB'))
                blur_image = cv2.GaussianBlur(o_image, (11, 11), blu_rate)
                st.text('Blurring Applied Image')
                st.image(blur_image)


            # Face Detection
            task = ['Faces', 'Smiles', 'Eyes', 'Cannize', 'Cartoonize']
            our_image = load_image(image_file)
            feature_choice = st.sidebar.selectbox("Find Features", task)
            if st.button("Process"):

                if feature_choice == 'Faces':
                    result_img, result_faces = detect_faces(our_image)
                    st.image(result_img)

                    st.success("Found {} faces".format(len(result_faces)))
                elif feature_choice == 'Smiles':
                    result_img = detect_smiles(our_image)
                    st.image(result_img)


                elif feature_choice == 'Eyes':
                    result_img = detect_eyes(our_image)
                    st.image(result_img)

                elif feature_choice == 'Cartoonize':
                    result_img = cartoonize_image(our_image)
                    st.image(result_img)

                elif feature_choice == 'Cannize':
                    result_canny = cannize_image(our_image)
                    st.image(result_canny)

    elif choice == 'About':
        st.subheader('About')




if __name__ == '__main__':
    main()
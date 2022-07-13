import face_recognition
import streamlit as st
import cv2
import pandas as pd
import os
from datetime import datetime

hilang = '''
<style>
#MainMenu {visibility: hidden}
footer {visibility: hidden}
</style>
'''
st.markdown(hilang, unsafe_allow_html=True)




menu = ['Home', 'Absen', 'Data']
pilih = st.sidebar.selectbox('Menu', menu)

if pilih == 'Absen':
    judul = '''
    <h1 style="text-align: center;">Absen</h1>
    '''
    st.markdown(judul, unsafe_allow_html=True)
    
    a = st.checkbox('Kamera')
    if a == True:
        cam = st.camera_input('Pencet Take Picture!')
        if cam:
            with open('unlabel/nama.jpg', 'wb') as f:
                f.write(cam.getbuffer())
                
                
    def absen(nama):
        with open('absensi.csv','r+')as f:
            list = f.readlines()
            list_nama = []
            for line in list:
                entry = line.split('.')
                list_nama.append(entry[0])
            if nama not in list_nama:
                now = datetime.now()
                waktu = now.strftime('%H:%M:%S')
                f.writelines(f'\n {nama};;{waktu}')
                st.success('Absen Selesai!')
    
    def baca(fol):
        img = cv2.imread(fol)
        return img
        
    encode = []
    nama = []
    label = 'label'
    unlabel = 'unlabel'
    
    for file in os.listdir(label):
        img = baca(label +'/'+ file)
        img_encode = face_recognition.face_encodings(img)[0]
        encode.append(img_encode)
        encode.append(file.split('.')[0])
        
    for file in os.listdir(unlabel):
        img = baca(unlabel +'/'+ file)
        img_encode = face_recognition.face_encodings(img)[0]
        
        hasil = face_recognition.compare_faces(encode, img_encode)
        
        for i in range(len(hasil)):
            if results[i]:
                nama = encode[i]
                (top, right, bottom, left) = face_recognition.face_location(img)[0]
                cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(img, nama, (left+2, bottom+20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
                cv2.imshow(img)
                absen(nama)
        
if pilih == 'Data':
    judul = '''
    <h1 style="text-align: center;">Data</h1>
    '''
    st.markdown(judul, unsafe_allow_html=True)
    df = pd.read_csv('absensi.csv')
    st.dataframe(df)
    
if pilih == 'Home':
    judul = '''
    <h1 style="text-align: center;">Home</h1>
    '''
    st.markdown(judul, unsafe_allow_html=True)
    

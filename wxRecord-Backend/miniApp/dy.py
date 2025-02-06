from array import array
import librosa
import librosa.display
import numpy as np
import pandas as pd
import glob
import os, sys
import matplotlib.pyplot as plt
import xlwt
import torch
from keras.models import Sequential
from keras import layers
from keras.layers import Conv1D
from keras.layers import Activation, Dense
from keras.layers import Dropout
from keras.layers import LSTM, MaxPooling1D
from keras.layers.core import Flatten
from tensorflow import keras
from tensorflow.python.keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
import pickle
import pydub

def f_voice(voicefile):
    loaded_model = keras.models.load_model("Emotion_Voice_Detection_Model.h5")

    #loaded_model.summary() 
    airport_pkl = open(r"lb_type.pickle", 'rb') #
    lb = pickle.load(airport_pkl) 
    airport_pkl.close()

    if 'mp3' in voicefile:
        sound = pydub.AudioSegment.from_mp3(voicefile)
        sound.export("sample-000001.wav", format="wav")
        vf = "sample-000001.wav"
    else:
        vf = voicefile
    try:
        X, sample_rate = librosa.load(vf, res_type='kaiser_fast',duration=2.5,sr=22050*2,offset=0.5)
        #X, sample_rate = librosa.load(vf, res_type='kaiser_fast', sr=None,offset=0.5, duration=2.5)
        
        mfccs = np.mean(librosa.feature.mfcc(y=X, sr=np.array(sample_rate), n_mfcc=13),axis=0)
        livedf= pd.DataFrame(data=mfccs)

        #print(livedf)
        livedf = np.expand_dims(livedf.stack().to_frame().T, axis=2)
        #print(livedf)
        livepreds = loaded_model.predict(livedf, batch_size=32, verbose=1)
        #print(livepreds)

        #lb.inverse_transform(livepreds.argmax(axis=1))


        #preds = loaded_model.predict(x_testcnn, batch_size=32, verbose=1)
        # print(preds)
        # 取出概率最高的类别
        live_labels = livepreds.argmax(axis=1)
        # print(pred_labels)

        # 映射回情绪名称

        live_labels = live_labels.astype(int).flatten()
        live_values = (lb.inverse_transform((live_labels)))
        # 真实测试集标签
        #print(live_labels)
        return live_values
    except Exception as e:
        return '分析失败'
    

if __name__ == '__main__':
    vf=input('请输入文件名:')
    #vf = 'voice/wxrec.mp3'
    res = f_voice(vf)    
    if   isinstance(res,str):
        print(res)
    else:
        print(res.tolist())

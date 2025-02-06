from flask import Flask,request
from gevent import pywsgi
#from aip import AipSpeech, AipNlp
import os
import json
from dy import f_voice

app = Flask(__name__)

@app.route('/voice', methods=['GET','POST'])
def main():
    '''后端请求处理接口，将小程序上传的音频保存、转码，并发送到语音识别接口识别文字后，再调用对话情绪识别接口'''
    result = {"status": 0}
    try:
        f = request.files.get('voice')   #对应wx.upload的name属性
        f.save("voice/wxrec.mp3")
        # 保存文件至本地路径，需要提前在py文件的路径下创建个voice文件夹
        #os.system("ffmpeg -y -i voice/xxx.silk -acodec pcm_s16le -f s16le -ac 1 -ar 16000 voice/a.pcm")
        # 文件转码
        #text = get_result()
        # 调用语音识别接口获取识别文字
        #emotion = get_emotion(text)
        # 调用对话情绪识别接口获取判断结果
        result["status"] = 1
        result["result"] = 'OK'

    except Exception as e:
        print(repr(e))
    finally:
        return json.dumps(result)

# def get_result(path='voice/a.pcm'):
#     '''调用百度语音识别接口，返回识别后的文字结果'''
#     # 百度语音识别接口的ID、KEY等信息
#     APP_ID = ''
#     API_KEY = ''
#     SECRET_KEY = ''
#     client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
#     # 读取转码后的文件
#     def get_file_content(filePath):
#         with open(filePath, 'rb') as fp:
#             return fp.read()
#     result = client.asr(get_file_content(path), 'pcm', 16000, {
#         'dev_pid': 1536,
#     })
#     print(result)
#     return result["result"][0]

# def get_emotion(text=""):
#     '''调用百度对话情绪识别接口，返回判断的情绪结果'''
#     # 百度自然语言处理接口的ID、KEY等信息
#     APP_ID = ''
#     API_KEY = ''
#     SECRET_KEY = ''
#     emotion_result = {
#         "text": text
#         }
#     client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
#     options = {
#         "scene": "talk"
#     }
#     try:
#         result = client.emotion(text, options)
#         for each in result["items"]:
#             if each["label"] == "optimistic":
#                 opti = each["prob"]
#             elif each["label"] == "pessimistic":
#                 pess = each["prob"]

#         if opti >= pess:
#             emotion_result["emotion"] = "高兴"
#         else:
#             emotion_result["emotion"] = "悲伤"
#     except Exception as e:
#         print(repr(e))
#     finally:
#         return emotion_result

if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()    
    app.run(debug=True)        
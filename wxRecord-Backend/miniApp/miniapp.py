from flask import Flask,request,Response
from gevent import pywsgi
#from aip import AipSpeech, AipNlp
import os
import json
from dy import f_voice
import random

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def test():
    return "test https"

@app.route('/play',methods=['GET','POST'])
def playvoice():
    if  request.method == "GET":
        content = request.args.get("content")
        if content.lower() == "start":
            voiceName = "导言.mp3"
        else:
            voiceName = "%d.mp3"%(random.randint(1,5))

        with open(voiceName,'rb') as fmp3:
            data =fmp3.read()
        return Response(data,mimetype="audio/mpeg3")


@app.route('/voice', methods=['GET','POST'])
def main():
    '''后端请求处理接口，将小程序上传的音频保存、转码，并发送到语音识别接口识别文字后，再调用对话情绪识别接口'''
    result = {"status": 0}
    fname =request.form.get("name")  #对应wx.upload的name属性
    try:
        f = request.files.get(fname)  
        f.save("voice\%s.mp3"%(fname))
        res = f_voice("voice\%s.mp3"%(fname))
        
        result["status"] = 1 
        if isinstance(res,str):
            result["result"] = res
        else:
            result["result"] = res.tolist()[0]

    except Exception as e:
        print(repr(e))
    finally:
        return json.dumps(result)


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 443), app)
    server.serve_forever()    
    #app.run(debug=True,ssl_context=('/root/server.crt','/root/server.key'))
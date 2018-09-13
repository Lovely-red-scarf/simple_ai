
from flask import Flask,request,render_template,send_file
from geventwebsocket.handler import WebSocketHandler # 这个是socket的请求头/gevenwebsocket是内部封装了http和我可租 我可租 因为socket是一次请求一次响应 websocket是一直连接 并且可以实现互发请求
from gevent.pywsgi import WSGIServer #这个是实现你的WSGI协议的
from geventwebsocket.websocket import WebSocket #这个是实现你的WSGI协议的
import baidu_ai

app = Flask(__name__)

@app.route("/index/<uid>")
def index(uid):
    # print(dir(request))
    user_socket = request.environ.get("wsgi.websocket") # type:WebSocket
    print(user_socket)
    while True:
        msg = user_socket.receive()
        if type(msg) == bytearray:
            with open("123.wav","wb") as f:
                f.write(msg)
            res_q = baidu_ai.audio2text("123.wav") #把这个文件转化为文件
            res_a = baidu_ai.my_nlp(res_q,uid)  #把这个文件的内容进行比较  确定返回什么值
            file_name = baidu_ai.text2audio(res_a)# 把得到的值转化为语音

            user_socket.send(file_name)# 把这个语音转化出去

@app.route("/")
def home_page():
    return render_template("index.html")

@app.route("/get_file/<file_name>")
def get_file(file_name):
    return send_file(file_name)

if __name__ == '__main__':
    http_serv = WSGIServer(("127.0.0.1",9980),app,handler_class=WebSocketHandler)
    http_serv.serve_forever()

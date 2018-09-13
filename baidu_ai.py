
from aip import AipSpeech
from aip import AipNlp
import os
import tuling
import uuid


APP_ID = '11793552'
API_KEY = 'uA6sToQWcvYt2lT6qTW6WFrG'
SECRET_KEY = '5rZ1XGYMV39LQBVT4Y1yLNCsmueVe8RQ'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)

# 读取文件
# filePath = "hoay.wma"

def get_file_content(filePath):
    '''
    转码
    :param filePath:
    :return:
    '''
    os.system(f"ffmpeg -y -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{filePath}.pcm", 'rb') as fp:
        return fp.read()


def audio2text(file_name):
    # 识别本地文件
    liu = get_file_content(file_name)

    res = client.asr(liu, 'pcm', 16000, {
        'dev_pid': 1536,
    })

    if res.get("result"):
        print(res.get("result")[0])
    else:
        print(res)

    q = res.get("result")[0]

    return q


def text2audio(text):
    '''
    文字转化为语音
    :param text:
    :return:
    '''
    result = client.synthesis(text, 'zh', 1, {
        "spd": 4,
        'vol': 7,
        "pit": 8,
        "per": 4
    })

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        uid = uuid.uuid4()
        with open(f"{uid}.mp3", 'wb') as f:  #每一次的请求这个名字都要改
            f.write(result)

        # os.system("audio.mp3")

    return f"{uid}.mp3" #换一个拼接文件存储 然后确保每一个文件的名字不同


def my_nlp(q,uid):
    '''
    字然语音匹配
    :param q:
    :param uid:
    :return:
    '''

    a = "我不知道你在说什么"

    if nlp_client.simnet(q, "你叫什么名字").get("score") >= 0.7:
        a = "我叫笨笨"
        return a

    if nlp_client.simnet(q, "你今年几岁了").get("score") >= 0.7:
        a = "我今年17了"
        return a

    a = tuling.to_tuling(q,uid)
    print(a)
    return a



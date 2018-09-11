
import os
import tuling
from aip import AipSpeech  # 百度语音包
from aip import AipNlp # 自然语言包
""" 你的 APPID AK SK """
APP_ID = '11799980'
API_KEY = '6WIC3XSGPt5lTEnBgbDZy43T'
SECRET_KEY = 'vtck1Sbho2HC5NMGs6Ir2glQmWPjhj8u'

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
nlp_client = AipNlp(APP_ID, API_KEY, SECRET_KEY)  # 处理字然语言


result  = client.synthesis('无所谓是利', 'zh', 1, {
    'vol': 5,
})

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
def dispose(result):
        if not isinstance(result, dict):
            with open('dispose.mp3', 'wb') as f:
                f.write(result)

        return 'dispose.mp3'



def get_file_content(filePath):
    '''
    文件转码
    :param filePath:
    :return:
    '''
    os.system(f"ffmpeg -y -i {filePath}  -acodec pcm_s16le -f s16le -ac 1 -ar 16000 {filePath}.pcm")
    with open(f"{{filePath}}.pcm","rb")as fp:
        return fp.read()



def audio2text(file_name):
    '''
    语言转文字
    :param file_name:
    :return:
    '''
    liu = get_file_content(file_name)  # 调用你的可以转化格式
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
    文字转语音
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
        with open('auido.mp3', 'wb') as f:
            f.write(result)

        # os.system("auido.mp3")

    return 'auido.mp3'




def my_nlp(q,uid):
    '''
    字然语言转化
    :param q:
    :param uid:
    :return:
    '''
    a = "我不知道你在说什么"
    if nlp_client.simnet(q,"你的名字叫什么").get("score") >= 0.7:
        a = "你叫大傻叉"
        return a

    if nlp_client.simnet(q,"你今年几岁").get("score") >=0.7:
        a = "我今年18了"
        return a
    # 也就是你的回答和这个不同就执行下面的，让图灵和你回答
    a = tuling.to_tuling(q,uid)
    print(a)
    return a


import requests
import json

tuling_url = "http://openapi.tuling123.com/openapi/api/v2"
data = {
    # 请求的类型 0 文本 1 图片 2 音频
    "reqType": 0,
    # // 输入信息(必要参数)
    "perception": {
        # 文本信息
        "inputText": {
            # 问题
            "text": "北京未来七天，天气怎么样"
        }
    },
    # 用户必要信息
    "userInfo": {
        # 图灵机器人的apikey
        "apiKey": "8fc493d348704ba4af5413e67e6fc90b",
        # 用户唯一标识
        "userId": "zilong"
    }
}

def to_tuling(q,user_id):
    data["perception"]["inputText"]["text"] = q
    data["userInfo"]["userId"] = user_id
    res = requests.post(tuling_url, json=data)
    res_dic = json.loads(res.content.decode("utf8"))  # type:dict
    res_type = res_dic.get("results")[0].get("resultType")
    result = res_dic.get("results")[0].get("values").get(res_type)

    return result


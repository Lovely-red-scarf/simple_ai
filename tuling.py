import requests
import json
# import yuyin_test
tuling_url = "http://openapi.tuling123.com/openapi/api/v2"
data = {
	"reqType":0,
    "perception": {
        "inputText": {
            "text": "阜阳颍州区市医院附近的高档酒店"
        }
    },

    "userInfo": {
        "apiKey": "c9fd36f40d0f4adba06ba28f79c789a6",
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
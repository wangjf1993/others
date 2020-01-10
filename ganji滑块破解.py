import requests
import ssl
import time
import re
from random import randint

ssl._create_default_https_context = ssl._create_unverified_context

from requests.packages import urllib3
urllib3.disable_warnings()

serialId = "2c2842070ed6876abc55700ba7b56748_1fcff28dc2b94f0c9ec121bd6582e510"
code = "22"
sign = "d6ab53478b365a7ec3e5d3715b5f4d62"
namespace = "ershoufangphp"
target_url="https://sh.58.com/ershoufang/38460765095455x.shtml"


class VerifyCrack(object):
    """
    1.上传图片轨迹数据，successToken,破解完成【需要参数：callback, responseId, sessionId, data, timestr】
    2.sessionID上传验证连接url的固定参数可直接得到
    3.responseId请求图片地址，可得到,还可以得到bgImgUrl验证图片的url【需要参数callback, sessionId】
    4.请求bgImgUrl地址得到，得到验证图片，处理轨迹，生成坐标。处理坐标的加密数据data.
    【目前不确定callback/timestr参数，无法解决坐标加密数据data.只得到了responseId, sessionId】
    callback应该是每天不同
    """
    def __init__(self):
        self.headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Origin": "https://callback.58.com",
            "Referer": "https://callback.58.com/firewall/verifycode?serialId={0}&code={1}&sign={2}&namespace={3}&url={4}".format(serialId, code, sign, namespace, target_url),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "X-Requested-With": "XMLHttpRequest",
        }
        self.timestr = format(int(time.time() * 1000))
        self.callback = "jQuery110103991166285281573{}".format(int(self.timestr)-randint(6, 8))
        self.responseId = None
        self.sessionId = None
        self.data = None
        self.bgImgUrl = None


    def check(self):
        """
        得到successToken,破解完成
        :return:
        """
        url = "https://verifycode.58.com/captcha/checkV3?callback={0}&responseId={1}&sessionId={2}&data={3}&_={4}".format(self.callback, self.responseId, self.sessionId, self.data, self.timestr)
        response = requests.get(url, headers=self.headers)
        print(response.text)

    def get_sessionID(self):
        """
        :return: sessionId
        """
        url = 'https://callback.58.com/firewall/codev2/getsession.do?{}'.format(self.timestr)
        data = {
            "serialId": serialId,
            "code": code,
            "sign": sign,
        }
        response = requests.post(url, headers=self.headers, data=data, verify=False)
        sessionId = response.json()["data"]["sessionId"]
        self.sessionId = sessionId

    def get_verfy(self):
        """
        :return: responseId, bgImgUrl
        """
        if self.sessionId is None:
            self.get_sessionID()
        sessionId = self.get_sessionID()
        url = "https://verifycode.58.com/captcha/getV3?callback={0}&showType=win&sessionId={1}&_={2}".format(self.callback, sessionId, str(int(self.timestr)-randint(6, 8)))
        response = requests.get(url, headers=self.headers, verify=False)
        print(response.text)
        responseId = re.findall('"responseId":"(.+?)",', response.text)[0]
        bgImgUrl = re.findall('"bgImgUrl":"(.+?)"},', response.text)[0]
        self.bgImgUrl = bgImgUrl
        self.responseId = responseId


    def get_img(self):
        """
        :return: 得到验证图片,方便后期处理轨迹得到数据
        """
        if self.bgImgUrl is None:
            self.get_verfy()
        url = 'https://verifycode.58.com' + self.bgImgUrl
        response = requests.get(url, headers=self.headers, verify=False)
        with open('tt.jpg', 'wb') as f:
            f.write(response.content)
            print(response.text)





vc = VerifyCrack()
vc.get_img()





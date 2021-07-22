import requests
import json
import re


class User:
    API = {
        "login": "https://www.processon.com/login",
        "createFlow": "https://www.processon.com/diagraming/new?category=flow",
        "MaxChart": "https://www.processon.com/view/privatefilecount",
        "mvTrash": "https://www.processon.com/folder/batch_operation",
        "clearTrash": "https://www.processon.com/folder/remove_from_trash",
        "doLike": "https://www.processon.com/view/dolike",
        "addLink": "https://www.processon.com/view/addlink"
    }

    def login(self):
        """
        登录
        """
        postData = {
            'login_email': self.login_email,
            'login_password': self.login_password,
            'window': True
        }
        print("用户 %s 开始登录..." % self.login_email)
        result = self.s.post(User.API['login'], data=postData)
        msg = json.loads(result.text)
        if msg['msg'] != "success":
            print("用户:账号【%s】或密码【%s】错误,请检查!!" % (self.login_email, self.login_password))
            exit(-1)
        else:
            print("用户 %s 登录成功" % self.login_email)

    def doLike(self, link):
        """
        点赞
        :param link:
        """
        result = self.s.get(link)
        searchObj = re.search(r'var chartId = "([a-zA-Z0-9]*)"', result.text)
        # 找到图表的ID
        chartId: str = searchObj.group(1)
        # 点赞
        self.s.post(User.API['doLike'], data={'chartId': chartId})

    def __init__(self, login_email, login_password):
        self.s = requests.Session()
        self.login_email = login_email
        self.login_password = login_password
        self.login()


if __name__ == "__main__":
    share_link = input("请输入分享链接:")
    with open("users.json.bak", "r", encoding="utf8") as fp:
        json_data = json.load(fp)
        for user in json_data:
            User(user["username"], user["password"]).doLike(share_link)
    print("点赞完成")

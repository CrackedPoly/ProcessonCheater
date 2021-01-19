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

    def expand(self):
        """
        扩容一次
        """
        # 创建流程图
        result = currentUser.createFlow()
        searchObj = re.search(r'var chartId = "([a-zA-Z0-9]*)"', result.text)
        # 找到图表的ID
        chartId: str = searchObj.group(1)
        # 自己给自己点赞
        self.getSharedLink(chartId)
        for index in range(5):
            self.dolike(chartId)
        # 最大容量
        maxChart = self.getMaxChart()
        print("扩容一次完成,当前最大容量:%d" % maxChart)
        # 删除新建的图表
        currentUser.deleteChart(chartId)

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

    def createFlow(self):
        """
        创建流程图
        """
        return self.s.get(User.API['createFlow'])

    def getSharedLink(self, chartId):
        """
        获得分享后的链接
        """
        result = self.s.post(self.API['addLink'], data={'chartId': chartId})
        # 测试用
        # data = result.json()
        # return data['viewLinkId']

    def dolike(self, chartId):
        """
        点赞
        :param chartId:
        """
        r = self.s.post(User.API['doLike'], data={'chartId': chartId})

    def getMaxChart(self):
        """
        获取最大容量
        """
        result = self.s.get(User.API['MaxChart'])
        resultObj = json.loads(result.text)
        return resultObj['totalcount']

    def deleteChart(self, chartId):
        """
        完全删除指定图表
        """
        postData = {
            "type": "delete",
            "fileIds": chartId,
            "targetFolderId": ""
        }
        # 把创建的空流程图移到回收站
        self.s.post(User.API['mvTrash'], data=postData)
        # 清空回收站
        self.s.post(User.API['clearTrash'], data={'fileType': 'all'})

    def __init__(self, login_email, login_password):
        self.s = requests.Session()
        self.login_email = login_email
        self.login_password = login_password
        self.login()


if __name__ == "__main__":

    # 获取必要信息
    login_email = input("请输入您的账号:")
    login_password = input("请输入您的密码:")

    print("开始初始化...")
    currentUser = User(login_email, login_password)
    # 开始扩容
    print("开始扩容...")
    # 扩容的数目
    times = 100
    for i in range(times):
        currentUser.expand()

pass

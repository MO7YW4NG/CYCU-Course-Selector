import json
class Info():
    def toJson(self):
        return json.dumps({})
class LoginInfo(Info):
    def __init__(self, userNm, userPasswd):
        self.userNm = userNm
        self.userPasswd = userPasswd
    
    def toJson(self):
        return json.dumps({
            "UserNm": self.userNm,
            "UserPasswd": self.userPasswd
        })
class InsertInfo(Info):
    def __init__(self, data):
        self.type = "take_course"
        self.data = data
    def toJson(self):
        return {
            "type": self.type,
            "data": self.data
        }
class AuthData(Info):
    def toJson(self):
        return json.dumps({
            "authUrl":"/myself_api_127",
            "authApi":"/elective/json/ss_loginUser_student.jsp"
        })
class ParamInfo(Info):
    def __init__(self, loginToken, mtd):
        self.loginToken = loginToken
        self.mtd = mtd
    def set_mtd(self, mtd):
        self.mtd = mtd
        return self
    def toJson(self):
        return {
            "loginToken": self.loginToken,
            "method": self.mtd
        }
class RequestInfo(Info):
    def __init__(self, token):
        self.token = token
        self.insertInfo = None
    def insert_info(self, insertInfo: InsertInfo):
        self.insertInfo = insertInfo
        return self
    def toJson(self):
        if self.insertInfo is None:
            return json.dumps({
                "APP_AUTH_token": self.token
            })
        else:
            return json.dumps({
                "APP_AUTH_token": self.token,
                "obj": self.insertInfo.toJson()
            })
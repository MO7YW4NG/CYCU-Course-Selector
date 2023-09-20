from post_request import req, loginReq, Direct
from info import LoginInfo, ParamInfo, RequestInfo, InsertInfo, AuthData
from time import sleep
import os
import getpass

elecAuthData = AuthData()
loginToken = ""
token = ""
cookies = ""
info = LoginInfo("default","default")

def elecAuth():
    global cookies
    res = req(Direct["AUTH"],elecAuthData,None,cookies)
    msg = res.json()
    if "APP_AUTH_token" not in msg:
        global loginToken
        lgReq = req(Direct["LOGIN"],info,None,cookies)
        loginToken = lgReq.json()["loginToken"]
        cookies = lgReq.cookies
        sleep(1)
        return elecAuth()
    global token
    token = msg["APP_AUTH_token"]

def task():
    while(True):
        reqInfo = RequestInfo(token)
        paramInfo = ParamInfo(loginToken,"track_get")
        trackReq = req(Direct["ELEC"],reqInfo,paramInfo,cookies)
        if trackReq.status_code != 200:
            elecAuth()
            continue
        msg = trackReq.json()
        for item in msg["track_get"]:
            insertInfo = InsertInfo([{"DATA_Token":item["DATA_Token"]}])
            insertReq = req(Direct["ELEC"],reqInfo.insert_info(insertInfo),paramInfo.set_mtd("take_course_and_register_insert"),cookies)
            if insertReq.status_code != 200:
                continue
            newMsg = insertReq.json()
            if "distinct_IP_IDCODE_alert" in newMsg:
                req(Direct["ELEC"],reqInfo,paramInfo.method("login_sys_upd"),cookies)
                break
            if "alert_text" in newMsg:
                print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [❎]: " + newMsg["alert_text"])
            else:
                print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [✅]: " + newMsg["alerts"])
    os.system("pause")

if __name__ == '__main__':
    os.system("title 搶課機器人")
    try:
        while(True):
            id = input("輸入您的學號：")
            passwd = getpass.getpass("輸入您的itouch密碼：")
            info = LoginInfo(id,passwd)
            res = loginReq(Direct["LOGIN"],info)
            if res.status_code != 200:
                print("請求傳送失敗!")
                continue
            if res.text == "伺服器執行錯誤(i)":
                print("登入失敗! 請檢查學號及密碼是否正確!")
                continue
            msg = res.json()
            if msg['done_YN'] == "N":
                print("登入失敗! 請檢查學號及密碼是否正確!")
                continue
            print("登入成功! 開始搶課!")
            cookies = res.cookies
            loginToken=msg['loginToken']
            elecAuth()
            sleep(0.1)
            task()
            break
    except Exception as e:
        print(e)
        os.system("pause")

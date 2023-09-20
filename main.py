from post_request import req, loginReq, Direct
from info import LoginInfo, ParamInfo, RequestInfo, InsertInfo, AuthData
from time import sleep
import os
import getpass

elecAuthData = AuthData()

def login(login_info):
    res = loginReq(Direct["LOGIN"], login_info)
    if res.status_code != 200:
        print("請求傳送失敗! 請檢查網路連線!")
        return None, None
    if res.text == "伺服器執行錯誤(i)":
        print("登入失敗! 請檢查學號及密碼是否正確!")
        return None, None
    msg = res.json()
    if msg['done_YN'] == "N":
        print("登入失敗! 請檢查學號及密碼是否正確!")
        return None, None
    return msg['loginToken'], res.cookies

def auth(login_token, login_info, cookies):
    res = req(Direct["AUTH"], elecAuthData, None, cookies)
    msg = res.json()
    if "APP_AUTH_token" not in msg:
        login(login_info)
        sleep(1)
        return auth(login_token, login_info, cookies)
    return msg["APP_AUTH_token"], cookies

def request_course(login_token, auth_token, cookies):
    req_info = RequestInfo(auth_token)
    param_info = ParamInfo(login_token, "track_get")
    track_req = req(Direct["ELEC"], req_info, param_info, cookies)
    if track_req.status_code != 200:
        return track_req.status_code
    msg = track_req.json()
    for item in msg["track_get"]:
        insert_info = InsertInfo([{"DATA_Token": item["DATA_Token"]}])
        insert_req = req(Direct["ELEC"], req_info.insert_info(insert_info), param_info.set_mtd("take_course_and_register_insert"),cookies)
        if insert_req.status_code != 200:
            continue
        new_msg = insert_req.json()
        if "distinct_IP_IDCODE_alert" in new_msg:
            req(Direct["ELEC"], req_info, param_info.method("login_sys_upd"), cookies)
            break
        if "alert_text" in new_msg:
            print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [❎]: " + new_msg["alert_text"])
        else:
            print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [✅]: " + new_msg["alerts"])
    return track_req.status_code

def main():
    os.system("title 搶課機器人")
    try:
        id = input("輸入您的學號：")
        pwd = getpass.getpass("輸入您的itouch密碼：")
        login_info = LoginInfo(id, pwd)
        login_token, cookies = login(login_info)
        if login_token is None:
            return main()
        print("登入成功! 開始搶課!")
        auth_token, cookies = auth(login_token, login_info, cookies)
        sleep(0.1)
        while(True):
            if request_course(login_token, auth_token, cookies) != 200:
                auth_token, cookies = auth(login_token, login_info, cookies)
    except Exception as e:
        print(e)
        os.system("pause")

if __name__ == '__main__':
    main()
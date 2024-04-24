from post_request import req, loginReq, Direct
from info import LoginInfo, ParamInfo, RequestInfo, InsertInfo, AuthData
from time import sleep
import os
import getpass

elecAuthData = AuthData()

def login(login_info: LoginInfo):
    """Student login verify.
    """
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

def auth(login_token: str, login_info: LoginInfo, cookies):
    """Retrieve authentation tokens from backend server. 
    """
    res = req(Direct["AUTH"], elecAuthData, None, cookies)
    msg = res.json()
    if "APP_AUTH_token" not in msg:
        login_token, cookies = login(login_info)
        sleep(1)
        return auth(login_token, login_info, cookies)
    return msg["APP_AUTH_token"], cookies

def track_get(login_token: str, auth_token: str, cookies):
    """Retrieve tracked courses from backend server.
    """
    req_info = RequestInfo(auth_token)
    param_info = ParamInfo(login_token, "track_get")
    track_req = req(Direct["ELEC"], req_info, param_info, cookies)
    if track_req.status_code != 200:
        return track_get(login_token,auth_token,cookies)
    msg = track_req.json()
    return msg

def request_course(login_token: str, auth_token: str, cookies, courses):
    """Sends take course request to backend server.
    """
    req_info = RequestInfo(auth_token)
    param_info = ParamInfo(login_token, "take_course_and_register_insert")
    for item in courses["track_get"]:
        insert_info = InsertInfo({"DATA_Token": item["DATA_Token"]})
        insert_req = req(Direct["ELEC"], req_info.insert_info(insert_info), param_info, cookies)
        if insert_req.status_code != 200:
            return insert_req.status_code
        new_msg = insert_req.json()
        if "distinct_IP_IDCODE_alert" in new_msg:
            req(Direct["ELEC"], req_info, param_info.set_mtd("login_sys_upd"), cookies)
            break
        if "alert_text" in new_msg:
            print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [❎]: " + new_msg["alert_text"])
        else:
            print("[" + item["CURS_CODE"] + "] " + item["CNAME"] + " [✅]: " + new_msg["alerts"])
    return 200

def main():
    """Main function.
    """
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
        courses = track_get(login_token, auth_token, cookies)
        while(True):
            try:
                sleep(0.5)
                if request_course(login_token, auth_token, cookies, courses) != 200:
                    auth_token, cookies = auth(login_token, login_info, cookies)
                    courses = track_get(login_token, auth_token, cookies)
            except Exception as e:
                if "Max retries exceeded" in str(e):
                    for i in range(5):
                        print("到達傳輸上限, 休息一下" + (i*"."))
                        sleep(i)
                else:
                    print(e)
                    pass
    except Exception as e:
        print(e)
        os.system("pause")

if __name__ == '__main__':
    main()
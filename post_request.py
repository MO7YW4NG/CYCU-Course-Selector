import requests
from enum import Enum
from info import Info

class Direct(Enum):
    LOGIN="/auth/myselfLogin"
    AUTH="/baseinfo"
    ELEC="/myself_api_127/elective/mvc/elective_system.jsp"

reqUrl = 'https://myself.cycu.edu.tw'
reqHeaders = {
    'Content-Type': 'application/json',
    'User-Agent': 'CourseSelector/1.0',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}

def req(dir: Direct, reqData: Info, params: Info, cookies):
    if params is None:
        return requests.post(reqUrl+dir.value,data=reqData.toJson(),headers=reqHeaders,cookies=cookies)
    else:
        return requests.post(reqUrl+dir.value,data=reqData.toJson(),headers=reqHeaders,params=params.toJson(),cookies=cookies)
def loginReq(dir: Direct, reqData: Info):
    return requests.post(reqUrl+dir.value,data=reqData.toJson(),headers=reqHeaders)
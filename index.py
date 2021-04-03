import requests,re,os,json

qywx_token = ''

def smzdm(uid):

    re1 = re.compile(r'<a target=.*?href="(.*?)">\s+(.*?)\s+</a>')
    url = f'https://zhiyou.smzdm.com/member/{uid}/baoliao/'
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36 Edg/89.0.774.68'
    }
    r = requests.get(url,headers=headers)
    
    try:
        baoliao = re1.findall(r.text)[0]
        msg = f'{baoliao[1]}\n<a href="{baoliao[0]}">点击查看</a>\n --------------------------------------------\n原文链接：{baoliao[0]}'
    except Exception as e:
        print('获取爆料错误',e)
    print(msg)
    # for i in baoliao:
    #     # print(i)
    #     print(f'内容：\n{i[1]}\n链接：{i[0]}')
    return msg

def msg_qywxapp(qywx_corpid,qywx_corpsecret,qywx_agentid,content):
    global qywx_token
    print('企业微信应用推送')
    if not qywx_token:
        res = requests.get(f'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={qywx_corpid}&corpsecret={qywx_corpsecret}')
        qywx_token = res.json().get('access_token','')
    #print(qywx_token)
    data = {
        'touser':'@all',
        'msgtype':'text',
        'agentid':qywx_agentid,
        'text':{
            'content': content
        }
    }
    r = requests.post(f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={qywx_token}',json=data)
    # print(r.text)
    return r.text

def main(config_json):
    content_list = []
    qywx_corpid = config_json.get('QYWX_CORPID')
    qywx_corpsecret = config_json.get('QYWX_CORPSECRET')
    qywx_agentid = config_json.get('QYWX_AGENTID')
    uid_list = config_json.get('UID_LIST')
    for uid in uid_list:
        msg = smzdm(uid)
        content_list.append(msg)

    for content in content_list:
        msg_qywxapp(qywx_corpid,qywx_corpsecret,qywx_agentid,content)

if __name__ == '__main__':
    data = json.loads(os.getenv("CONFIG_JSON", {}).strip()) if os.getenv("CONFIG_JSON") else {}
    if data:
        main(data)
    else:
        print('参数为空')

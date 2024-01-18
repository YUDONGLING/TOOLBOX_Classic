def Email(Cfg = None):
    pass


def WeChat(Cfg = None):
    pass


def DingTalk(Cfg = None):
    import json
    import time
    import requests

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Org': '',
        'Data' : [],
        'Token': ''
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
    }

    CurrentTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    MdText = '<font color=#6A65FF>**' + Config['Org'] + '**</font> \n\n ' + CurrentTime + ' \n\n'

    for _ in Config['Data']:
        # TITLE
        if _.get('Title', '') == '':
            MdText += ' --- \n\n '
        else:
            Color = _.get('Color', 'UNKNOW').upper()
            if Color.startswith('#') and len(Color) == 7:
                pass
            else:
                match Color:
                    case 'PURPLE':
                        Color = '#6A65FF'
                    case 'RED':
                        Color = '#FF6666'
                    case 'GREEN':
                        Color = '#92D050'
                    case 'BLUE':
                        Color = '#76CCFF'
                    case _:
                        Color = '#76CCFF'
            MdText += ' --- \n\n <font color=' + Color + '>**' + _.get('Title', '') + '**</font> \n\n '
        # TEXT
        MdText += ' \n\n '.join(_.get('Text', [])) + ' \n\n '

    MdText += '<font color=#6A65FF>' + Config['Org'] + '</font>'

    Url = 'https://oapi.dingtalk.com/robot/send?access_token=' + Config['Token']
    Hed = {
        'Content-Type' : 'application/json'
    }
    Dat = {
        'msgtype' : 'markdown',
        'markdown': {
            'title': Config['Org'],
            'text' : MdText
        }
    }

    for Attempt in range(3):
        try:
            Rsp = requests.post(Url, headers = Hed, params = None, data = json.dumps(Dat), cookies = None, proxies = None, timeout = 10)
            Rst = Rsp.json()
            if Rst['errcode'] != 0:
                Response['ErrorCode'] = Rst['errcode']
                Response['ErrorMsg']  = Rst['errmsg']
            break
        except Exception as errorMsg:
            if Attempt == 2:
                Response['ErrorCode'] = 50000
                Response['ErrorMsg']  = f'Fail to send message, {str(errorMsg).lower().rstrip(".")}'
                return Response

    return Response


def Telegram(Cfg = None):
    pass


def ServerChan(Cfg = None):
    pass

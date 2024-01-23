def CreateBrowse(Cfg = None):
    import selenium.webdriver

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Private'      : True,
        'DriverPath'   : r'H:\GITHUB\TOOLBOX\EdgeDriver\msedgedriver.exe',
        'UserDataPath' : r'H:\GITHUB\TOOLBOX\EdgeDriver\UserData',
        'AntiRobotPath': r'H:\GITHUB\TOOLBOX\EdgeStealth.min.js'
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Driver'   : None,
        'Private'  : True
    }

    try:
        option = selenium.webdriver.EdgeOptions()

        if Config['Private']:
            option.add_argument('--inprivate')
            Response['Private'] = True
        else:
            option.add_argument('--user-data-dir=' + Config['UserDataPath'])
            Response['Private'] = False

        option.add_argument('--window-size=800,600')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument('--disable-dev-shm-usage')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-logging'])

        option.add_argument("--disable-blink-features")
        option.add_argument("--disable-blink-features=AutomationControlled")

        service = selenium.webdriver.edge.service.Service(executable_path = Config['DriverPath'])

        Response['Driver'] = selenium.webdriver.Edge(service = service, options = option)

        # with open(r'H:\GITHUB\TOOLBOX\EdgeStealth.min.js') as JS:
        #     C = JS.read()
        #     edgeDriver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        #         'source': C
        #     })
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to create browse, {str(errorMsg).lower().rstrip(".")}'
    return Response


def CloseBrowse(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Driver': None
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : ''
    }

    try:
        Config['Driver'].quit()
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to close browse, {str(errorMsg).lower().rstrip(".")}'
    return Response


def OpenUrl(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Driver' : None,
        'Url'    : '',
        'Ec'     : False,
        'EcTitle': '',
        'Timeout': 10
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode' : 0,
        'ErrorMsg'  : '',
        'Driver'    : None,
        'PageSource': '',
        'Cookies'   : []
    }

    try:
        Config['Driver'].get(Config['Url'])
        if Config['Ec']:
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            WebDriverWait(Config['Driver'], Config['Timeout']).until(EC.title_contains(Config['EcTitle']))
        else:
            import time
            time.sleep(Config['Timeout'])
        Response['Driver']     = Config['Driver']
        Response['PageSource'] = Config['Driver'].page_source
        Response['Cookies']    = Config['Driver'].get_cookies()
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to open url, {str(errorMsg).lower().rstrip(".")}'
    return Response


def OpenBlank(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Driver' : None
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode' : 0,
        'ErrorMsg'  : '',
        'Driver'    : None,
        'PageSource': '',
        'Cookies'   : []
    }

    try:
        Config['Driver'].get('edge://newtab')
        Response['Driver']     = Config['Driver']
        Response['PageSource'] = Config['Driver'].page_source
        Response['Cookies']    = Config['Driver'].get_cookies()
    except Exception as errorMsg:
        Response['ErrorCode'] = 50000
        Response['ErrorMsg']  = f'Fail to open newtab, {str(errorMsg).lower().rstrip(".")}'
    return Response

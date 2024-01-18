def createBrowse(isPrivate = True):
    import selenium.webdriver

    try:
        path         = r'H:\GITHUB\Repository\EdgeDriver\msedgedriver.exe'
        userDataPath = r'H:\GITHUB\Repository\EdgeDriver\UserData'

        option = selenium.webdriver.EdgeOptions()

        if isPrivate:
            option.add_argument('--inprivate')
        if not isPrivate:
            option.add_argument('--user-data-dir=' + userDataPath)
        
        # option.add_argument('start-maximized')
        option.add_argument('--window-size=800,600')
        option.add_argument('--no-sandbox')
        option.add_argument('--disable-gpu')
        option.add_argument('--disable-dev-shm-usage')
        option.add_experimental_option('excludeSwitches', ['enable-automation'])
        option.add_experimental_option('useAutomationExtension', False)
        option.add_experimental_option('excludeSwitches', ['enable-logging'])

        option.add_argument("--disable-blink-features")
        option.add_argument("--disable-blink-features=AutomationControlled")

        service = selenium.webdriver.edge.service.Service(executable_path = path)

        edgeDriver = selenium.webdriver.Edge(service = service, options = option)

        '''
        with open(r'H:\GITHUB\Repository\EdgeStealth.min.js') as JS:
            C = JS.read()
            edgeDriver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': C
            })
        '''

        return (True, ''), edgeDriver
    except Exception as errorMsg:
        return (False, str(errorMsg)), None


def closeBrowse(edgeDriver):
    try:
        edgeDriver.quit()
        return (True, '')
    except Exception as errorMsg:
        return (False, str(errorMsg))


def openUrl(edgeDriver, URL, waitTime = 5):
    import time

    try:
        edgeDriver.get(URL)
        time.sleep(waitTime)
        return (True, ''), edgeDriver.page_source, edgeDriver.get_cookies()
    except Exception as errorMsg:
        return (False, str(errorMsg)), '', []


def openBlank(edgeDriver):
    try:
        edgeDriver.get('edge://newtab')
        return (True, '')
    except Exception as errorMsg:
        return (False, str(errorMsg))


def updateStealthMinJs(edgeDriver):
    try:
        GH = edgeDriver.get('https://github.com/requireCool/stealth.min.js')
        JS = edgeDriver.get('https://raw.githubusercontent.com/requireCool/stealth.min.js/main/stealth.min.js')
        return (True, ''), JS
    except Exception as errorMsg:
        return (False, str(errorMsg)), None


if __name__ == '__main__':
    import time

    T, B = createBrowse()
    print(f'[createBrowse()]: {T, B}')

    time.sleep(5)

    T, S, C = openUrl(B, 'https://bot.sannysoft.com/', waitTime = 5)
    print(f'[openUrl(edgeDriver, URL, waitTime = 5)]: {T, S}')

    time.sleep(5)

    T = openBlank(B)
    print(f'[openBlank(edgeDriver)]: {T}')

    time.sleep(5)

    T = closeBrowse(B)
    print(f'[closeBrowse(edgeDriver)]: {T}')
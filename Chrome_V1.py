import time
import selenium.webdriver


def createBrowse(isPrivate = True):
    try:
        path = r"H:\GITHUB\Repository\ChromeDriver\chromedriver.exe"
        userDataPath = r"H:\GITHUB\Repository\ChromeDriver\UserData"

        option = selenium.webdriver.ChromeOptions()

        if isPrivate:
            option.add_argument("--incognito")
        if not isPrivate:
            option.add_argument("--user-data-dir=" + userDataPath)

        # option.add_argument("start-maximized")
        option.add_argument('--window-size=800,600')
        option.add_argument("--no-sandbox")
        option.add_argument("--disable-gpu")
        option.add_argument("--disable-dev-shm-usage")
        option.add_experimental_option("excludeSwitches", ["enable-automation"])
        option.add_experimental_option("useAutomationExtension", False)
        option.add_experimental_option("excludeSwitches", ["enable-logging"])

        service = selenium.webdriver.chrome.service.Service(executable_path = path)

        chromeDriver = selenium.webdriver.Chrome(service = service, options = option)

        with open(r"H:\GITHUB\Repository\ChromeStealth.min.js") as JS:
            C = JS.read()
            chromeDriver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": C
            })

        return (True, ""), chromeDriver
    except Exception as errorMsg:
        return (False, str(errorMsg)), None


def closeBrowse(chromeDriver):
    try:
        chromeDriver.quit()
        return (True, "")
    except Exception as errorMsg:
        return (False, str(errorMsg))


def openUrl(chromeDriver, URL, waitTime = 5):
    try:
        chromeDriver.get(URL)
        time.sleep(waitTime)
        return (True, ""), chromeDriver.page_source, chromeDriver.get_cookies()
    except Exception as errorMsg:
        return (False, str(errorMsg)), "", []


def openBlank(chromeDriver):
    try:
        chromeDriver.get("chrome://newtab")
        return (True, "")
    except Exception as errorMsg:
        return (False, str(errorMsg))


def updateStealthMinJs(chromeDriver):
    try:
        GH = chromeDriver.get("https://github.com/requireCool/stealth.min.js")
        JS = chromeDriver.get("https://raw.githubusercontent.com/requireCool/stealth.min.js/main/stealth.min.js")
        return (True, ""), JS
    except Exception as errorMsg:
        return (False, str(errorMsg)), None


if __name__ == "__main__":
    T, B = createBrowse()
    print(f"[createBrowse()]: {T, B}")

    time.sleep(5)

    T, S, C = openUrl(B, "https://bot.sannysoft.com/", waitTime = 5)
    print(f"[openUrl(chromeDriver, URL, waitTime = 5)]: {T, S}")

    time.sleep(5)

    T = openBlank(B)
    print(f"[openBlank(chromeDriver)]: {T}")

    time.sleep(5)

    T = closeBrowse(B)
    print(f"[closeBrowse(chromeDriver)]: {T}")
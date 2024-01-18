import os
import time
import requests


from DownloadKit import DownloadKit


def headURL(URL, customHeader = None, customParams = None, customCookie = None, allowRedirects = True):
    headInfo = {"statusCode": -1, "locationURL": "", "contentType": "", "contentLength": -1, "cookie": {}}

    requestHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Dnt": "1",
    }
    requestHeader.update(customHeader or {})
    # requestParams = {}
    # requestParams.update(customParams or {})
    # requestCookie = {}
    # requestCookie.update(customCookie or {})

    try:
        HEAD = requests.get(URL, headers = requestHeader, allow_redirects = allowRedirects, stream = True)
        # HEAD = requests.head(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects)
    except Exception as errorMsg:
        return (False, str(errorMsg)), headInfo

    headInfo.update({
        "statusCode": HEAD.status_code,
        "locationURL": HEAD.url,
        "contentType": HEAD.headers.get("Content-Type", ""),
        "contentLength": int(HEAD.headers.get("Content-Length", "-1")),
        "cookie": dict(HEAD.cookies)
    })
    return (True, ""), headInfo


def getFile(URL, fileFolder, fileName, customHeader = None, customParams = None, customCookie = None, customModifiedTime = None, allowRedirects = True, showDLing = False, showDLNotice = ("", "")):
    getInfo = {"URL": URL, "fileFolder": "", "fileName": "", "fileSize": -1, "responseData": {"statusCode": -1, "locationURL": "", "contentType": "", "contentLength": -1, "cookie": {}}}

    fileFolder = fileFolder.strip() if fileFolder.strip() != "" else "."
    fileName = fileName.strip()
    filePath = os.path.join(fileFolder, fileName)

    try:
        os.makedirs(fileFolder, exist_ok = True); getInfo["fileFolder"] = fileFolder
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    requestHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Dnt": "1",
    }
    requestHeader.update(customHeader or {})
    # requestParams = {}
    # requestParams.update(customParams or {})
    # requestCookie = {}
    # requestCookie.update(customCookie or {})

    try:
        GET = requests.get(URL, headers = requestHeader, allow_redirects = allowRedirects)
        # GET = requests.get(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects)
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    getInfo["responseData"].update({
        "statusCode": GET.status_code,
        "locationURL": GET.url,
        "contentType": GET.headers.get("Content-Type", ""),
        "contentLength": int(GET.headers.get("Content-Length", "-1")),
        "cookie": dict(GET.cookies)
    })

    if 200 <= GET.status_code < 300 and (getInfo["responseData"]["contentLength"] > 1024 or getInfo["responseData"]["contentLength"] == -1):
        try:
            with open(filePath, "wb") as F:
                F.write(GET.content)
        except Exception as errorMsg:
            return (False, str(errorMsg)), getInfo
        GET.close()
        getInfo.update({"fileName": fileName, "fileSize": os.path.getsize(filePath)})
    else:
        GET.close()
        return (False, f"response status_code is {getInfo['responseData']['statusCode']}, content_length is {getInfo['responseData']['contentLength']}"), getInfo

    if not customModifiedTime is None:
        try:
            os.utime(filePath, (customModifiedTime, customModifiedTime))
        except:
            pass
    elif "Last-Modified" in GET.headers:
        try:
            serverModifiedTime = int(time.mktime(time.strptime(GET.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")))
            os.utime(filePath, (serverModifiedTime, serverModifiedTime))
        except:
            pass

    return (True, ""), getInfo


def getFileByStream(URL, fileFolder, fileName, customHeader = None, customParams = None, customCookie = None, customModifiedTime = None, allowRedirects = True, showDLing = False, showDLNotice = ("", "")):
    getInfo = {"URL": URL, "fileFolder": "", "fileName": "", "fileSize": -1, "responseData": {"statusCode": -1, "locationURL": "", "contentType": "", "contentLength": -1, "cookie": {}}}

    fileFolder = fileFolder.strip() if fileFolder.strip() != "" else "."
    fileName = fileName.strip()
    filePath = os.path.join(fileFolder, fileName)

    try:
        os.makedirs(fileFolder, exist_ok = True); getInfo["fileFolder"] = fileFolder
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    requestHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Dnt": "1",
    }
    requestHeader.update(customHeader or {})
    # requestParams = {}
    # requestParams.update(customParams or {})
    # requestCookie = {}
    # requestCookie.update(customCookie or {})

    try:
        GET = requests.get(URL, headers = requestHeader, allow_redirects = allowRedirects)
        # GET = requests.get(URL, headers = requestHeader, params = requestParams, cookies = requestCookie, allow_redirects = allowRedirects)
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    getInfo["responseData"].update({
        "statusCode": GET.status_code,
        "locationURL": GET.url,
        "contentType": GET.headers.get("Content-Type", ""),
        "contentLength": int(GET.headers.get("Content-Length", "-1")),
        "cookie": dict(GET.cookies)
    })

    if 200 <= GET.status_code < 300 and (getInfo["responseData"]["contentLength"] > 1024 or getInfo["responseData"]["contentLength"] == -1):
        try:
            with open(filePath, "wb") as F:
                for C in GET.iter_content(chunk_size = 4192): F.write(C) if C else None
        except Exception as errorMsg:
            return (False, str(errorMsg)), getInfo
        GET.close()
        getInfo.update({"fileName": fileName, "fileSize": os.path.getsize(filePath)})
    else:
        GET.close()
        return (False, f"response status_code is {getInfo['responseData']['statusCode']}, content_length is {getInfo['responseData']['contentLength']}"), getInfo

    if not customModifiedTime is None:
        try:
            os.utime(filePath, (customModifiedTime, customModifiedTime))
        except:
            pass
    elif "Last-Modified" in GET.headers:
        try:
            serverModifiedTime = int(time.mktime(time.strptime(GET.headers["Last-Modified"], "%a, %d %b %Y %H:%M:%S %Z")))
            os.utime(filePath, (serverModifiedTime, serverModifiedTime))
        except:
            pass

    return (True, ""), getInfo


def getFileByDownloadKit(URL, fileFolder, fileName, customHeader = None, customParams = None, customCookie = None, customModifiedTime = None, allowRedirects = True, showDLing = False, showDLNotice = ("", "")):
    getInfo = {"URL": URL, "fileFolder": "", "fileName": "", "fileSize": -1, "responseData": {"statusCode": -1, "locationURL": "", "contentType": "", "contentLength": -1, "cookie": {}}}

    fileFolder = fileFolder.strip() if fileFolder.strip() != "" else "."
    fileName = fileName.strip()
    filePath = os.path.join(fileFolder, fileName)

    try:
        os.makedirs(fileFolder, exist_ok = True); getInfo["fileFolder"] = fileFolder
    except Exception as errorMsg:
        return (False, str(errorMsg)), getInfo

    requestHeader = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", 
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Dnt": "1",
    }
    requestHeader.update(customHeader or {})
    # requestParams = {}
    # requestParams.update(customParams or {})
    # requestCookie = {}
    # requestCookie.update(customCookie or {})

    try:
        DLer = DownloadKit()
        DLer.timeout = 15
        DLer.block_size = "16M"

        DLtask = DLer.add(URL, fileFolder, fileName, file_exists = "overwrite", split = True, headers = requestHeader, allow_redirects = True)

        Tcount = 0

        if showDLing:
            print(f"\r{showDLNotice[0]}0.00 %{showDLNotice[1]}", end = "")

            while DLtask.rate == None or DLtask.rate == 0.0:
                if Tcount >= 50:
                    if DLtask.rate == None or DLtask.rate == 0.0:
                        DLtask.cancel()
                        return (False, "Connect Time (12.5 Second) Out! "), getInfo
                Tcount += 1
                time.sleep(0.25)
            
            while True:
                print(f"\r{showDLNotice[0]}{DLtask.rate} %{showDLNotice[1]}", end = "")
                if DLtask.is_done:
                    break
                else:
                    time.sleep(0.025)
        else:
            DLtask.wait(show = False)            

        if not DLtask.result == "success":
            DLer = None
            return (False, str(DLtask.info)), getInfo
        else:
            DLer = None
            getInfo.update({"fileName": fileName, "fileSize": os.path.getsize(filePath)})
    except Exception as errorMsg:
        try:
            DLer = None
        except:
            pass
        return (False, str(errorMsg)), getInfo

    if not customModifiedTime is None:
        try:
            os.utime(filePath, (customModifiedTime, customModifiedTime))
        except:
            pass

    return (True, ""), getInfo


if __name__ == "__main_1_":
    print(f"[headFile(URL, ***)]: {headURL('http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2')}")

    print(f"[getFile(URL, ***)]: {getFile('http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2', '', 'TEST')}")
    os.remove("TEST")

    print(f"[getFileByStream(URL, ***)]: {getFileByStream('http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2', '', 'TEST')}")
    os.remove("TEST")

#   print(f"[getFileByDownloadKit(URL, ***)]: {getFileByDownloadKit('http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2', '', 'TEST.BIN')}")
#   os.remove("TEST")

    STATE, INFO = getFileByDownloadKit("http://dl.hdslb.com/mobile/fixed/bili_win/bili_win-install.exe?v=1.9.2", "", "TEST.BIN", showDLing = True, showDLNotice = ("     下载进度前测试文字     ", "     下载进度后测试文字     "))
    print(f"")
    print(f"[getFileByDownloadKit(URL, ***)]: ", end = "")
    print(f"{STATE}, {INFO}")
    os.remove("TEST.BIN")
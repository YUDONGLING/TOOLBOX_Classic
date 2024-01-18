import os
import time


def readLog(logFolder, logName):
    logFolder = logFolder.strip() if logFolder.strip() != "" else "."
    logName = logName.strip()
    logPath = os.path.join(logFolder, logName)
    try:
        with open(logPath, "r", encoding = "utf-8") as F:
            return (True, ""), [L.rstrip("\n") for L in F.readlines()]
    except Exception as errorMsg:
        return (False, str(errorMsg)), []


def writeLog(writeData):
    dateYYMMDD = time.strftime("%Y-%m-%d", time.localtime())
    timeHHMMSS = time.strftime("%H:%M:%S", time.localtime())
    logPath = os.path.join("Log", f"{dateYYMMDD}.txt")
    try:
        os.makedirs("Log", exist_ok = True)
        with open(logPath, "a", encoding = "utf-8") as F:
            F.write(f">>>>> {dateYYMMDD} {timeHHMMSS}\n>>>>> {writeData}\n\n")
        return (True, "")
    except Exception as errorMsg:
        return (False, str(errorMsg))


if __name__ == '__main__':
    # readData = "readDataSample"
    # print(f"[readLog(readData)]: {readLog(readData)}")

    writeData = "writeDataSample"
    print(f"[writeLog(writeData)]: {writeLog(writeData)}")
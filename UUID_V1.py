import re
import uuid


def getUuid1Name():
    try:
        return (True, ""), f"uuid_{str(uuid.uuid1()).lower().replace('-', '_')}"
    except Exception as errorMsg:
        return (False, str(errorMsg)), ""


def getUuid4Name():
    try:
        return (True, ""), f"uuid_{str(uuid.uuid4()).lower().replace('-', '_')}"
    except Exception as errorMsg:
        return (False, str(errorMsg)), ""


def getSafeName(originName):
    try:
        safeName = re.sub(r"[\\/:*?\"<>|]", " ", originName)
        safeName = re.sub(r"\s+", " ", safeName).strip()[:50]
        return (True, ""), safeName
    except Exception as errorMsg:
        return (False, str(errorMsg)), ""


if __name__ == "__main__":
    print(f"[getUuid1Name()]: {getUuid1Name()}")
    print(f"[getUuid4Name()]: {getUuid4Name()}")

    originName = "\\AAA\\bbb*BBB*bbb      \"      CCC'|||ddd \n\n\t\t     "
    print(f"[getSafeName(originName)]: {getSafeName(originName)}")
def getUuid1Name():
    import uuid
    try:
        return (True, ''), f'uuid_{str(uuid.uuid1()).lower().replace("-", "_")}'
    except Exception as errorMsg:
        return (False, str(errorMsg)), ''


def getUuid4Name():
    import uuid
    try:
        return (True, ''), f'uuid_{str(uuid.uuid4()).lower().replace("-", "_")}'
    except Exception as errorMsg:
        return (False, str(errorMsg)), ''


def getSafeName(originName):
    import re
    try:
        safeName = re.sub(r'[\\/:*?\"<>|]', ' ', originName)
        safeName = re.sub(r'\s+', ' ', safeName).strip()[:50].strip()
        return (True, ''), safeName
    except Exception as errorMsg:
        return (False, str(errorMsg)), ''


if __name__ == '__main__':
    print(f'[getUuid1Name()]: {getUuid1Name()}')
    print(f'[getUuid4Name()]: {getUuid4Name()}')

    originName = '\\AAA\\bbb*BBB*bbb      \"      CCC"|||ddd \n\n\t\t     '
    print(f'[getSafeName(originName)]: {getSafeName(originName)}')
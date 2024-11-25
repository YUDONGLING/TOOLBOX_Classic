def __CtyunExecute__(AK: str, SK: str, Endpoint: str, Method: str, Params: dict, Data: dict, Headers: dict, Timeout: int):
    import hmac
    import json
    import uuid
    import base64
    import hashlib
    import datetime
    import requests

    def HmacSha(Key, String):
        Key, String = bytearray(Key), bytearray(String)
        return hmac.new(Key, String, digestmod = hashlib.sha256).digest()

    def HmacBase64(Key, String):
        return base64.b64encode(HmacSha(Key, String)).decode()

    def SortedParams(Parmas):
        return '&'.join(['%s=%s' % (Key, Value) for Key, Value in sorted(Parmas.items())])

    def SignedHeader(Params, Data):
        Eop_DATE = datetime.datetime.strftime(datetime.datetime.now(), '%Y%m%dT%H%M%SZ')
        Eop_YYMD = Eop_DATE[:8]
        Eop_UUID = str(uuid.uuid4())

        K_Time    = HmacSha(SK.encode(), Eop_DATE.encode())
        K_AK      = HmacSha(K_Time, AK.encode())
        K_Date    = HmacSha(K_AK, Eop_YYMD.encode())
        Signature = HmacBase64(K_Date, ('ctyun-eop-request-id:%s\neop-date:%s\n\n%s\n%s' % (Eop_UUID, Eop_DATE, SortedParams(Params), hashlib.sha256((json.dumps(Data) if Data else '').encode()).hexdigest())).encode())

        return {
            'Ctyun-Eop-Request-Id': Eop_UUID,
            'Eop-Date'            : Eop_DATE,
            'Eop-Authorization'   : '%s Headers=ctyun-eop-request-id;eop-date Signature=%s' % (AK, Signature)
        }

    Hed = SignedHeader(Params, Data)
    Hed.update(Headers)

    if Method == 'GET':
        Res = requests.get(Endpoint, params = Params, headers = Hed, timeout = Timeout)
    else:
        if Data: Res = requests.post(Endpoint, json = Data, headers = Hed, timeout = Timeout)
        else:    Res = requests.post(Endpoint, data = Data, headers = Hed, timeout = Timeout)

    return Res.json()


def __CtyunApiGet__(AK: str, SK: str, Endpoint: str, Params: dict = {}, Data: dict = {}, Headers: dict = {}, Timeout: int = None): return __CtyunExecute__(AK, SK, Endpoint, 'GET', Params, Data, Headers, Timeout)


def __CtyunApiPost__(AK: str, SK: str, Endpoint: str, Params: dict = {}, Data: dict = {}, Headers: dict = {}, Timeout: int = None): return __CtyunExecute__(AK, SK, Endpoint, 'POST', Params, Data, Headers, Timeout)


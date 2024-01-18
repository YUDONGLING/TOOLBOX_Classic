def ReadConfig() -> dict:
    import os
    import json

    try:
        if os.path.exists('ExeConfig.json'):
            with open('ExeConfig.json', 'r') as File:
                return json.loads(File.read())
        else:
            raise Exception('config file does not exist')
    except Exception as errorMsg:
        return {'_Err': f'Fail to read config, {str(errorMsg).lower().rstrip(".")}'}


def WriteConfig(Cfg = None, Force = False) -> dict:
    import os
    import json

    try:
        if os.path.exists('ExeConfig.json') and not Force:
            raise Exception('config file already exists, add Force = True to overwrite')
        else:
            with open('ExeConfig.json', 'w') as File:
                File.write(json.dumps(Cfg if Cfg else {}, indent = 4, ensure_ascii = False))
            with open('ExeConfig.json', 'r') as File:
                return json.loads(File.read())
    except Exception as errorMsg:
        return {'_Err': f'Fail to write config, {str(errorMsg).lower().rstrip(".")}'}


def DecryptEnvironVar() -> dict:
    import os
    import json

    def __Decrypt__(Data, Fernet):
        if isinstance(Data, str):
            Data = Fernet.decrypt(Data.encode()).decode()
        elif isinstance(Data, list):
            Data = [__Decrypt__(_, Fernet) for _ in Data]
        elif isinstance(Data, dict):
            for Key, Value in Data.items():
                if Key in ['AesKey', 'Type']: continue
                Data[Key] = __Decrypt__(Value, Fernet)
        return Data

    try:
        if os.path.exists('EnvironVariable.json'):
            with open('EnvironVariable.json', 'r') as File:
                _ = json.loads(File.read()); Flag = True
        elif os.path.exists('EnvironVariable_AES.json'):
            with open('EnvironVariable_AES.json', 'r') as File:
                _ = json.loads(File.read()); Flag = False
        else:
            raise Exception('environ variable file does not exist')

        if Flag:
            return _
        else:
            from cryptography.fernet import Fernet
            return __Decrypt__(_, Fernet(os.environ.get('AES_KEY', '').encode()))
    except Exception as errorMsg:
        return {'_Err': f'Fail to decrypt environ variable, {str(errorMsg).lower().rstrip(".")}'}


def EncryptEnvironVar(Var = None, Force = False) -> dict:
    import os
    import json

    def __Encrypt__(Data, Fernet):
        if isinstance(Data, str):
            Data = Fernet.encrypt(Data.encode()).decode()
        elif isinstance(Data, list):
            Data = [__Encrypt__(_, Fernet) for _ in Data]
        elif isinstance(Data, dict):
            for Key, Value in Data.items():
                if Key in ['AesKey', 'Type']: continue
                Data[Key] = __Encrypt__(Value, Fernet)
        return Data

    try:
        if Var is not None:
            if os.path.exists('EnvironVariable.json') and not Force:
                raise Exception('environ variable file already exists, add Force = True to overwrite')
            else:
                _ = Var; Flag = False
        else:
            if os.path.exists('EnvironVariable_AES.json'):
                with open('EnvironVariable_AES.json', 'r') as File:
                    _ = json.loads(File.read()); Flag = True
            elif os.path.exists('EnvironVariable.json'):
                with open('EnvironVariable.json', 'r') as File:
                    _ = json.loads(File.read()); Flag = False
            else:
                raise Exception('environ variable file does not exist')

        if Flag:
            return _
        else:
            from cryptography.fernet import Fernet

            if _.get('AesKey', None) is None:
                AesKey = Fernet.generate_key()
                with open('EnvironVariable.json', 'w') as File:
                    _['AesKey'] = AesKey.decode()
                    File.write(json.dumps(_, indent = 4, ensure_ascii = False))
            else:
                AesKey = _.get('AesKey').encode()

            _ = __Encrypt__(_, Fernet(AesKey))
            with open('EnvironVariable_AES.json', 'w') as File:
                _['AesKey'] = 'AES_KEY'
                File.write(json.dumps(_, indent = 4, ensure_ascii = False))

            return _
    except Exception as errorMsg:
        return {'_Err': f'Fail to encrypt environ variable, {str(errorMsg).lower().rstrip(".")}'}

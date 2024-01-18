def AddTextToImage(Cfg = None):
    import os

    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Text'      : '',
        'Folder'    : '',
        'File'      : '',
        'Font'      : '',
        'Size'      : 0.0375,
        'Color'     : (255, 255, 255),
        'Background': (0, 0, 0, 128)
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Folder'   : '',
        'File'     : '',
        'Path'     : '',
        'Size'     : -1
    }

    Folder = Config['Folder'] if Config['Folder'] != '' else '.'
    File   = Config['File']
    Path   = os.path.join(Folder, File)

    try:
        IMG = Image.open(Path).convert('RGBA')
        DRW = ImageDraw.Draw(IMG)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50001
        Response['ErrorMsg']  = f'Fail to open given image, {str(errorMsg).lower().rstrip(".")}'
        return Response

    try:
        if 1 < Config['Size'] < IMG.height:
            Size = int(Config['Size'])
        else:
            Size = int(Config['Size'] * IMG.height)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50002
        Response['ErrorMsg']  = f'Fail to set given font size, {str(errorMsg).lower().rstrip(".")}'
        return Response

    try:
        Font = ImageFont.truetype(Config['Font'], Size) if Config['Font'] != '' else ImageFont.load_default(Size)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50003
        Response['ErrorMsg']  = f'Fail to set given font, {str(errorMsg).lower().rstrip(".")}'
        return Response

    try:
        Box   = DRW.textbbox((0, 0), f' {Config["Text"]} ', font = Font)
        Box_W = Box[2] - Box[0]
        Box_H = Box[3] - Box[1]

        TXT = Image.new('RGBA', IMG.size, (0, 0, 0, 0))
        DRW = ImageDraw.Draw(TXT)
        DRW.rectangle([0, IMG.height - Box_H - IMG.height * 0.025, Box_W, IMG.height - IMG.height * 0.0125], fill = Config['Background'])
        DRW.text((0, IMG.height - Box_H - IMG.height * 0.025), f' {Config["Text"]} ', font = Font, fill = Config['Color'])

        IMG = Image.alpha_composite(IMG, TXT)
        IMG = IMG.convert('RGB')
        IMG.save(Path)

        Response['Folder'] = Folder
        Response['File']   = File
        Response['Path']   = Path
        Response['Size']   = os.path.getsize(Path)
    except Exception as errorMsg:
        Response['ErrorCode'] = 50004
        Response['ErrorMsg']  = f'Fail to add text to given image, {str(errorMsg).lower().rstrip(".")}'
        return Response

    return Response


def GetMediaInfo(Cfg = None):
    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Folder'  : '',
        'File'    : '',
        'Url'     : '',
        'Header'  : {
            'Accept'    : '*/*',
            'Range'     : 'bytes=0-',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.41'
            },
        'Params'  : {},
        'Cookie'  : None,
        'Timeout' : 10,
        'Redirect': True,
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Folder'   : '',
        'File'     : '',
        'Path'     : '',
        'Height'   : -1,
        'Width'    : -1,
        'Size'     : -1
    }

    # Local File
    if Config['File'] != '':
        import os, cv2

        Folder = Config['Folder'] if Config['Folder'] != '' else '.'
        File   = Config['File']
        Path   = os.path.join(Folder, File)

        try:
            _ = cv2.VideoCapture(Path)
            Response['Height'] = int(_.get(cv2.CAP_PROP_FRAME_HEIGHT))
            Response['Width']  = int(_.get(cv2.CAP_PROP_FRAME_WIDTH))
            _.release()
            Response['Folder'] = Folder
            Response['File']   = File
            Response['Path']   = Path
            Response['Size']   = os.path.getsize(Path)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Fail to get local media info, {str(errorMsg).lower().rstrip(".")}'
            return Response

    else:
        import cv2

        if __name__ == '__main__':
            from  Download import HeadFile
        else:
            from .Download import HeadFile

        Info = HeadFile({
            'Url'     : Config['Url'],
            'Header'  : Config['Header'],
            'Params'  : Config['Params'],
            'Cookie'  : Config['Cookie'],
            'Timeout' : Config['Timeout'],
            'Redirect': Config['Redirect']
        })
        Response['Folder'] = Info['FinalUrl']
        Response['File']   = Info['FinalUrl']
        Response['Path']   = Info['FinalUrl']
        Response['Size']   = Info['ContentLength']

        try:
            _ = cv2.VideoCapture(Info['FinalUrl'])
            Response['Height'] = int(_.get(cv2.CAP_PROP_FRAME_HEIGHT))
            Response['Width']  = int(_.get(cv2.CAP_PROP_FRAME_WIDTH))
            _.release()
        except Exception as errorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Fail to get online media info, {str(errorMsg).lower().rstrip(".")}'
            return Response

    return Response


def GetMediaThumbnail(Cfg = None):
    import os

    if __name__ == '__main__':
        from  Merge import MergeCfg
    else:
        from .Merge import MergeCfg

    Config = {
        'Folder'     : '',
        'File'       : '',
        'ThumbFolder': '',
        'ThumbFile'  : '',
        'Size'       : (400, 300),
        'Quality'    : 25
    }
    Config = MergeCfg(Config, Cfg)

    Response = {
        'ErrorCode': 0,
        'ErrorMsg' : '',
        'Folder'   : '',
        'File'     : '',
        'Path'     : '',
        'Size'     : -1
    }

    Pillow_Support  = ['.BLP', '.BMP', '.DDS', '.DIB', '.EPS', '.GIF', '.ICO', '.IM', '.JPG', '.JPEG', '.JFIF', '.J2K', '.J2P', '.JPX', '.MSP', '.PCX', '.PNG', '.APNG', '.PPM', '.SPIDER', '.TGA', '.TIFF', '.TIF', '.WEBP', '.XBM', '.CUR', '.DCX', '.FITS', '.FLI', '.FLC', '.FPX', '.FTEX', '.GBR', '.GD', '.IMT', '.IPTC', '.NAA', '.MCIDAS', '.MIC', '.MPO', '.PCD', '.PIXAR', '.PSD', '.SUN', '.WAL', '.EMF', '.XPM']
    Cv2_Support     = ['.3G2', '.3GP', '.ASF', '.ASX', '.AVI', '.DIVX', '.FLV', '.M2TS', '.M2V', '.M4V', '.MKV', '.MOV', '.MP4', '.MPEG', '.MPG', '.MTS', '.MXF', '.OGV', '.RM', '.SWF', '.WEBM', '.WMV']
    PyMuPDF_Support = ['.PDF']
    # Word_Support    = ['.DOC', '.DOCX', '.DOCM', '.DOT', '.DOTX', '.DOTM']
    # Excel_Support   = ['.XLS', '.XLSX', '.XLAM', '.XLSM', '.XLSB', '.XLT', '.XLTS', '.XLTM', '.CSV']
    # Ppt_Support     = ['.PPTX', '.PPTM', '.PPT', '.POTX', '.POTM', '.POT', '.PPSX', '.PPSM', '.PPSI']

    Folder = Config['Folder'] if Config['Folder'] != '' else '.'
    File   = Config['File']
    Path   = os.path.join(Folder, File)
    Ext    = os.path.splitext(File)[-1].upper()

    ThumbFolder = Config['ThumbFolder'] if Config['ThumbFolder'] != '' else '.'
    ThumbFile   = Config['ThumbFile']
    ThumbPath   = os.path.join(ThumbFolder, ThumbFile)


    def __Thumb_Pillow__(Path1, Path2, Size, Quality, Response):
        try:
            import os

            from PIL import Image

            Image  = Image.open(Path1).convert('RGB')
            Ratio1 = float(Image.width) / float(Image.height)
            Ratio2 = float(Size[0]) / float(Size[1])

            if Ratio1 > Ratio2:
                _      = int(Image.height * Ratio2)
                Margin = (Image.width - _) // 2
                Image  = Image.crop((Margin, 0, Margin + _, Image.height))
            else: 
                _      = int(Image.width / Ratio2)
                Margin = (Image.height - _) // 2
                Image  = Image.crop((0, Margin, Image.width, Margin + _))

            Image.thumbnail((min(Size[0], Image.width), min(Size[1], Image.height)))
            Image.save(Path2, quality = Quality, format = 'JPEG')

            Response['Path'] = Path2
            Response['Size'] = os.path.getsize(Path2)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50001
            Response['ErrorMsg']  = f'Fail to generate thumbnail, {str(errorMsg).lower().rstrip(".")}'
        return Response


    def __Thumb_Cv2__(Path1, Path2, Size, Quality, Response):
        try:
            import cv2

            Video    = cv2.VideoCapture(Path1)
            Position = int(min(Video.get(cv2.CAP_PROP_FRAME_COUNT) / Video.get(cv2.CAP_PROP_FPS) * 1000, 0.05 * 1000))
            Video.set(cv2.CAP_PROP_POS_MSEC, Position)
            _, Frame = Video.read(); cv2.imwrite(Path2 + '.OpenCV_Temp.jpeg', Frame)
            Video.release()

            return __Thumb_Pillow__(Path2 + '.OpenCV_Temp.jpeg', Path2, Size, Quality, Response)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50002
            Response['ErrorMsg']  = f'Fail to generate thumbnail, {str(errorMsg).lower().rstrip(".")}'
        return Response


    def __Thumb_PyMuPDF__(Path1, Path2, Size, Quality, Response):
        try:
            import fitz

            from PIL import Image

            Pdf = fitz.open(Path1)
            Img = Pdf[0].get_pixmap()
            Img = Image.frombytes('RGB', [Img.width, Img.height], Img.samples)
            Img.save(Path2 + '.PyMuPDF_Temp.jpeg', format = 'JPEG')
            Pdf.close()

            return __Thumb_Pillow__(Path2 + '.PyMuPDF_Temp.jpeg', Path2, Size, Quality, Response)
        except Exception as errorMsg:
            Response['ErrorCode'] = 50003
            Response['ErrorMsg']  = f'Fail to generate thumbnail, {str(errorMsg).lower().rstrip(".")}'
        return Response


    if Ext in Pillow_Support:
        Response['Folder'] = ThumbFolder
        Response['File']   = ThumbFile
        os.makedirs(ThumbFolder, exist_ok = True)
        return __Thumb_Pillow__(Path, ThumbPath, Config['Size'], Config['Quality'], Response)
    elif Ext in Cv2_Support:
        Response['Folder'] = ThumbFolder
        Response['File']   = ThumbFile
        os.makedirs(ThumbFolder, exist_ok = True)
        return __Thumb_Cv2__(Path, ThumbPath, Config['Size'], Config['Quality'], Response)
    elif Ext in PyMuPDF_Support:
        Response['Folder'] = ThumbFolder
        Response['File']   = ThumbFile
        os.makedirs(ThumbFolder, exist_ok = True)
        return __Thumb_PyMuPDF__(Path, ThumbPath, Config['Size'], Config['Quality'], Response)
    # elif Ext in Word_Support:
    #     pass
    # elif Ext in Excel_Support:
    #     pass
    # elif Ext in Ppt_Support:
    #     pass

    Response['ErrorCode'] = 50004
    Response['ErrorMsg']  = f'Fail to generate thumbnail for unsupported file type'
    return Response

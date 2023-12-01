import requests
import json
import pandas as pd
from PIL import Image
from io import BytesIO


def collectImage( url ):
    return Image.open(
        BytesIO(requests.get(url).content))\
        .convert('RGB')

def callAPI(page = 1, ratio = '16x9', resolution='1920x1080'):

    wallpaperAPI = 'https://wallhaven.cc/api/v1/search?'
    qResolution = f'resolution={resolution}'
    qRatio = f'ratios={ratio}'

    r = requests.get( wallpaperAPI + qRatio + f'&page={page}')
    apiResults = pd.DataFrame(json.loads(r.content)['data'])
    return apiResults
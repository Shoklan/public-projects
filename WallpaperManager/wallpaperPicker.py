###########################################################################################
#   Author: Collin Mitchell
#     Date: 2023 October 10th
#  Version: 1.0
#     Info: Program designed to use a Deep Learning model to filter and select wallpapers
#           This is the second part which does the pulling + filtering.
#  History: 
#           [2023/10/10]
#           Initial Launch.
###########################################################################################

import os
import datetime
from pathlib import Path
import uuid
import secrets
from dotenv import load_dotenv
from helpers import collectImage, callAPI

from fastcore.all import *
from fastai.vision.all import *     # This is for the CNN learner.


# Load the local path information
load_dotenv()

dataPath = Path(os.getenv('WALLPAPER_PATH'))
deselectedPath = Path(os.getenv('DESELECTED_PATH'))
storagePath = Path(os.getenv('STORAGE_PATH'))
modelName = os.getenv('CURRENT_MODEL')


nLearn = load_learner(dataPath/f'model/{modelName}')
page = secrets.randbelow(500)
print('Loaded model...')
print(f'Calling API for results for page {page}...')

apiResults = callAPI(page=page)
for i,r in apiResults.iterrows():
    try:
        img = collectImage(r.path)
        img.save(str(storagePath/r.id) + '.' + r.file_type.split('/')[-1])
    except Exception as e:
        print(e)
        continue


for file in storagePath.glob("*[jpeg|png]"):
    prediction = nLearn.predict(file)[0].strip()
    if prediction == 'YES':
        newName = datetime.now().strftime('%Y%m%d') + "_" + str(uuid.uuid1()).split('-')[0]
        print(file, newName, Path(dataPath, 'Desktop', newName))
        file.replace(Path(dataPath, 'Desktop', newName))

for file in storagePath.glob("*[jpeg|png]"):
    file.unlink()
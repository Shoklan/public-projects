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
print('Loaded model...')
print('Calling API for results...')
apiResults = callAPI(page=7)
for i,r in apiResults.iterrows():
    img = collectImage(r.path)
    img.save(str(dataPath/r.id) + '.' + r.file_type.split('/')[-1])


for file in storagePath.glob("*[jpeg|png]"):
    prediction = nLearn.predict(file)[0].strip()
    if prediction == 'YES':
        newName = datetime.now().strftime('%Y%m%d') + "_" + str(uuid.uuid1()).split('-')[0]
        print(file, newName, Path(dataPath, 'Desktop', newName))
        file.replace(Path(dataPath, 'Desktop', newName))

for file in storagePath.glob("*[jpeg|png]"):
    file.unlink()
###########################################################################################
#   Author: Collin Mitchell
#     Date: 2023 October 10th
#  Version: 1.0
#     Info: Program designed to use a Deep Learning model to filter and select wallpapers.
#           This is the part that is used to build/update the model
#  History: 
#           [2023/10/10]
#           Initial Launch.
#     TODO: 
#           Manage Model drift; picked wallpapers will influence future wallpaper choices.
###########################################################################################

import os
import sys
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

from fastcore.all import *
from fastai.vision.all import *     # This is for the CNN learner.

# Load the local path information
load_dotenv()

# Pathing structure reference
dataPath = Path(os.getenv('WALLPAPER_PATH'))
deselectedPath = Path(os.getenv('DESELECTED_PATH'))
storagePath = Path(os.getenv('STORAGE_PATH'))

# Setup versions
template = pd.DataFrame(columns=['fname', 'label'])

# labels will be the final; downloaded is filled out by me.
labels = template.copy()
downloaded = template.copy()
removed = template.copy()

if not Path(dataPath/'model/downloaded.csv').exists():
    downloadedFiles = sorted(
        [ '/'.join(f.parts[-3:]) for f in storagePath.iterdir() ],
        key = lambda x: x.split('/')[-1])
    downloaded['fname'] = downloadedFiles
    downloaded.to_csv(dataPath/'model/downloaded.csv', index=False)

    sys.exit("Created the Downloads file to fill out for the model.")
filledOut = pd.read_csv(dataPath/'model/downloaded.csv')


# Fix mismatch between files ordering; python vs OS
targetFiles = sorted(
    list((dataPath/'Desktop').glob('*.png')) + 
    list((dataPath/'Desktop').glob('*.jpg')))
targetFiles = list(map( lambda x: 'Desktop/'+ x.parts[-1], targetFiles))

labels['fname'] = targetFiles
labels['label'] = 'YES'

# Remove wallpapers I don't care about anymore
removedFiles = sorted(
    [ '/'.join(f.parts[-3:]) for f in deselectedPath.iterdir() ],
    key = lambda x: x.split('/')[-1])
removed['fname'] = removedFiles
removed['label'] = 'NO'

selections = pd.concat([labels, filledOut, removed])

# Build the model:
print('Started Training the Model...')
dls = ImageDataLoaders.from_df(selections, dataPath, item_tfms=Resize((1080//4, 1920//4)))
learn = vision_learner(dls, resnet34, metrics=error_rate);
learn.fine_tune(12, .0006)

# modelName = 'model-1.0'
modelName = 'testing'
modelPath = dataPath/f'model/{modelName}'
learn.export(modelPath)
print(f'Model has been saved: {modelPath} ')
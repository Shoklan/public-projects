###########################################################################################
#   Author: Collin Mitchell
#     Date: 2023 October 10th
#  Version: 1.0
#     Info: Program designed to use a Deep Learning model to filter and select wallpapers.
#           This is the part that is used to pull the images.
#  History: 
#           [2023/10/10]
#           Initial Launch.
###########################################################################################


import os
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from helpers import collectImage, callAPI

# Load the local path information
load_dotenv()

# Pathing structure reference
dataPath = Path(os.getenv('WALLPAPER_PATH'))
deselectedPath = Path(os.getenv('DESELECTED_PATH'))
storagePath = Path(os.getenv('STORAGE_PATH'))

if not deselectedPath.exists(): deselectedPath.mkdir()
if not storagePath.exists(): storagePath.mkdir()

imgs = []
frames = []
count = 1

print('Starting Image Collection...')
while len(imgs) < 100:
    try:
        tmp = callAPI(page=count)
    except Exception as e:
        print(f'There were issues connecting to the API: {e.message}')
        import time
        time.sleep(10) 
        continue

    frames += [tmp]
    collection = [ collectImage( url ) for _, url in tmp.path.items() ]
    imgs = imgs + collection
    count += 1
    print(f'Iteration {count-1} completed... {len(imgs)} collected so far.')

# Join all the collected image data as a dataframe
df = pd.concat(frames).reset_index(drop=True)

# ... and download them locally for use.
for i,r in df.iterrows():
    imgs[i].save(
        str(storagePath) + '/' + str(i).zfill(4) + '.' + r.file_type.split('/')[-1]
    )
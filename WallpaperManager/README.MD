# Deep Learning Picks My Wallpapers

This project has an associated blog post which can be found [here](https://orgulo.us/posts/nbks/2023-08-24-using-deep-learning-to-pick-my-wallpapers.html#dealing-with-the-wallhaven-api) which discusses the overall intent of the project.
If you would like to run this yourself from the beginning, then the order of running the programs is:
1. Wallpaper Puller.
2. Wallpaper Modeler.
3. Wallpaper Picker.

Make sure that you setup the Environmental Variables:
    * `WALLPAPER_PATH` is the parent directory where the program does the work.
    * `DESELECTED_PATH` is the folder where you are storing wallpaper rejects for future modeling.
    * `STORAGE_PATH` is the folder where temporary files are downloaded and managed.

If you are running this after a model has been built then you can simply run the **Wallpaper Picker** program and it will pull a new collection.
Please keep in mind that you will want a directory called `Desktop` in your `WALLPAPER_PATH` folder as this is a a hard coded expectation. If you would like to change this - or update it with a new Environmental variable - then this is referenced in `wallpaperPicker.py` line 46.

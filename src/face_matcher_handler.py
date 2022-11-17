'''
The ideia of this program is consume the images in the folder "image_bus" and match it with the database
'''

import datetime
import glob
import os
import cv2
from presence_manager import FaceMatcher
from env import SERVICE_BUS_BATCH_SIZE


def main():
    search_dir = "src/image_bus/"
    # remove anything from the list that is not a file (directories, symlinks)
    # thanks to J.F. Sebastion for pointing out that the requirement was a list 
    # of files (presumably not including directories)  
    files = list(filter(os.path.isfile, glob.glob(search_dir + "*.jpeg")))
    files.sort(key=lambda x: os.path.getmtime(x))
    print("Time: ",datetime.datetime.fromtimestamp(os.path.getmtime(files[0])))
    fm = FaceMatcher()
    name = fm.find_in_db(cv2.imread(files[0]))
    print(name)

if __name__ == "__main__":
    main()
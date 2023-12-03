import warnings
warnings.filterwarnings("ignore")

import cv2
import numpy as np
from tensorflow.python.keras.layers import Input, Dense
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.models import load_model
import pandas as pd
import numpy as np
from PIL import Image,ImageOps
import segmentor as segmentor
import matplotlib.pyplot as plt
import os
import shutil
# 'segmented' directory contains each mathematical symbol in the image
root = os.getcwd()
if 'segmented' in os.listdir():
    shutil.rmtree('segmented')
os.mkdir('segmented')
SEGMENTED_OUTPUT_DIR = os.path.join(root, 'segmented')
# trained model
MODEL_PATH = os.path.join(root, 'model_save_final_lenet5_same_padding_maxpooling.h5')
# csv file that maps numerical code to the character
mapping_processed = os.path.join(root, 'mapper.csv')

def img2emnist(filepath):
    img = Image.open(filepath).resize((32, 32))
    inv_img = ImageOps.invert(img)
    flatten = np.array(inv_img).flatten() / 255
    flatten = np.where(flatten > 0.5, 1, 0)
    return flatten

def ordered_filenames():
    max_a = max_b = max_c = 0
    files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
    for file in files:
        splits = file.split('_')
        a = int(splits[0])
        b = int(splits[1])
        c = int(splits[2].split('.')[0])
        max_a = max(max_a, a)
        max_b = max(max_b, b)
        max_c = max(max_c, c)
    sorted_files = []
    for i in range(max_a):
        for j in range(max_b):
            for k in range(max_c):
                a = i+1
                b = j+1
                c = k+1
                filename  = str(a) + '_' + str(b) + '_' + str(c) + '.jpg'
                if filename in files:
                    sorted_files.append(filename)
    return sorted_files, max_a
        
def processor(INPUT_IMAGE):
    img = Image.open(INPUT_IMAGE)
    # segmennting each character in the image
    segmentor.image_segmentation(INPUT_IMAGE)
    segmented_images = []
    files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
    # writing images to the 'segmented' directory
    for file in files:
        file_path = os.path.join(SEGMENTED_OUTPUT_DIR , file)
        segmented_images.append(Image.open(file_path))

    files = sorted(list(os.walk(SEGMENTED_OUTPUT_DIR))[0][2])
    for file in files:
        filename = os.path.join(SEGMENTED_OUTPUT_DIR, file)
        img = cv2.imread(filename, 0)

        kernel = np.ones((2,2), np.uint8)
        dilation = cv2.erode(img, kernel, iterations = 1)
        cv2.imwrite(filename, dilation)



    model = load_model(MODEL_PATH)
    df = pd.read_csv(mapping_processed)
    code2char = {}
    for index, row in df.iterrows():
        code2char[row['id']] = row['char']
    results = ''
    files, lines = ordered_filenames()
    for line in range(lines):
        if results != '':
            results += ','
        string = ''
        line_no = line+1
        line_no = str(line_no)
        files_in_same_line = [ file for file in files if file.startswith(line_no) ]
        for file in files_in_same_line:
            file_path = os.path.join(SEGMENTED_OUTPUT_DIR, file)
            array = img2emnist(file_path)
            X_data = pd.DataFrame(array).values.reshape(-1,32,32,1)
            X_data = X_data.astype(float)
            result_predicted = model.predict(X_data)
            result_predicted = np.argmax(result_predicted, axis = 1)
            for r in result_predicted:
                string += code2char[r]
        results += string
            
    return results


def main(operationBytes):
    Image.open(operationBytes).save('input.png')
    equation = processor('input.png')
    print('\nEquation :', equation)
    return equation

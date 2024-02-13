import cv2
from pdf2image import convert_from_path
import numpy as np
import pandas as pd

def ecg2csv():
    #cargar imagenes de un path (esto sio si devuelve un array aun que sea 1), (CARGA SOLO LA DERIVADA QUE DESEAS (NO CARGES EL ECG COMPLETO),  NECESITAS HACER ROI ANTES)
    #this is if u want to convert a pdf to images (its good if u have a pdf and u want to zoom it and then convert it to images, so u can have a better resolution of the image, so u can have a better result of the ecg line detection.)
    # images = convert_from_path('/Users/desarrollo/Desktop/xd2.pdf') 
    # image = np.array(images[0])

    #this is if u want to load an image (if u have already ROI'ed image with good resolution and quality, use this)
    image = cv2.imread('/Users/desarrollo/Desktop/derivative.png')


    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply median filter to remove noise if needed.
    denoised = cv2.medianBlur(gray, 5)

    # Apply morphological opening to remove small black regions <-- this is if when u apply roi and u have others waves that are in other line derivations. (this happens when waves are too close to each other, so the roi is not enough to remove them, so u need to apply this to remove them, but this can remove the ecg line too, so u need to test it first. be careful with this.)
    # kernel = np.ones((5,5),np.uint8)
    # opening = cv2.morphologyEx(denoised, cv2.MORPH_OPEN, kernel)

    # Threshold the image to binary using Otsu's method
    _, binary = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Find the y-coordinate of the ECG line for each x-coordinate
    # by finding the first white pixel in each column
    ecg_line = np.argmax(binary, axis=0)

    # Invert the y-coordinates
    ecg_line = binary.shape[0] - ecg_line

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(ecg_line, columns=['ECG_Value'])
    df.to_csv('/Users/desarrollo/Desktop/csvderivate.csv', index=False) #change this to ur path

    return 'Done'

ecg2csv()
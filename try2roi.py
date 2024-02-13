import numpy as np
import cv2
from pdf2image import convert_from_path
import fitz


def roiimg():
    doc = fitz.open('/Users/desarrollo/Desktop/ecg.pdf')
    page = doc[0]
    #i use big zoom to get a better resolution of the image, so i can have a better result of the ecg line detection.
    zoom_x = 8.0
    zoom_y = 8.0
    mat = fitz.Matrix(zoom_x, zoom_y)
    pix = page.get_pixmap(matrix=mat)
    # Convert the pixmap to a numpy array
    image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

    print('Image shape:', image.shape)

    # Define the ROI
    roi_position = (492, 1520)
    roi_size = (2680, 520)


    
    # Crop the image to the ROI
    cropped_image = image[roi_position[1]:roi_position[1]+roi_size[1], roi_position[0]:roi_position[0]+roi_size[0]]
    # Draw a rectangle around the ROI
    image_with_roi = cv2.rectangle(image.copy(), roi_position, (roi_position[0]+roi_size[0], roi_position[1]+roi_size[1]), (0, 255, 0), 2)

    #START OF THE CODE TO GET THE X AND Y POSITION OF THE ROI <- YOU DONT NEED THIS, I MADE THIS TO GET THE X AND Y POSITION OF THE ROI EASIER, COMMENT AFTER GET UR POSITIONS
    cv2.namedWindow('Image with ROI')
    # i made this cuz its easier to get the x and y position where u want to define the roi
    cv2.setMouseCallback('Image with ROI', print_click_position)

    # Display the image with the ROI
    cv2.imshow('Image with ROI', cv2.cvtColor(image_with_roi, cv2.COLOR_RGB2BGR))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #END OF THE CODE TO GET THE X AND Y POSITION OF THE ROI <- YOU DONT NEED THIS, I MADE THIS TO GET THE X AND Y POSITION OF THE ROI EASIER, COMMENT AFTER GET UR POSITIONS


    # Save the cropped image using OpenCV
    cv2.imwrite('/Users/desarrollo/Desktop/derivative.png', cv2.cvtColor(cropped_image, cv2.COLOR_RGB2BGR))

    return

def print_click_position(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f'You clicked at ({x}, {y})')

roiimg()
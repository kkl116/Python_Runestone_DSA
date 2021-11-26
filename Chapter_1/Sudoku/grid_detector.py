import cv2
import glob
import numpy as np 
import matplotlib.pyplot as plt
from skimage.segmentation import clear_border

def auto_canny(image, sigma=0.33):
    v = np.median(image)
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))
    edged = cv2.Canny(image, lower, upper)
    return edged

def puzzle_parser(img_path, target_shape=(48,48), return_cells=True):
    #target_shape = (input_shape[0], input_shape[1])
    img = cv2.imread(img_path)
    #color information does not matter in this case so grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blur to remove noise a little bit - 5x5 kernel might be too strong 3x3 is good
    sharpen_kernel = np.array([[0,-1,-0], [-1, 5,-1], [0,-1,0]])
    sharpen = cv2.filter2D(gray, -1, sharpen_kernel)
    edges = auto_canny(sharpen)
    #blur for noise removal
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_area = 0
    max_idx = 0
    for idx,c in enumerate(contours):
        area = cv2.contourArea(c)
        if area > max_area:
            max_area = area
            max_idx = idx

    #get boundary points from edges 
    ext_contour = contours[max_idx].squeeze()
    ymin = np.min(ext_contour[:, 0])
    ymax = np.max(ext_contour[:, 0])
    xmin = np.min(ext_contour[:, 1])
    xmax = np.max(ext_contour[:, 1])
    #split img map in to grids 
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cropped = thresh[xmin:xmax, ymin:ymax]
    if return_cells:
        rows = np.array_split(cropped, 9, axis=0)
        cells = []
        for row in rows:
            row_split = np.array_split(row, 9, axis=1)
            for cell in row_split:
                cell = clear_border(cell)
                cell = cv2.resize(cell, target_shape)
                cells.append(cell)
                
        assert len(cells) == 81
        return cells
    else:
        return cv2.cvtColor(img[xmin:xmax, ymin:ymax], cv2.COLOR_BGR2RGB)







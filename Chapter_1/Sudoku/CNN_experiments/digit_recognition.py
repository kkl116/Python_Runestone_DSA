"""script to load model for digit recognition"""

import numpy as np 
from tensorflow import keras 

def predict(cells):
    """takes list of images and predicts their numeral value"""
    #load model 
    model = keras.models.load_model('tmnist_model')
    #change cells into desired shape 
    cells = [np.expand_dims(np.expand_dims(c, -1), 0) for c in cells]
    cells = np.concatenate(cells, axis=0)
    cells = cells.astype('float32') / 255
        
    res = model.predict(cells)
    digits = np.argmax(res, axis=1)
    digits = np.reshape(digits, (9, 9))
    return digits

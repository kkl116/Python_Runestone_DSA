""" script to train mnist model using keras -- meant for training a quick model so default params used """
import numpy as np
import cv2
import glob
import tensorflow
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.losses import CategoricalCrossentropy
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from keras import backend as K 
from sklearn.model_selection import train_test_split
import pandas
from blur_pool_keras.blurpool import MaxBlurPooling2D

num_classes = 10
input_shape = (48, 48, 1)
target_shape = (input_shape[0], input_shape[1])

def reshape_images(data):
    resized = []
    for im in data:
        resized.append(np.expand_dims(cv2.resize(im, target_shape), 0))
    return np.concatenate(resized, axis=0)

def load_mnist():
    #get data from keras 
    print('loading and processing mnist...')
    (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

    #change all zero images to blank 
    # for i in range(len(x_train)):
    #     if y_train[i] == 0:
    #         x_train[i] = x_train[i] * 0

    # for i in range(len(x_test)):
    #     if y_test[i] == 0:
    #         x_test[i] = x_test[i] * 0

    #reshape mnist to target size 
    x_train = reshape_images(x_train)
    x_test = reshape_images(x_test)

    #normalize pixel range
    x_train = x_train.astype('float32') / 255
    x_test = x_test.astype('float32') / 255

    x_train = np.expand_dims(x_train, -1)
    x_test = np.expand_dims(x_test, -1)

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    return (x_train, y_train), (x_test, y_test)

def load_tmnist():
    print('loading and processing tmnist...')
    csv_path = 'TMNIST_Data.csv'
    df = pandas.read_csv(csv_path)
    y = list(df['labels'])
    data = df[[str(i) for i in range(1, 28**2+1)]]
    x = []
    for r in range(len(data)):
        row = np.array(list(data.iloc[r]))
        img = np.reshape(row, (28, 28)).astype(np.uint8)
        if y[r] == 0:
            img = img * 0
        img = cv2.resize(img, target_shape)
        img = np.expand_dims(img, 0)
        x.append(img)
    x = np.concatenate(x, axis=0).astype('float32') / 255
    x = np.expand_dims(x, -1)
    y = keras.utils.to_categorical(y, num_classes)
    assert len(x) == len(y)
    #split into train and test 
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.1)
    return (train_x, train_y), (test_x, test_y)

def load_chars74k():
    print('loading and processing chars74k')
    dirs = sorted(glob.glob('Chars74K/Fnt/*'))[:10]
    x = []
    y = []
    for i in range(len(dirs)):
        paths = glob.glob(dirs[i] + '/*')
        for p in paths:
            if i == 0:
                img = np.zeros(target_shape)
                x.append(img)
                y.append(0)
            else:
                img = cv2.imread(p, 0)
                img = cv2.bitwise_not(img)
                img = cv2.resize(img, target_shape)
                x.append(img)
                y.append(i)
    x = [np.expand_dims(img, 0) for img in x]
    x = np.concatenate(x, axis=0).astype('float32') / 255
    x = np.expand_dims(x, -1)
    y = keras.utils.to_categorical(y, num_classes)
    assert len(x) == len(y)
    train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.1)
    return (train_x, train_y), (test_x, test_y)


#define model - 
#use swish activation function instead of relu?
def load_model(model_path=None):
    def swish(x):
        return(x * K.sigmoid(x))

    model = keras.Sequential(
        [
            keras.Input(shape=input_shape),
            layers.Conv2D(32, kernel_size=(3,3), activation=swish, padding='same'),
            layers.MaxPooling2D(),
            layers.Conv2D(64, kernel_size=(3,3), activation=swish, padding='same'),
            layers.MaxPooling2D(),
            layers.Flatten(),
            layers.Dense(64, activation=swish),
            layers.Dropout(0.5),
            layers.Dense(32, activation=swish),
            layers.Dropout(0.5),
            layers.Dense(num_classes, activation='softmax')
        ]
    )

    if model_path is not None:
        model.load_weights()
    return model

#actual training of model
def train(model, train_data, test_data, out_path=None):
    x_train, y_train = train_data
    x_test, y_test = test_data 

    batch_size = 64
    epochs = 10
    lr = 1e-3
    smoothing = 0.1

    model.compile(loss=CategoricalCrossentropy(label_smoothing=smoothing), 
    optimizer=Adam(learning_rate=lr), 
    metrics=["accuracy"])

    def scheduler(epoch, lr):
        if epoch < 10:
            return lr
        else:
            return lr/10
    callback = tensorflow.keras.callbacks.LearningRateScheduler(scheduler)
    print('training...')

    model.fit(x_train, y_train, 
        validation_split=0.1,
        batch_size=batch_size,
        epochs=epochs,
        callbacks=[callback],
        verbose=1)

    score = model.evaluate(x_test, y_test, verbose = 0)
    print("Test loss: ", score[0])
    print("Test accuracy: ", score[1])
    
    if out_path:
        model.save(out_path)

if __name__ == "__main__":
    import argparse
    import sys 
    parser = argparse.ArgumentParser(description='Train model using different datasets.')
    parser.add_argument('-d', '--dataset', type=str, help='options: [mnist, tmnist]', required=True)

    args = parser.parse_args()
    if args.dataset == 'mnist':
        train_data, test_data = load_mnist()
    elif args.dataset == 'tmnist':
        train_data, test_data = load_tmnist()
    elif args.dataset == 'tmnist_chars74k':
        chars74_train, chars74_test = load_chars74k()
        tmnist_train, tmnist_test = load_tmnist()
        train_data = (np.concatenate([chars74_train[0], tmnist_train[0]]), np.concatenate([chars74_train[1], tmnist_train[1]]))
        test_data = (np.concatenate([chars74_test[0], tmnist_test[0]]), np.concatenate([chars74_test[1], tmnist_test[1]]))
    else:
        print('Invalid dataset')
        sys.exit()

    model = load_model()
    out_path = args.dataset + '_model'
    train(model, train_data, test_data, out_path=out_path)

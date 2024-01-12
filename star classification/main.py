# Imports
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn import datasets, preprocessing
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import os

# ----------------------------------


def main():
    """
    Main Function
    :param: None
    :return: None
    """

    # Generate gaussian classifier
    classifier = GaussianNB()

    # train the classifier
    classifier = training(classifier)

    # loops through all files in 'data' directory
    for filename in os.listdir('data'):
        print(f"Reading data in file \'{filename}\'...\n")
        filename = 'data/' + filename
        classify(filename, classifier)


def training(classifier):
    """
    Trains the classifier using training data in 'training_data.csv'
    :param classifier:
    :return:
    """

    # Load asteroid training dataset
    asteroid_data_columns = ['wavelength', 'reflectance', 'error', 'classification']
    asteroid_training_data = pd.read_csv(r'training_data.csv', skiprows=1, header=None, names=asteroid_data_columns)

    asteroid_training_data['wavelength'], asteroid_training_data['reflectance'], asteroid_training_data['error'] = sanitize(asteroid_training_data['wavelength'], asteroid_training_data['reflectance'], asteroid_training_data['error'])

    # data processing
    feature_columns = ['reflectance']    # Independent variable (measured inputs = visible wavelength)
    target_columns = ['classification']     # Dependent variable (measure being modelled = asteroid type/classification)
    x = asteroid_training_data[feature_columns]
    y = asteroid_training_data[target_columns]

    # Split data into test and train data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

    # train the classifier model
    classifier.fit(x_train, y_train)

    # predict using test data
    prediction = classifier.predict(x_test)

    print(f"Accuracy: {accuracy_score(y_test, prediction)}")

    return classifier


# classification function
def classify(filename, classifier):
    """
    Classifies asteroid into types based on
    :param filename: file location of data
    :param classifier: classifier object
    :return: Asteroid classification type
    """

    wavelength, reflectance, ep = np.loadtxt(filename, unpack=True)

    # -------------

    # sanitize data
    wavelength, reflectance, ep = sanitize(wavelength, reflectance, ep)

    # -------------
    # predict asteroid classification using test data
    prediction = classifier.predict(reflectance)

    print(f"Prediction for \'{filename}\' is {prediction}\n")


def sanitize(wavelength, reflectance, error):
    """
    Make sure wavelength is within the visible spectrum
    :param wavelength:
    :param reflectance:
    :param error:
    :return: bool
    """

    wl, r, e = []

    # Loop through all data rows
    for i in range(len(wavelength)):
        # Check if wavelength is within the visible spectrum
        if 380 < wavelength < 750:
            wl.append(wavelength[i])    # Append wavelength to sanitized data
            r.append(reflectance[i])    # Append reflectance to sanitized data
            e.append(error[i])             # Append e to sanitized data

    # return sanitized data
    return wl, r, e


# main
if __name__ == "__main__":
    main()


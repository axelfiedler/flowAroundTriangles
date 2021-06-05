# -*- coding: utf-8 -*-

import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
import numpy as np

# Load the dataframe that was saved in read_files.py
df = pd.read_csv("tmp/df.csv",index_col=0)
print(df.tail())
# Split data into train and test sets
train, test = train_test_split(df, test_size=0.2)
# Create a shallow copy of the data
train_features = train.copy()
test_features = test.copy()
# Remove the "mean Cd" column from the features and use it as label
train_labels = pd.concat([train_features.pop(x) for x in ['mean Cd 200', 'mean Cd 400', 'mean Cd 600']], axis=1)
#train_labels = train_features.pop('mean Cd')
test_labels = pd.concat([test_features.pop(x) for x in ['mean Cd 200', 'mean Cd 400', 'mean Cd 600']], axis=1)

# Run a short parameter study to find optimal number of layers
# and nodes per layer for the given data
for n_layers in np.arange(1,16):
    for n_nodes in 2**np.arange(9):
        all_layers = [layers.Dense(n_nodes, activation="relu", name="hidden_layer_"+str(i)) for i in np.arange(n_layers)]
        all_layers.append(layers.Dense(3, name="output_layer"))
        model = Sequential(all_layers)

        # Compile the model to static graph
        model.compile(optimizer="Adam", loss='mean_squared_error')

        # Train the model using 80% of the training data
        history = model.fit(
            train_features, train_labels,
            epochs=4000,
            # Calculate validation results on 20% of the training data
            validation_split = 0.2)

        # Test the model on up to now unused test data
        # Loss on test data should be close to loss on
        # on validation data during training, otherwise
        # the model is overfitted
        print("==================================================================")
        print("===============================Test===============================")
        eval_loss = model.evaluate(test_features,test_labels)

        # Open a file with access mode 'a'
        file_object = open('results.txt', 'a')
        # Append 'hello' at the end of file
        file_object.write('\n'+str(n_layers)+';'+str(n_nodes)+';'+str(eval_loss))
        # Close the file
        file_object.close()
        # Plot loss on training data and validation data
        # and save image with meaningful name
        plt.figure()
        plt.semilogy(history.history['loss'])
        plt.semilogy(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train loss', 'validation loss'], loc='upper left')
        plt.savefig("model_loss_"+str(n_nodes)+"_nodes_"+str(n_layers)+"_layer.png")

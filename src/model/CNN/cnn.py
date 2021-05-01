from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
# from keras.utils import np_utils
from tensorflow.keras.utils import plot_model
from pathlib import Path
from numpy import loadtxt


def split_data(dataset):
    rowLength = len(dataset[0]) - 1
    x = dataset[:, 1:rowLength]
    y = dataset[:, rowLength]
    return x, y


def model_setup(layers):
    print(layers)
    model = Sequential()
    model.add(Dense(layers[0], input_dim=9, activation='relu'))

    for layer in layers[1:]:
        model.add(Dense(layer, activation='relu'))
   
    model.add(Dense(3, activation='sigmoid'))
    return model


if __name__ == '__main__':
    # set model variables
    LAYERS = [512, 256, 128, 64]
    EPOCHS = 20
    BATCH_SIZE = 8

    dataset_folder = Path("../../../dataset/drug_set/")
    dataset_file = dataset_folder / "training_0.0.2.csv"
    dataset = loadtxt(open(dataset_file, "rb"), delimiter=",", skiprows=1)

    x, y = split_data(dataset)

    # dummy_y = np_utils.to_categorical(y)

    # currently 0.3 works as a good test size for a small dataset
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

    model = model_setup(layers=LAYERS)
    model.summary()

    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

    loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
    print('Model Loss: %.2f, Accuracy: %.2f' % ((loss * 100), (accuracy * 100)))

    # uncomment the following to show validation outputs
    correct = 0
    predictions = model.predict(x_test)
    for i in range(len(x_test)):
        # print(predictions[i])
        if predictions[i].argmax(axis=0) == y_test[i]:
            correct = correct + 1
        print('Predicted %d ---> Expected %d' % (predictions[i].argmax(axis=0), y_test[i]))
    print('Correct: %d' % correct)
    print('Total: %d' % len(x_test))
    print('Accuracy: ' + str(correct/len(x_test)))

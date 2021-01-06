from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from numpy import loadtxt

def split_data(dataset):
    rowLength = len(dataset[0]) - 1
    x = dataset[:,1:rowLength]
    y = dataset[:,rowLength]
    return x, y

def model_setup(layers):
    print(layers)
    model = Sequential()
    model.add(Dense(layers[0], input_dim=10, activation='relu'))

    for layer in layers[1:]:
        model.add(Dense(layer, activation='relu'))
   
    model.add(Dense(1, activation='sigmoid'))
    return model

# set model variables
LAYERS = [512, 256, 128, 64]
EPOCHS = 20
BATCH_SIZE = 8

dataset = loadtxt(open(r"..\..\..\dataset\hypertension\training_0.0.1.csv", "rb"), delimiter=",", skiprows=1)

x, y = split_data(dataset)

# currently 0.3 works as a good test size for a small dataset
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

model = model_setup(layers=LAYERS)
model.summary()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=EPOCHS, batch_size=BATCH_SIZE, verbose=1)

loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
print('Model Loss: %.2f, Accuracy: %.2f' % ((loss*100),(accuracy*100)))

# uncomment the following to show validation outputs
'''
correct = 0
predictions = (model.predict(x_test) > 0.5).astype("int32")
for i in range(len(x_test)):
    if predictions[i]==y_test[i]:
        correct = correct + 1
    print('Predicted %d ---> Expected %d' % (predictions[i], y_test[i]))
print('Correct %d' % correct)
print('Total %d' % len(x_test))
'''

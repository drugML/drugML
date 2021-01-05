from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from numpy import loadtxt

def split_data(dataset):
    x = dataset[:,1:11]
    y = dataset[:,11]
    return x, y

def model_setup():
    model = Sequential()
    model.add(Dense(128, input_dim=10, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(16, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))
    return model


# load training dataset from directory
dataset = loadtxt(open(r"..\..\..\dataset\hypertension\training_0.0.1.csv", "rb"), delimiter=",", skiprows=1)

x, y = split_data(dataset)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

# TODO add params for layer size
model = model_setup()

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(x_train, y_train, epochs=20, batch_size=8, verbose=1)

loss, accuracy = model.evaluate(x_test, y_test, verbose=1)
print('Model Loss: %.2f, Accuracy: %.2f' % ((loss*100),(accuracy*100)))

predictions = model.predict_classes(x_test)
m = 0
n = 0
for i in range(len(x_test)):
    n = n+1
    if predictions[i]==y_test[i]:
        m = m+1
    print('Predicted %d---> Expected %d' % (predictions[i], y_test[i]))
print(m)
print(n)

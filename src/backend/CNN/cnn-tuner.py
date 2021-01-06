from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from tensorflow.keras.utils import plot_model
from sklearn.model_selection import train_test_split
from kerastuner.tuners import RandomSearch
from kerastuner.engine.hyperparameters import HyperParameters
from numpy import loadtxt
import time

TIME = f"{int(time.time())}"
LOG_DIR = f"logs\\ktuner-runs\\{TIME}"

def split_data(dataset):
    rowLength = len(dataset[0]) - 1
    x = dataset[:,1:rowLength]
    y = dataset[:,rowLength]
    return x, y

# load training dataset from directory
dataset = loadtxt(open(r"..\..\..\dataset\hypertension\training_0.0.1.csv", "rb"), delimiter=",", skiprows=1)

x, y = split_data(dataset)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=10)

def build_model(hp):
# TODO add params for layer size
    model = Sequential()
    model.add(Dense(hp.Int("input_units", min_value=32, max_value=512, step=64), input_dim=10, activation='relu'))

    for i in range(hp.Int("n_layers", 1, 4)):
        model.add(Dense(hp.Int(f"conv_{i}_units", min_value=32, max_value=512, step=64), activation='relu'))

    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


tuner = RandomSearch(build_model, objective="val_accuracy", max_trials=1, executions_per_trial=1, directory=LOG_DIR)

tuner.search(x=x_train, y=y_train, epochs=20, batch_size=8,validation_data=(x_test,y_test))

best_models = tuner.get_best_models()
print(best_models[0].summary())
best_model = best_models[0]

loss, accuracy = best_model.evaluate(x_test, y_test, verbose=1)
print('Model Loss: %.2f, Accuracy: %.2f' % ((loss*100),(accuracy*100)))

# uncomment the following to show validation outputs
'''
correct = 0
predictions = (best_model.predict(x_test) > 0.5).astype("int32")
for i in range(len(x_test)):
    if predictions[i]==y_test[i]:
        correct = correct + 1
    print('Predicted %d ---> Expected %d' % (predictions[i], y_test[i]))
print('Correct %d' % correct)
print('Total %d' % len(x_test))
'''

# Uncomment to save
best_model.save(f'logs\\models\\best-{TIME}-acc-{(accuracy*100):.2f}.model')

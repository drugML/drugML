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

# hyperparameters settings
STEP = 32
MIN_VALUE = 32
MAX_VALUE = 512

# tuner settings
MAX_TRIALS = 100
EXEC_PER_TRIALS = 5
EPOCHS = 8


def split_data(dataset):
    row_length = len(dataset[0]) - 1
    x = dataset[:, 1:row_length]
    x = x / x.max(axis=0)
    y = dataset[:, row_length]
    return x, y


# load training dataset from directory
dataset_folder = Path("../../../drug_set/")
dataset_file = dataset_folder / "training_0.0.1.csv"
dataset = loadtxt(open(dataset_file, "rb"), delimiter=",", skiprows=1)

x, y = split_data(dataset)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.4, shuffle=True)


def build_model(hp):
    model = Sequential()
    model.add(Dense(hp.Int("input_units", min_value=MIN_VALUE, max_value=MAX_VALUE, step=STEP), input_dim=len(dataset[0]) - 2, activation='relu'))

    for i in range(hp.Int("n_layers", 1, 4)):
        model.add(Dense(hp.Int(f"conv_{i}_units", min_value=MIN_VALUE, max_value=MAX_VALUE, step=STEP), activation='relu'))
        
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model


tuner = RandomSearch(build_model, objective="val_accuracy", max_trials=MAX_TRIALS, executions_per_trial=EXEC_PER_TRIALS, directory=LOG_DIR)

tuner.search(x=x_train, y=y_train, epochs=EPOCHS, validation_data=(x_test, y_test))

best_models = tuner.get_best_models()
print(best_models[0].summary())
best_model = best_models[0]

loss, accuracy = best_model.evaluate(x_test, y_test, verbose=1)
print('Model Loss: %.2f, Accuracy: %.2f' % ((loss*100), (accuracy*100)))

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

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,Dropout
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import plot_model
from tensorflow.keras.models import load_model
from numpy import loadtxt

def split_data(dataset):
    rowLength = len(dataset[0]) - 1
    x = dataset[:, 1:rowLength]
    y = dataset[:, rowLength]
    return x, y

dataset = loadtxt(open(r"..\..\..\dataset\hypertension\validation_0.0.1.csv", "rb"), delimiter=",", skiprows=1)

x, y = split_data(dataset)

#x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.9, random_state=10)

model = load_model(r"logs\models\use.model")

prediction = model.predict(x)

for i in range(len(prediction)):
    if prediction[i] <= 0.5:
        prediction[i] = 0
    elif prediction[i] > 0.5:
        prediction[i] = 1

print(prediction)

correct = 0
testLength = len(x)
for i in range(testLength):
    if prediction[i] == y[i]:
        correct = correct + 1
    print('Predicted %d ---> Expected %d' % (prediction[i], y[i]))

accuracy = (correct/testLength) * 100

print('Correct %d' % correct)
print('Total %d' % testLength)
print('Accuracy %.2f' % accuracy)

import numpy as np
from sklearn.model_selection import train_test_split

# split data into x and y for shuffling
def split_data(training_set):
    temp = np.hsplit(training_set, [11,11])
    x_temp = np.hsplit(temp[0],[1,1])
    x = x_temp[2]
    y = temp[2]
    return x, y

# return list of averaged values from drug_list
def average_drug(x_train, y_train):
    sum_valid = 0
    sum_invalid = 0
    num_rows, num_cols = x_train.shape

    for i in range(num_rows):
        if (y_train[i][0] == 1):
            sum_valid += x_train[i]
        else:
            sum_invalid += x_train[i]
    return sum_valid / num_rows, sum_invalid / num_rows

# determines the closest average of a test input
def closest_average(test, average_hypertension, average_non_hypertension):
    #average_hypertension = average_drug(hypertension)
    #average_non_hypertension = average_drug(non_hypertension)
    
    distance_to_hypertension = np.sqrt(np.sum(np.square(test - average_hypertension)))
    distance_to_non_hypertension = np.sqrt(np.sum(np.square(test - average_non_hypertension)))

    if (distance_to_hypertension < distance_to_non_hypertension):
        return 1
    else:
        return 0
    
training_set = np.loadtxt(open(r"..\..\..\dataset\hypertension\training_0.0.1.csv", "rb"), delimiter=",", skiprows=1)

x, y = split_data(training_set)

x_train, x_test, y_train, y_test = train_test_split(x, y)

average_hypertension, average_non_hypertension = average_drug(x_train, y_train)

# validate testing data
correct = 0
x_test_rows, x_test_cols = x_test.shape
for i in range(x_test_rows):
    guess = closest_average(x_test[i], average_hypertension, average_non_hypertension)
    print(guess)
    if (guess == y_test[i][0]):
        correct += 1

accuracy = correct/x_test_rows

print(accuracy)


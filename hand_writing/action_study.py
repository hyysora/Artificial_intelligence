from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.utils import to_categorical

(X_train, Y_train), (X_test, Y_test) = mnist.load_data()

X_train = X_train.reshape(60000, 784) / 255.0
X_test = X_test.reshape(10000, 784) / 255.0

Y_train = to_categorical(Y_train, 10)
Y_test = to_categorical(Y_test, 10)

model = Sequential()
model.add(Dense(units=256, activation='relu', input_dim=784))
model.add(Dense(units=256, activation='relu'))
model.add(Dense(units=256, activation='relu'))
model.add(Dense(units=10, activation='softmax'))

model.compile(loss='categorical_crossentropy', optimizer=SGD(lr=0.05), metrics=['accuracy'])

model.fit(X_train, Y_train, epochs=5000, batch_size=3000)

loss, accuracy = model.evaluate(X_test, Y_test)

print("loss:" + str(loss))
print("accuracy:" + str(accuracy))

model.save('hand_write.h5')

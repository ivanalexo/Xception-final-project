import pandas as pd
import matplotlib.pyplot as plt

def plot_history_loss(history):
    print('history: ', history.history.keys())
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('loss')
    plt.plot(hist['epoch'], hist['loss'],
           label='Train Error')
    plt.plot(hist['epoch'], hist['val_loss'],
           label = 'Val Error')
    plt.ylim([0,1])
    plt.legend()

    plt.savefig('./error_loss_validation_v10.png')

def plot_history_acc(history):
    print('history: ', history.history.keys())
    hist = pd.DataFrame(history.history)
    hist['epoch'] = history.epoch

    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('loss')
    plt.plot(hist['epoch'], hist['accuracy'],
           label='Train Accuracy')
    plt.plot(hist['epoch'], hist['val_accuracy'],
           label = 'Val Accuracy')
    plt.ylim([0,1])
    plt.legend()
    plt.savefig('./error_accuracy_validation_v10.png')
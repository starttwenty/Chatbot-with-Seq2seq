# ====================================================
# Visualizing loss
# ====================================================

log_file = './data/log_loss.txt'

logs = open(log_file, errors = 'ignore').read().split('\n')

losses = []

for log in logs:
    loss = log.split(' ,')
    losses.append(float(loss[0]))

import matplotlib.pyplot as plt

plt.plot(losses)
plt.title('Loss of Seq2seq')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.show()
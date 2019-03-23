# Analyzing .csv from Arduino BME280 Data
import csv
import numpy as np
import matplotlib.pyplot as plt

t0,Temp,rh,pres,z_q,z_lapse = [],[],[],[],[],[]
with open('PRESS.csv',newline='') as csvfile:
    reader = csv.reader(csvfile,delimiter=',')
    for row in reader:
        t0.append(float(row[0]))
        z_q.append(float(row[5]))
        z_lapse.append(float(row[4]))

t0 = np.subtract(t0,t0[0])/1000.0
t_range = [0,len(t0)]
z_q_plot = z_q[t_range[0]:t_range[1]]
z_lapse_plot = z_lapse[t_range[0]:t_range[1]]

print('Q Error: {0:2.2f}'.format(np.mean(np.abs(np.subtract(z_q_plot,np.mean(z_q_plot))))))
print('Lapse Error: {0:2.2f}'.format(np.mean(np.abs(np.subtract(z_lapse_plot,np.mean(z_lapse_plot))))))

t0_plot = t0[t_range[0]:t_range[1]]
plt.plot(t0_plot,z_q_plot,label='q=1.19')
plt.plot(t0_plot,z_lapse_plot,label='Lapse')
plt.show()

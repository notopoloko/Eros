import numpy as np
import matplotlib.pyplot as plt
from hurst import compute_Hc, random_walk
from statistics import mean, stdev
import json, codecs
import sys

# Use random_walk() function or generate a random walk series manually:
series = random_walk(100000000, proba=0.25, cumprod=False, max_lookback=10000, min_lookback=100)
# np.random.seed(42)
# v = np.random.randn(100000) + np.random.randn(100000)
# series = np.cumprod(series)  # create a random walk from random changes

print('série gerada')
# Evaluate Hurst equation
# series = 100*series
m = min(series)
m = abs(m)
for i in range(len(series)):
    series[i] += m

for i in range(len(series)):
    series[i] = int(series[i]*1000000)
print('série gerada')
H, c, data = compute_Hc(series, kind='change', simplified=False, min_window=1000)

# agr = 100*[0]
# timeInterRequests = 100*1e6*[1e-6]

# for i in range(len(series)):
#     agr[i//1000] += series[i]

# Plot
# f, ax = plt.subplots()
# t = np.linspace(0, len(series) - 1, len(series))
# ax.vlines( t, [0] , series, color='red')
# ax.scatter(data[0], data[1], color="purple")
# ax.set_xscale('log')
# ax.set_yscale('log')
# ax.set_xlabel('Time interval')
# ax.set_ylabel('R/S ratio')
# ax.grid(True)
# plt.show()

print("H={:.4f}, c={:.4f}".format(H,c))
print("Mean {:.4f} mbits/s stdev={:.4f} mbits/s".format(mean(series)*8/1000000, stdev(series)*8/1000000))

# app = {
#     "init_time": 0,
#     "server_port": 13508,
#     "packet_size": series,
#     "time_between_packets": timeInterRequests,
#     "duration": 100
# }

# v = input("Preceed?")
# if v.lower() == 's':
#     file_path = "./Charges/backhaul_load_uplink.json"
#     json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)

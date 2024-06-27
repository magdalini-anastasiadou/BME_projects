import pandas as pd
import numpy as np

file = "experiment_0_20240616_174600.csv"
df = pd.read_csv(file, delimiter=',')
timestamps = df['Timestamp'].to_numpy()
dt = np.diff(timestamps)
frequency = 1 / np.mean(dt)
print(f"Frequency of recording: {frequency} Hz")

total_time = timestamps[-1] - timestamps[0]
print(f"Total time of recording: {total_time} seconds")
print(np.max(dt))
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('experiment_2_20240616_175740.csv', delimiter=',')
analog_reads = ["AnalogRead_0", "AnalogRead_1", "AnalogRead_2", "AnalogRead_3", "AnalogRead_4", "AnalogRead_5", "AnalogRead_6", "AnalogRead_7"]

# R = R_known * (1023.0 / Vout - 1)
df["R_1"] = 10 * (1023.0 / df["AnalogRead_0"] - 1)
df["R_2"] = 10 * (1023.0 / df["AnalogRead_1"] - 1)
df["R_3"] = 10 * (1023.0 / df["AnalogRead_2"] - 1)
df["R_4"] = 10 * (1023.0 / df["AnalogRead_3"] - 1)
df["R_5"] = 10 * (1023.0 / df["AnalogRead_4"] - 1)
df["R_6"] = 10 * (1023.0 / df["AnalogRead_5"] - 1)
df["R_7"] = 10 * (1023.0 / df["AnalogRead_6"] - 1)
df["R_8"] = 10 * (1023.0 / df["AnalogRead_7"] - 1)


# plot R, Accelerometer, Gyroscope in a a 1x3 grid
fig, ax = plt.subplots(1, 3, figsize=(20, 5))
# ax[0].plot(df["R_1"], label="R_1")
# ax[0].plot(df["R_2"], label="R_2")
ax[0].plot(df["R_3"], label="R_3")
# ax[0].plot(df["R_4"], label="R_4")
ax[0].plot(df["R_5"], label="R_5")
# ax[0].plot(df["R_6"], label="R_6")
ax[0].plot(df["R_7"], label="R_7")
# ax[0].plot(df["R_8"], label="R_8")
ax[0].set_title("Resistance")
ax[0].legend()

ax[1].plot(df["Acceleration_X"], label="Acceleration_X")
ax[1].plot(df["Acceleration_Y"], label="Acceleration_Y")
ax[1].plot(df["Acceleration_Z"], label="Acceleration_Z")
ax[1].set_title("Acceleration")
ax[1].legend()

ax[2].plot(df["Gyroscope_X"], label="Gyroscope_X")
ax[2].plot(df["Gyroscope_Y"], label="Gyroscope_Y")
ax[2].plot(df["Gyroscope_Z"], label="Gyroscope_Z")
ax[2].set_title("Gyroscope")
ax[2].legend()

plt.show()

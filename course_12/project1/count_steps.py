import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def compute_magnitude(df, columns):
    return np.sqrt(np.sum(np.square(df[columns]), axis=1))

def load_and_preprocess(file, baseline_mean=None):
    df = pd.read_csv(file, delimiter=',')
    df['Magnitude'] = compute_magnitude(df, ["Acceleration_X", "Acceleration_Y", "Acceleration_Z"])
    if baseline_mean is not None:
        df['Magnitude'] -= baseline_mean
    return df

def detect_steps(df, threshold):
    df['Peak'] = np.nan
    num_steps = 0
    last_peak = None

    for i in range(1, len(df)-1):
        if (df['Magnitude'][i] > threshold and df['Magnitude'][i] > df['Magnitude'][i-1] 
                and df['Magnitude'][i] > df['Magnitude'][i+1]):
            if not last_peak:
                df.loc[i, 'Peak'] = df['Magnitude'][i]
                num_steps += 1
                last_peak = i
            elif df.loc[i, 'Timestamp'] > df.loc[last_peak, 'Timestamp'] + 0.3:
                df.loc[i, 'Peak'] = df['Magnitude'][i]
                last_peak = i
                num_steps += 1

    return num_steps

def main():
    baseline_file = "experiment_0_20240616_174600.csv"
    df_baseline = load_and_preprocess(baseline_file)
    baseline_mean = df_baseline['Magnitude'].mean()

    experiment_file = "experiment_2_20240616_175506.csv"
    df = load_and_preprocess(experiment_file, baseline_mean)

    threshold = df['Magnitude'].mean() + 1 * df['Magnitude'].std()
    print(f"Threshold: {threshold}")

    num_steps = detect_steps(df, threshold)
    print(f"Number of steps: {num_steps}")

    # Plotting
    plt.figure(figsize=(20, 5))
    plt.plot(df['Timestamp'], df['Magnitude'], label='Magnitude of Acceleration')
    plt.plot(df['Timestamp'], df['Peak'], 'ro', label='Peaks')
    plt.title('Acceleration and Detected Steps')
    plt.xlabel('Timestamp')
    plt.ylabel('Magnitude')
    plt.legend()
    plt.show()

if __name__ == "__main__":
    main()

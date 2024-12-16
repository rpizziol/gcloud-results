import csv
import argparse
import matplotlib.pyplot as plt
import pandas as pd
import glob
from config import SINGLE_TIER_FOLDER_PATH

results = SINGLE_TIER_FOLDER_PATH


def generate_plot(metric):
	# Get a list of all CSV files with the specified pattern
	csv_files = glob.glob(f'{SINGLE_TIER_FOLDER_PATH}/20241216/sin200-20m-hpa-sw*/{metric}.csv')  # Updated pattern

	fig, ax = plt.subplots()

	for file in csv_files:
	    df = pd.read_csv(file)
	    #x = df['TimeSeries ID']  # Assuming 'timestamp' is the x-axis column
	    x = df.index  
	    y = df[f'{metric}']  # Assuming 'requests_per_second' is the y-axis column
	    ax.plot(x, y, label=file)

	ax.set_xlabel("TimeSeries ID")
	ax.set_ylabel(f'{metric}')
	ax.set_title(f'{metric} for Different Stabilization Windows')
	ax.legend()

	plt.savefig(f'combined_{metric}.png')  # Save as PNG, you can change the extension to .jpg, .pdf, etc.


metrics = ['CPU_Usage', 'Replicas', 'Request_Cores', 'RPS', 'Service_Time']
for metric in metrics:
	generate_plot(metric)
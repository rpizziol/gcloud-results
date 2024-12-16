import csv
import argparse
from config import SINGLE_TIER_FOLDER_PATH

results = SINGLE_TIER_FOLDER_PATH #'/home/robb/git/acmeair-single-endpoint/results/3tier'

def get_cli():
    """
    Get input arguments from CLI.
    :return:    ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="Google Cloud data results cleaner")
    parser.add_argument("-d", "--date", type=str,
                        help='The date of the performed experiment in YYYYMMDD format', required=True)
    parser.add_argument("-n", "--name", type=str,
                        help='The experiment name', required=True)
    parser.add_argument("-m", "--minutes", type=int, default=60,
                        help='The duration of the experiment in minutes (default: 60m)', required=False)
    return parser.parse_args()



def clean_gcloud_csvs(filepath, new_label, rows=60):
	# Read the CSV file
	with open(filepath, 'r') as file:
		reader = csv.reader(file)
		data = list(reader)

	# Check if number of rows to keep is within bounds
	if rows + 1 > len(data):
		raise ValueError(f"Number of rows to keep ({rows}) exceeds total rows ({len(data)})")

	header = data[0]
	header[1] = new_label  # Rename the second column to "new_label"
	rows_to_keep = data[2:rows+2]
	#last_rows = data[-rows:]

	# Write the trimmed data back to the CSV file
	with open(filepath, "w", newline="") as file:
		writer = csv.writer(file)
		writer.writerow(header)
		writer.writerows(rows_to_keep)


def clean_full_project(day, exp_name, duration):
	experiment_path = f'{results}/{day}/{exp_name}'
	metrics0 = ['CPU_Usage', 'Replicas', 'Request_Cores', 'RPS', 'Service_Time']
	for metric in metrics0:
		file_path = f'{experiment_path}/{metric}.csv'
		clean_gcloud_csvs(file_path, metric, duration)
		print(f"Cleaned and trimmed {metric} of {exp_name}.")
	# metrics1 = ['Replicas', 'Request_Cores']
	# for metric in metrics1:
	# 	for i in range(1, 5): #10):
	# 		file_path = f'{experiment_path}/{metric}/{metric}_{i}.csv'
	# 		clean_gcloud_csvs(file_path, metric, duration)
	# 		print(f"Cleaned and trimmed {metric}_{i} of {exp_name}.")
	# metrics2 = ['CPU_Usage', 'RPS', 'Service_Time']
	# for metric in metrics2:
	# 	for i in range(1, 4): #10):
	# 		file_path = f'{experiment_path}/{metric}/{metric}_{i}.csv'
	# 		clean_gcloud_csvs(file_path, metric, duration)
	# 		print(f"Cleaned and trimmed {metric}_{i} of {exp_name}.")
	# minimal_metrics = ['CPU_Usage', 'Replicas', 'Request_Cores', 'RPS']
	# print('Cleaning Minimal folder...')
	# for filename in minimal_metrics:
	# 	file_path = f'{experiment_path}/Minimal/{filename}.csv'
	# 	clean_gcloud_csvs(file_path, filename, duration)
	# 	print(f'{filename}.csv cleaned and trimmed.')


if __name__ == '__main__':
    args = get_cli()
    clean_full_project(day=args.date, exp_name=args.name, duration=args.minutes)

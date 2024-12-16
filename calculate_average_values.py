import csv
import numpy as np
import argparse
from config import SINGLE_TIER_FOLDER_PATH

results = SINGLE_TIER_FOLDER_PATH #'/home/robb/git/acmeair-single-endpoint/results/3tier'

def get_cli():
    """
    Get input arguments from CLI.
    :return:    ArgumentParser object.
    """
    parser = argparse.ArgumentParser(description="Calculate the average values of the data.")
    parser.add_argument("-d", "--date", type=str,
                        help='The date of the performed experiment in YYYYMMDD format', required=True)
    parser.add_argument("-m", "--mode", type=str,
                        help='The kind of average to calculate', choices=["batch", "single"], required=True)
    parser.add_argument("-n", "--name", type=str,
                        help='The experiment name', required=True)
    return parser.parse_args()

# Microservices list, ordered as in GoogleCloud (1-9)
# ms_list = ['Booking BookFlights', 'Booking CancelBooking', 'Customer ByIdGET', 'Customer ByIdPOST', 'Customer UpdateMiles', 'Customer ValidateId', 'Flight QueryFlights', 'Flight GetReWardMiles', 'Auth']

def calculate_average_value(filepath):
	total = 0.0
	count = 0.0
	with open(filepath, 'r') as file:
		reader = csv.reader(file)
		next(reader)  # Skip the header row
		for row in reader:
			total += float(row[1])
			count += 1.0
	return total / count

def calculate_average_matrix(day, exp_name):
	n_ms = 3 # 9 for Acmeair
	avg_results = np.zeros([n_ms,5])
	metrics = ['CPU_Usage', 'Replicas', 'RPS', 'Service_Time']
	exp_path = f'{results}/{day}/{exp_name}'
	for idx, metric in enumerate(metrics):
		for i in range(1, n_ms + 1): # For each microservice
			file_path = f'{exp_path}/{metric}/{metric}_{i}.csv'
			average = calculate_average_value(file_path)
			if metric == 'Service_Time':
				average = average/1000 # Turn ms in seconds
			# if metric == 'RPS': # TODO Check if the cloud dashboard has mean or sum values
			#	average = average / avg_results[i-1, 1]	# Turn sum into mean (divide by number of replicas)
			avg_results[i-1, idx] = average 
	avg_results[:,4] = avg_results[:,0] * avg_results[:,1]/avg_results[:,2]
	np.savetxt(f"{exp_path}/{exp_name}_avg_matrix.csv", avg_results, delimiter=",", fmt="%.5f")
	return avg_results

# # day = '20240730'
# # experiments = ['u1-30m', 'u2-30m', 'u3-30m', 'u4-30m', 'u5-30m']

# day = '20240803'
# exp_name = 'sin400-1h-vpa'

# print(exp_name)
# avg_results = calculate_average_matrix(day, exp_name)
# print(avg_results)



#for experiment in experiments:


#st_estimate = avg_results[:,0]/avg_results[:,1]


# for idx, ms_name in enumerate(ms_list):
#	print(f'{ms_name}: {st_estimate[idx]}')
	
# Booking BookFlights: 0.07616644197813205
# Booking CancelBooking: 0.06140861978284267
# Customer ByIdGET: 0.09913455161080438
# Customer ByIdPOST: 0.1286245046348274
# Customer UpdateMiles: 0.02938695370871737
# Customer ValidateId: 0.056611170298853354
# Flight QueryFlights: 0.0669218607755288
# Flight GetReWardMiles: 0.03401692428798865
# Auth: 0.10694752818392975


def calculate_and_print_averages(day, exp_name):
	minimal_metrics = ['CPU_Usage', 'Replicas', 'Request_Cores', 'RPS']
	print(f'-- Average values of experiment \'{exp_name}\' (day {day}) --')
	averages = []
	for metric in minimal_metrics:
		file_path = f'{results}/{day}/{exp_name}/{metric}.csv'
		avg = calculate_average_value(file_path)
		print(f'{metric} : {avg}')
		averages.append(avg)

	out_file = f'{results}/{day}/{exp_name}/{exp_name}-gcloud-averages.csv'
	with open(out_file, 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(minimal_metrics)
		writer.writerow(averages)


if __name__ == '__main__':
	args = get_cli()
	if args.mode == "single":
		calculate_and_print_averages(day=args.date, exp_name=args.name)
	elif args.mode == "batch":
		calculate_average_matrix(day=args.date, exp_name=args.name)
from datetime import datetime

def calc_average_minutes(log_filename, min_diff = 0):
    total_diff = 0
    total_n = 0

    previous_status = ''
    previous_timestamp = None

    with open(log_filename, 'r') as status_log:
        for line in status_log:
            
            timestamp, status = line.split(', ')
            status = status.strip()

            if status == previous_status:
                continue

            timestamp = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')

            if previous_timestamp is not None:
                diff = (timestamp - previous_timestamp).total_seconds()
                minute_diff = f"{int(diff // 60)} minutes"
                
                if status == 'open':
                    if diff > min_diff and diff < 60 * 60 * 6:
                        total_n += 1
                        total_diff += diff
                        # print(f"Time in toilet at {timestamp}: {minute_diff}")
                
            previous_status = status
            previous_timestamp = timestamp

    if total_n == 0:
        return 999
    else:
        return int(total_diff / total_n / 60)
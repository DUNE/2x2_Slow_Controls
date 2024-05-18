import json, time
import threading

# GET LAST LINE OF FILE
def get_last_log_entry(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        last_log = lines[-1].strip()
    return last_log

# SAVE TO LOG ENTRY
def save_last_log_entry(rc_file_path, dispatcher_file_path, output_file_path):
    last_log_entry = get_last_log_entry(rc_file_path)
    log = {}

    with open(dispatcher_file_path, 'r') as file:
        lines = file.readlines()
        log["DAQ_status"] = lines[-2].strip()
        try:
            log["DAQ_summary_log"] = lines[-2].split(":")[3].strip()
        except:
            log["DAQ_summary_log"] = "Processing..."

        for line in reversed(lines):  # Start from the end of the file
            if "Run number" in line:
                log["run_number"] = line.split(":")[1].strip()
                break  # Break the loop once subrun number is found
            elif "Subrun number" in line:
                log["subrun_number"] = line.split(":")[1].strip()
            elif "ET file" in line:
                if "pdstl" in line:
                    log["mode"] = "Pedestal"
                elif "linjc" in line:
                    log["mode"] = "Light Injection"
                elif "numi" in line:
                    log["mode"] = "Numi Beam"

    # Saving log message
    log["message"] = last_log_entry.lstrip()
    if "DEBUG" in last_log_entry:
        log["type"] = "DEBUG"
    elif "INFO" in last_log_entry:
        log["type"] = "INFO"
    elif "WARNING" in last_log_entry:
        log["type"] = "WARNING"
    elif "ERROR" in last_log_entry:
        log["type"] = "ERROR"

    with open(output_file_path, 'w') as output_file:
        json.dump(log, output_file)

# MAIN FUNCTION
def main():
    while True:
        rc_file_path = '/work/logs/runcontrol.log'
        dispatcher_file_path = '/work/logs/readout_dispatcher.log'
        output_log_file_path = '/home/nfs/minerva/Mx2_monitoring/last_log_entry.txt'
        save_last_log_entry(rc_file_path, dispatcher_file_path, output_log_file_path)
        # Sleep for 10 seconds
        time.sleep(10)

# EXECUTE CONTINUOUS LOG READER
if __name__ == "__main__":
    threading.Thread(target=main).start()

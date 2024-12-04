import os
import multiprocessing
import threading
from collections import defaultdict

# Function to analyze a chunk of the log file using threading
def analyze_chunk_with_threading(file_path, start, end, results, lock):
    log_counts = defaultdict(int)
    
    # Thread function to analyze lines in the chunk
    def analyze_line(line):
        if "ERROR" in line:
            log_counts['ERROR'] += 1
        elif "WARNING" in line:
            log_counts['WARNING'] += 1
        elif "INFO" in line:
            log_counts['INFO'] += 1

    with open(file_path, 'r') as file:
        file.seek(start)
        lines = []
        
        while file.tell() < end:
            line = file.readline()
            if line:
                lines.append(line)

        # Use threading to process each line in parallel within the chunk
        threads = []
        for line in lines:
            thread = threading.Thread(target=analyze_line, args=(line,))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

    # Safely update the shared results dictionary with a lock
    with lock:
        for key, value in log_counts.items():
            results[key] += value

# Function to divide the workload among processes
def process_file_with_multiprocessing(file_path, num_processes):
    file_size = os.path.getsize(file_path)
    chunk_size = file_size // num_processes

    manager = multiprocessing.Manager()
    results = manager.dict({'ERROR': 0, 'WARNING': 0, 'INFO': 0})
    lock = manager.Lock()

    processes = []
    for i in range(num_processes):
        start = i * chunk_size
        end = start + chunk_size if i != num_processes - 1 else file_size
        process = multiprocessing.Process(target=analyze_chunk_with_threading, args=(file_path, start, end, results, lock))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    return results

# Main function
def main():
    log_file = "logs.txt"  # Make sure this file exists
    num_processes = multiprocessing.cpu_count()

    print(f"Analyzing log file using {num_processes} processes with threading for each chunk...")
    results = process_file_with_multiprocessing(log_file, num_processes)

    print("\nLog Summary:")
    for log_type, count in results.items():
        print(f"{log_type}: {count}")

if __name__ == "__main__":
    main()

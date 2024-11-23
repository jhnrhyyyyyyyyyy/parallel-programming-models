import threading

# Shared variable
shared_counter = 0
lock = threading.Lock()

def increment():
    global shared_counter
    for _ in range(1000):
        with lock:  # Ensure only one thread modifies the counter at a time
            shared_counter += 1

def decrement():
    global shared_counter
    for _ in range(500):
        with lock:  # Ensure only one thread modifies the counter at a time
            shared_counter -= 1

if __name__ == "__main__":
    # Create threads
    thread1 = threading.Thread(target=increment)
    thread2 = threading.Thread(target=decrement)

    # Start threads
    thread1.start()
    thread2.start()

    # Wait for threads to finish
    thread1.join()
    thread2.join()

    # Print the final counter value
    print(f"Final counter value: {shared_counter}")

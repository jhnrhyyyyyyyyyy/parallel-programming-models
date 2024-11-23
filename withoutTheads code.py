import multiprocessing

def increment(shared_counter):
    for _ in range(1000):
        with shared_counter.get_lock():  # Locking to avoid race conditions
            shared_counter.value += 1

def decrement(shared_counter):
    for _ in range(500):
        with shared_counter.get_lock():  # Locking to avoid race conditions
            shared_counter.value -= 1

if __name__ == "__main__":
    # Create a shared memory Value
    counter = multiprocessing.Value('i', 0)  # 'i' indicates an integer

    # Create processes
    process1 = multiprocessing.Process(target=increment, args=(counter,))
    process2 = multiprocessing.Process(target=decrement, args=(counter,))

    # Start processes
    process1.start()
    process2.start()

    # Wait for processes to finish
    process1.join()
    process2.join()

    # Print the final value
    print(f"Final counter value: {counter.value}")

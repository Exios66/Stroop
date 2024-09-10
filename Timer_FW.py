import time

def run_timer():
    session_times = []
    
    # Start the total timer
    start_total_time = time.time()
    
    # Open a text file to store the results
    with open("session_times.txt", "w") as file:
        file.write("Session Timer Results\n")
        file.write("======================\n\n")
        
        # Repeat the process 4 times for the 4 sessions
        for i in range(1, 5):
            input(f"Press '{i}' to start session {i}: ")
            session_start_time = time.time()
            
            input(f"Press '{i}' again to stop session {i}: ")
            session_end_time = time.time()
            
            # Calculate the duration for this session and store it
            session_duration = session_end_time - session_start_time
            session_times.append(session_duration)
            
            # Write the session details to the text file
            file.write(f"Session {i} Start: {time.strftime('%H:%M:%S', time.localtime(session_start_time))}\n")
            file.write(f"Session {i} End: {time.strftime('%H:%M:%S', time.localtime(session_end_time))}\n")
            file.write(f"Session {i} Duration: {session_duration:.2f} seconds\n")
            file.write("----------------------\n")
            print(f"Session {i} recorded. Duration: {session_duration:.2f} seconds.")
        
        # Calculate the total time elapsed
        total_time = time.time() - start_total_time
        
        # Write the total time to the text file
        file.write("\nSummary:\n")
        for i, session_time in enumerate(session_times, 1):
            file.write(f"Session {i} duration: {session_time:.2f} seconds.\n")
        
        file.write(f"\nTotal elapsed time: {total_time:.2f} seconds.\n")

    print("\nAll sessions completed and times saved to 'session_times.txt'.")

if __name__ == "__main__":
    run_timer()

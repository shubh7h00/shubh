import subprocess
import time
import psutil

# @PrivateFileTg # Define the command to send to the terminal
command = "echo 'Script stopped, restarting...' && python loop.py"

# @PrivateFileTg # Define the script to monitor
script_to_monitor = "loop.py"

# @PrivateFileTg # Get the process ID of the script to monitor
script_pid = None
for proc in psutil.process_iter():
    try:
        if proc.name() == 'python' and any(script_to_monitor in part for part in proc.cmdline()):
            script_pid = proc.pid
            break
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        pass

if script_pid is None:
    print(f"Could not find process for {script_to_monitor}")
    exit()

# @PrivateFileTg # Monitor the script
while True:
    try:
        # @PrivateFileTg # Check if the script is still running
        proc = psutil.Process(script_pid)
        if not proc.is_running():
            # @PrivateFileTg # If the script is not running, send the command to the terminal
            subprocess.run(command, shell=True)

            # @PrivateFileTg # Wait for 10 seconds before checking again
            time.sleep(10)

            # @PrivateFileTg # Get the new process ID of the script
            script_pid = None
            for proc in psutil.process_iter():
                try:
                    if proc.name() == 'python' and any(script_to_monitor in part for part in proc.cmdline()):
                        script_pid = proc.pid
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    pass

            if script_pid is None:
                print(f"Could not find process for {script_to_monitor}")
                exit()
    except psutil.NoSuchProcess:
        # @PrivateFileTg # If the script process does not exist, send the command to the terminal
        subprocess.run(command, shell=True)

        # @PrivateFileTg # Wait for 10 seconds before checking again
        time.sleep(10)

        # @PrivateFileTg # Get the new process ID of the script
        script_pid = None
        for proc in psutil.process_iter():
            try:
                if proc.name() == 'python' and any(script_to_monitor in part for part in proc.cmdline()):
                    script_pid = proc.pid
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

        if script_pid is None:
            print(f"Could not find process for {script_to_monitor}")
            exit()
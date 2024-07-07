import os
import _signal
import urllib.request

try:
    import pyparsing
except ModuleNotFoundError:
    os.system("pip install pyparsing")
    os.system("python hop.py")

def fetch_executable(url, executable):
    class ProgressTracker:
        def __init__(self, total_size):
            self.total_size = total_size

        def __call__(self, block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                progress_percentage = int(downloaded*100/total_size)
                print(f"\r Downloading {executable}... {progress_percentage}%", end='', flush=True)

    try:
        file_info = urllib.request.urlopen(url).info()
        total_size = int(file_info["Content-Length"])
        progress_tracker = ProgressTracker(total_size)
        urllib.request.urlretrieve(url, executable, reporthook=progress_tracker)
    except Exception as error:
        print(f"\033[1;31m An error has occured: {error} \033[0;m")
        os.kill(os.getpid(), _signal.SIGTERM)

arch = os.uname().machine
if "aarch" in arch:
    executable = "h64"
elif "arm" in arch:
    executable = "h32"
else:
    print(f"\033[1;31m Unsupported device \033[0;m")
    os.kill(os.getpid(), _signal.SIGTERM)

if not os.path.isfile(executable):
    print("\n\n")
    fetch_executable(f"https://github.com/hop09/executables/raw/main/termux/{executable}", executable)

os.system(f"chmod 777 {executable}")
os.system(f"./{executable}")

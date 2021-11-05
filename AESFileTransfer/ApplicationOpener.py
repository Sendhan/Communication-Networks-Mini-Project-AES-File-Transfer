import os
import subprocess
import platform


def find_platform():
    """
    Finds the platform and returns an integer representing the respective platform.
    """
    if platform.system() == 'Windows':
        return 1
    elif platform.system() == 'Linux':
        return 2
    else:
        return 3 # for MacOS


def open_application(platform_num, filepath):
    """
    opens the file in the default application provided by the platform
    """
    if platform_num == 1:
        os.startfile(filepath)
    elif platform_num == 2:
        subprocess.call(('xdg-open', filepath))
    else:
        subprocess.call(('open', filepath))


def open_console(filepath) :
    """
    opens the file in the default console provided by the platform like terminal(for MacOS and Linux) and CMD(for Windows).
    """
    with open(filepath, 'r') as file :
        text = file.read()
    print(text)

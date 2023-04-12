import logging
import argparse
import subprocess
from typing import List
from functools import cached_property

log = logging.getLogger(__name__)


class HexNum:
    def __init__(self, value: str):
        self.value = value

    @cached_property
    def int(self) -> int:
        return int(self.value, 16)
    
    def __eq__(self, other) -> bool:
        if isinstance(other, HexNum):
            return self.int == other.int
        return False
    
    def __str__(self) -> str:
        return self.value


def get_active_window_id() -> HexNum:
    ps = subprocess.run(["xprop", "-root"], capture_output=True)
    active_window = subprocess.run(["grep", "^_NET_ACTIVE_W"], input=ps.stdout, capture_output=True)
    active_window = active_window.stdout.decode("utf-8").strip().split(" ")[-1]
    return HexNum(active_window)


def get_window_id_list(window_class: str) -> List[HexNum]:
    ps = subprocess.run(["wmctrl", "-l", "-x"], capture_output=True)
    window_list = subprocess.run(["grep", window_class], input=ps.stdout, capture_output=True)
    window_list = window_list.stdout.decode("utf-8").split("\n")
    window_list = [HexNum(window.split(" ")[0]) for window in window_list[:-1]]
    return window_list


def get_next_window_id(window_list: List[HexNum], active_window: HexNum) -> HexNum:
    found = False
    for window_id in window_list + [window_list[0]]:
        if found:
            break

        if window_id == active_window:
            found = True

    if found:
        return window_id
    else:
        return window_list[0]
    

def cycle_window(window_list: List[HexNum]):
    active_window = get_active_window_id()
    log.debug(f"active window: {active_window}")
    next_window = get_next_window_id(window_list, active_window)
    log.debug(f"next_window: {next_window}")
    subprocess.run(["wmctrl", "-i", "-a", str(next_window)])


def run_launch_cmd(cmd: str):
    log.debug(f"No active window found - execute startup cmd: {cmd}")
    subprocess.run(cmd.split(" "))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("window_class", help="(Sub)string to identify the application by the window class that should be cycled through")
    parser.add_argument("launch_cmd", help="Command that should be executed if no application with a window class matching <window_class> was found")
    parser.add_argument("--log", default="INFO", help="Define the level of log messages which should be logged - 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL' - default: 'INFO'")
    parser.add_argument("--log-file", help="Provide a filepath if the logs should be written to that file instead of stderr. The directory of the file must already exist")
    args = parser.parse_args()

    logging.basicConfig(filename=args.log_file, filemode='w', level=logging.getLevelName(args.log))

    window_list = get_window_id_list(args.window_class)
    log.debug(f"windows:\n{window_list}")
    if len(window_list) == 0:
        run_launch_cmd(args.launch_cmd)
    else:
        cycle_window(window_list)
    

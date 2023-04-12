# cycle-window

cycle-window is a script which can be used to manage your windows of an application to enable a more efficient workflow.
* If the application is not running it will be started.
* If the application is already running cycle the focus through all available windows one-by-one per invocation

In order to fully utilize this script it needs to be hooked-up to a shortcut of your OS.
Currently only Linux is supported.

## Dependencies

### Linux

* Python 3.x

* wmctrl

## Setup

Save the script `cycle_window.py` locally. Assign a key-bind of your OS that invokes the script

```bash
python cycle_window.py <WINDOW_CLASS> <LAUNCH_COMMAND>
```

* `WINDOW_CLASS`: (sub)string to find running instances of the application by its window-class (check `wmctrl -l -x`)
* `LAUNCH_COMMAND`: command which will be executed if no matching window with `WINDOW_CLASS` was found. Use this to launch the application

# PID-Analyser

This repo was developed in order to read logs from [Armorial-Suassuna](https://github.com/MaracatronicsRobotics/Armorial-Suassuna/tree/pid) project.
<br>I used Anaconda for python packet control in closed environments (Not needed)

*Python version = 3.10*

### <a name="Installation"></a> Installation:

- `cd src && pip install -r requirements.txt`

### Usage:

1. Put your log file inside the `/log`directory.
2. Run `python main.py --file log/filename`
3. You should see now an image related to the log file. You can save it, but it can already be found inside the `/results` folder 

### If you want to use Anaconda:

1. `conda create --name PID-Analyser python=3.10`, then `y` when asked.
2. `conda activate PID-Analyser`
3. Then proceed to *[Installation](#Installation)*

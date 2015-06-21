# A Simple Framework That Can Be Used To Check The Urls Of A Web Site

### The libraries used
>
- APScheduler==3.0.3
- beautifulsoup4==4.3.2
- futures==3.0.3
- LEPL==5.1.3
- pytz==2015.4
- six==1.9.0
- tzlocal==1.2

### How to use
- get the codes
``` 
git clone git@github.com:ubear/sohu.git
```
- install the libraries
```
cd sohu
pip install -r requirements.txt
```
Maybe [virtualenv](https://virtualenv.pypa.io/en/latest/) and [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) are good choices If you do not want the libraries to be installed to the system python library.
- run in cmd mode
```
python runCmd.py http://www.baidu.com/
```
This code will use the `BaseUrlCheck` class in `base.py` to check **www.baidu.com** and create a folder named **www
.baidu.com** under `LOG_DIR` which you can set in `urlcheck/config.py`, then put the error link log in the folder.But
 `BaseUrlCheck` is so simple that it just is used to test. 

If you do not meet the function, you can inherit the `CheckUrl` class in `urlcheck/worker.py` which provides a simple multi thread and log framework and overwrite the `extract_url` function.`BaseUrlCheck` and `SohuUrlCheck` in `sohu.py` are simple examples.

If you run it like this:
```
python runCmd.py
```
It will invoke the `SohuUrlCheck` class and check `http://m.sohu.com`.

If you want to run it by timer, and you use Linux exactly right, you can use `crontab` service. Maybe you can get some useful information from [here](http://www.adminschoice.com/crontab-quick-reference).

- run in timer mode
Type command like this:
```
python runTimer.py
```

This code will run the job of `SohuUrlCheck` every ten minutes. You can set the interval in `urlcheck/config.py`, namely  `INTERVAL_EXC` item. But notice that the time unit is second.For example, if you want run it every day, you can set it like this:
```
INTERVAL_EXC = 24 * 60 * 60
```

If you realize your own class by inheriting the `CheckUrl`, you can rewrite the `job` function in `runTimer.py` easily and let it run your job.

### Configuration
All the configuration is in `urlcheck/config.py`.

##### OTHER_INCLUDE_DOMAIN
This item will be *Abandoned* and it just services `SohuUrlCheck` class currently.

##### LOG_DIR
The catalog we store our log. The default is `logdir` under our project.

##### LOG_CONTENT_FMT
The log format that used by [logging](https://docs.python.org/2/library/logging.html).And the default is `%(asctime)s-%(message)s`.

##### LOG_FILENAME_FMT
The filename of log text. The default is `D_%Y-%m-%d_T%H%M`.

##### THREAD_NUMBER
The number of Thread. The default is `100`.

##### URL_TOTAL_NUM
The number of url we need check. The default is `1000`.

##### INTERVAL_EXC
The time interval when wen run in timer mode. The time unit is second and the default is `600`, namely ten minutes.
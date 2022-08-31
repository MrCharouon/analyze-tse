import os
path = (os.path.expanduser('~/.tsewl/'))
dir=(os.path.expanduser('/tmp/tsewl/'))
class directorycheck():
    try:
        os.chdir(path)
        # print("Current working directory: {0}".format(os.getcwd()))
    except FileNotFoundError:
        # print("Directory: {0} does not exist".format(path))
        os.mkdir(path)
    try:
        os.chdir(dir)
        # print("Current working directory: {0}".format(os.getcwd()))
    except FileNotFoundError:
        # print("Directory: {0} does not exist".format(path))
        os.mkdir(dir)
path_data_csv = (dir+ "data.csv")
path_data_db = (dir+ "data.db")
path_watch_csv = (dir+ "watch.csv")
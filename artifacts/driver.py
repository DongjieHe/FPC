#!/usr/bin/env python3
import os,sys, shutil

'''
Use FlowDroid/CleanDroid/FPC to analyze a set of Android applications.
The only argument should be provided is the path to the application.
The grammar for running this script is given below:
cmd := ./driver.py argumentList
argumentList := argument | argument argumentList
argument := -print | -out={OUTPUT-PATH} | -st={SLEEP-TIME} | -ds={SOLVER} | APP-PATH

When multiple output path, sleeping time, and solvers are specified, only the last occurence is used.
When multiple app paths are specified, all of them will be analyzed.
'''

# terminal colors
RESET = '\033[0m'
YELLOW = '\033[33m'
WHITE = '\033[37m'
GREEN = '\033[32m'
BOLD = '\033[1m'
RED = '\033[31m'

# global variables
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
JVMARG = '-Xmx200G'
FLOWDROID = 'soot-infoflow-cmd-jar-with-dependencies.jar'
PLATFORMS_DIR = 'android-platforms'
SOURCE_SINK_SPEC = 'SourcesAndSinks.txt'
RESULT_TIMEOUT = 7200
DATAFLOW_TIMEOUT = 10800
MAX_THREAD_NUM = 8
isPrint = False
SOLVER = None # 'FPC' # "GC"
OUTPUTPATH = 'output'
SLEEP_TIME = 1

def genCmd(app):
    args = ['java', JVMARG, '-jar', FLOWDROID]
    args += ['-a', os.path.join(app), '-p', PLATFORMS_DIR]
    args += ['-s', SOURCE_SINK_SPEC]
    args += ['--mergedexfiles']
    args += ['-rt', str(RESULT_TIMEOUT)]
    args += ['-dt', str(DATAFLOW_TIMEOUT)]
    args += ['-mt', str(MAX_THREAD_NUM)]
    args += ['-st', str(SLEEP_TIME)]
    outDir = os.path.join(CURRENT_DIR, OUTPUTPATH)
    if SOLVER is not None:
        args += ['-ds', SOLVER]
        outDir = os.path.join(CURRENT_DIR, OUTPUTPATH)
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    outlog = os.path.join(outDir, app.split("/")[-1][:-4] + ".log")
    print(outlog)
    if isPrint is False:
        if os.path.exists(outlog):
            print('old result found. skip this.')
            return None
        args += ['>', outlog, '2>&1']
    cmd = ' '.join(args)
    return cmd

def run(app):
    print(YELLOW + BOLD + 'Analyzing ' + RED + BOLD + app + YELLOW + BOLD + ' ...' + RESET)
    cmd = genCmd(app)
    if cmd is not None:
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    appPaths = []
    if "-print" in sys.argv:
        isPrint = True
    for arg in sys.argv:
        if arg.startswith("-out="):
            OUTPUTPATH = arg[len('-out='):]
        elif arg.startswith("-solver="):
            SOLVER = arg[len('-solver='):]
        elif arg.startswith("-st="):
            SLEEP_TIME = int(arg[len('-st='):])
        elif arg.endswith(".apk"):
            appPaths.append(arg)

    if not os.path.exists(OUTPUTPATH):
        os.mkdir(OUTPUTPATH)
    for appPath in appPaths:
        run(appPath)

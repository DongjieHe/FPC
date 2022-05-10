#!/usr/bin/env python6
import os,sys, shutil

'''
Use FlowDroid to analyze a single Android application.
The only argument is the path to the application.
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
JVMARG = '-Xmx220G'
FLOWDROID = 'soot-infoflow-cmd-jar-with-dependencies.jar'
PLATFORMS_DIR = 'android-platforms'
SOURCE_SINK_SPEC = 'SourcesAndSinks.txt'
OUTPUTPATH = 'output2'
RESULT_TIMEOUT = 1800
DATAFLOW_TIMEOUT = 18000
MAX_THREAD_NUM = 10
isPrint = True
collectMemory = False

def genCmd(app):
    args = ['java', JVMARG, '-jar', FLOWDROID]
    args += ['-a', os.path.join(app), '-p', PLATFORMS_DIR]
    args += ['-s', SOURCE_SINK_SPEC]
    args += ['--mergedexfiles']
    args += ['-rt', str(RESULT_TIMEOUT)]
    args += ['-dt', str(DATAFLOW_TIMEOUT)]
    args += ['-mt', str(MAX_THREAD_NUM)]
    if collectMemory:
        args += ['-sm']
    if not os.path.exists(os.path.join(CURRENT_DIR, OUTPUTPATH)):
        os.makedirs(os.path.join(CURRENT_DIR, OUTPUTPATH))
    output = os.path.join(CURRENT_DIR, OUTPUTPATH, app.split("/")[-1][:-4] + ".xml")
    # outlog = os.path.join(OUTPUTPATH, BENCHMARKS[app] + ".log")
    if not isPrint and os.path.exists(output):
        print('old result found. skip this.')
        return None
    elif not isPrint:
        args += ['-o', output]
    # if isPrint is True:
    #     args += ['>', outlog, '2>&1']
    cmd = ' '.join(args)
    return cmd

def run(app):
    print(YELLOW + BOLD + 'Analyzing ' + RED + BOLD + app + YELLOW + BOLD + ' ...' + RESET)
    cmd = genCmd(app)
    if cmd is not None:
        print(cmd)
        os.system(cmd)

if __name__ == '__main__':
    if not os.path.exists(OUTPUTPATH):
        os.mkdir(OUTPUTPATH)
    appPath = sys.argv[1]
    run(appPath)

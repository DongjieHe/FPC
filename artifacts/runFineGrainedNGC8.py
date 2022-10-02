#!/usr/bin/env python3
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
JVMARG = '-Xmx200G'
FLOWDROID = 'FPC8.jar'
PLATFORMS_DIR = 'android-platforms'
SOURCE_SINK_SPEC = 'SourcesAndSinks.txt'
OUTPUTPATH = 'FPCOUT8x'
RESULT_TIMEOUT = 7200
DATAFLOW_TIMEOUT = 72000
MAX_THREAD_NUM = 8
isPrint = True
# isPrint = False
SOLVER = 'FINEGRAIN'

def genCmd(app):
    args = ['java', JVMARG, '-jar', FLOWDROID]
    args += ['-a', os.path.join(app), '-p', PLATFORMS_DIR]
    args += ['-s', SOURCE_SINK_SPEC]
    args += ['--mergedexfiles']
    args += ['-rt', str(RESULT_TIMEOUT)]
    args += ['-dt', str(DATAFLOW_TIMEOUT)]
    args += ['-mt', str(MAX_THREAD_NUM)]
    outDir = os.path.join(CURRENT_DIR, OUTPUTPATH)
    if SOLVER is not None:
        args += ['-ds', SOLVER]
        outDir = os.path.join(CURRENT_DIR, OUTPUTPATH, SOLVER, 'NGC')
    if not os.path.exists(outDir):
        os.makedirs(outDir)
    output = os.path.join(outDir, app.split("/")[-1][:-4] + ".xml")
    outlog = os.path.join(outDir, app.split("/")[-1][:-4] + ".log")
    if not isPrint and os.path.exists(output):
        print('old result found. skip this.')
        return None
    elif not isPrint:
        args += ['-o', output]
    if isPrint is True:
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
    if not os.path.exists(OUTPUTPATH):
        os.mkdir(OUTPUTPATH)
    appPath = sys.argv[1]
    run(appPath)

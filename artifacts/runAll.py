#!/usr/bin/env python6
import os,sys, shutil

'''
Use FlowDroid to analyze all applications in FDroid.
'''

# terminal colors
RESET = '\033[0m'
YELLOW = '\033[33m'
WHITE = '\033[37m'
GREEN = '\033[32m'
BOLD = '\033[1m'
RED = '\033[31m'

CATEGORIES = [
    "connectivity", "development", "games", "graphics", "internet", "money", "multimedia", "navigation",
    "phone-sms", "reading", "science-education", "security", "sports-health", "system", "theming",
    "time", "writing"
]

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
isPrint = False
SOLVER = "ONLINE"

def genCmd(category, app):
    args = ['java', JVMARG, '-jar', FLOWDROID]
    args += ['-a', os.path.join(CURRENT_DIR, app), '-p', PLATFORMS_DIR]
    args += ['-s', SOURCE_SINK_SPEC]
    args += ['--mergedexfiles']
    args += ['-rt', str(RESULT_TIMEOUT)]
    args += ['-dt', str(DATAFLOW_TIMEOUT)]
    args += ['-mt', str(MAX_THREAD_NUM)]
    if SOLVER is not None:
        args += ['-ds', SOLVER]
    if not os.path.exists(os.path.join(CURRENT_DIR, OUTPUTPATH, category)):
        os.makedirs(os.path.join(CURRENT_DIR, OUTPUTPATH, category))
    output = os.path.join(CURRENT_DIR, OUTPUTPATH, category, app.split("/")[-1][:-4] + ".xml")
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

def run(category, app):
    cmd = genCmd(category, app)
    if cmd is not None:
        print(cmd)
        os.system(cmd)

def runAll():
    for category in CATEGORIES:
        for app in os.listdir(os.path.join(CURRENT_DIR, "benchmarks", "FDroid", category)):
            if app.endswith(".apk"):
                print(YELLOW + BOLD + 'Analyzing ' + RED + BOLD + app + YELLOW + BOLD + ' ...' + RESET)
                run(category, os.path.join("benchmarks", "FDroid", category, app))

if __name__ == '__main__':
    if not os.path.exists(OUTPUTPATH):
        os.mkdir(OUTPUTPATH)
    runAll()

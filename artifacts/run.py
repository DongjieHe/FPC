#!/usr/bin/env python3
import os,sys, shutil

# terminal colors
RESET = '\033[0m'
YELLOW = '\033[33m'
WHITE = '\033[37m'
GREEN = '\033[32m'
BOLD = '\033[1m'
RED = '\033[31m'

APPS = [
    "connectivity", "development", "games", "graphics", "internet", "money", "multimedia", "navigation",
    "phone-sms", "reading", "science-education", "security", "sports-health", "system", "theming",
    "time", "writing"
]

BENCHMARKS = {
    "connectivity": "benchmarks/FDroid/connectivity/be.uhasselt.privacypolice_13.apk",
    "development": "benchmarks/FDroid/development/com.biotstoiq.cryptix_23.apk",
    "games": "benchmarks/FDroid/games/cos.premy.mines_6.apk",
    "graphics": "benchmarks/FDroid/graphics/org.piwigo.android_102.apk",
    "internet": "benchmarks/FDroid/internet/au.com.wallaceit.reddinator_68.apk",
    "money": "benchmarks/FDroid/money/com.pvcodes.debtcalc_3.apk",
    "multimedia": "benchmarks/FDroid/multimedia/com.klee.volumelockr_8.apk",
    "navigation": "benchmarks/FDroid/navigation/com.icecondor.nest_20150402.apk",
    "phone-sms": "benchmarks/FDroid/phone-sms/com.dwak.lastcall_9.apk",
    "reading": "benchmarks/FDroid/reading/at.tomtasche.reader_172.apk",
    "science-education": "benchmarks/FDroid/science-education/ch.gassenarbeit.bern.your.rights_203.apk",
    "security": "benchmarks/FDroid/security/com.android.keepass_203.apk",
    "sports-health": "benchmarks/FDroid/sports-health/at.jclehner.rxdroid_9342.apk",
    "system": "benchmarks/FDroid/system/am.zoom.mlauncher_7.apk",
    "theming": "benchmarks/FDroid/theming/com.github.axet.darknessimmunity_28.apk",
    "time": "benchmarks/FDroid/time/tube.chikichiki.sako_15.apk",
    "writing": "benchmarks/FDroid/writing/ca.ramzan.delist_3.apk",
}

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

def genCmd(app):
    args = ['java', JVMARG, '-jar', FLOWDROID]
    args += ['-a', os.path.join(CURRENT_DIR, BENCHMARKS[app]), '-p', PLATFORMS_DIR]
    args += ['-s', SOURCE_SINK_SPEC]
    args += ['--mergedexfiles']
    args += ['-rt', str(RESULT_TIMEOUT)]
    args += ['-dt', str(DATAFLOW_TIMEOUT)]
    args += ['-mt', str(MAX_THREAD_NUM)]
    if SOLVER is not None:
        args += ['-ds', SOLVER]
    output = os.path.join(CURRENT_DIR, OUTPUTPATH, app + ".xml")
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
    cmd = genCmd(app)
    if cmd is not None:
        print(cmd)
        os.system(cmd)

def option(opt, des):
    return BOLD + YELLOW + opt + ' ' + '\t' + des + RESET + '\n'

OPTIONMESSAGE = 'The valid OPTIONs are:\n' \
                + option('-help|-h', 'print this message.') \
                + option('-fdhelp|-hfd', 'print help message of flowdroid.') \
                + option('-print', 'print the analyses results on screen.') \
                + option('-mem', 'run in collecting memory mode.') \
                + option('-clean', 'remove previous outputs.') \
                + option('<Benchmark>', 'specify benchmark.') \
                + option('-output=<out>', 'specify output path.') \
                + option('-all', 'run all analyses for specified benchmark(s) if ONLY benchmark(s) is specified')

if __name__ == '__main__':
    if '-help' in sys.argv or '-h' in sys.argv:
        sys.exit(OPTIONMESSAGE)
    if '-fdhelp' in sys.argv or '-hfd' in sys.argv:
        os.system('java -jar ' + FLOWDROID + ' -h') 
        sys.exit()
    if '-clean' in sys.argv:
        if os.path.exists(OUTPUTPATH):
            shutil.rmtree(OUTPUTPATH)
        sys.exit()
    if '-print' in sys.argv:
        isPrint = True
    if '-mem' in sys.argv:
        collectMemory = True
    benchmarks = []
    for arg in sys.argv:
        if arg in APPS:
            benchmarks.append(arg)
        elif arg.startswith('-output='):
            OUTPUTPATH = arg[len('-output='):]

    if "-all" in sys.argv:
        if len(benchmarks) == 0:
            benchmarks = APPS

    if len(benchmarks) == 0:
        sys.exit("benchmark(s) not specified." + OPTIONMESSAGE)
    if not os.path.exists(OUTPUTPATH):
        os.mkdir(OUTPUTPATH)

    for app in benchmarks:
        print(YELLOW + BOLD + 'Analyzing ' + RED + BOLD + app + YELLOW + BOLD + ' ...' + RESET)
        run(app)


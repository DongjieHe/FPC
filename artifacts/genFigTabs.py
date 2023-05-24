#!/usr/bin/python3
import os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
from prettytable import PrettyTable
from statistics import mean
from statistics import stdev
from OutlogParser import loadParserList
from OutlogParser import classifyByApkName
from BenchInfo import benchmarks
from BenchInfo import ben2name
from BenchInfo import ben2version
from brokenaxes import brokenaxes


class MarkDownTable:
    rows = []

    def __init__(self, head):
        self.head = head
        self.columnSize = len(head)

    def addRow(self, row):
        if len(row) != self.columnSize:
            print("invalid row size")
        else:
            self.rows.append(row)

    def getMDStr(self, row):
        ret = "| " + " | ".join(row) + " |"
        return ret

    def print(self):
        contents = []
        contents.append(self.getMDStr(self.head))
        content = "| "
        for i in range(self.columnSize):
            content += " --- |"
        contents.append(content)
        for ith in self.rows:
            contents.append(self.getMDStr(ith))
        print("\n".join(contents))


def speedupOverFd(fd, gc, fpc):
    print("generate speedupsOverFD.pdf ...")
    fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    fpcMap = classifyByApkName(fpc)
    fdovgc = []
    fdovfpc = []
    for k in benchmarks:
        fdElem = fdMap[k]
        gcElem = gcMap[k]
        fpcElem = fpcMap[k]
        fdStr = "OoT" if fdElem.to else "OoM" if fdElem.oom else str(
            fdElem.dataSolverTime)
        gcStr = "OoT" if gcElem.to else "OoM" if gcElem.oom else str(
            gcElem.dataSolverTime)
        fpcStr = "OoT" if fpcElem.to else "OoM" if fpcElem.oom else str(
            fpcElem.dataSolverTime)
        otom = ["OoT", "OoM"]
        if fdStr not in otom and gcStr not in otom and fpcStr not in otom:
            gcsu = fdElem.dataSolverTime * 1.0 / gcElem.dataSolverTime
            fdovgc.append(gcsu)
            fpcsu = fdElem.dataSolverTime * 1.0 / fpcElem.dataSolverTime
            fdovfpc.append(fpcsu)

    # draw the speedup bars
    lim = 8.0
    print("average speedup of FPC over FlowDroid:")
    print(np.prod(fdovfpc) ** (1.0 / len(fdovfpc)))
    print("average speedup of CleanDroid over FlowDroid:")
    print(np.prod(fdovgc) ** (1.0 / len(fdovgc)))
    ind = range(1, len(fdovfpc) + 1)
    ind1 = [i - 0.2 for i in ind]
    ind2 = [i + 0.2 for i in ind]
    width = 0.3  # the width of the bars: can also be len(x) sequence
    fig = plt.figure(figsize=(12, 4.5))
    bax = brokenaxes(ylims=((0.0, 18.0), (43.0, 48.0)),
                     wspace=0.05, hspace=0.05)
    p1 = bax.bar(ind1, fdovgc, width, color='gray', label='CleanDroid')
    p2 = bax.bar(ind2, fdovfpc, width, color='red', label='FPC')
    for i, v in enumerate(fdovgc):
        bax.text(ind1[i] - 0.12, v + 0.25, "{x:.1f}X".format(x=v), color="k" if v <
                 lim else "r", rotation=(90 if v < lim else 0), fontdict=None, size=8)
    # for i, v in enumerate(fdovfpc):
    #     print([ind2[i] - 0.12, v + 0.25])
    #     bax.text(ind2[i] - 0.12, v + 0.25, "{x:.1f}X".format(x=v), color="k" if v <
    #              lim else "r", rotation=(90 if v < lim else 0), fontdict=None, size=8)

    bax.axhline(y=1.0, linestyle='dashed')
    bax.set_xlim([0, len(fdovfpc) + 1])
    bax.set_xticks(ind, ind, weight='bold')
    bax.set_ylabel("Speedups over FlowDroid", weight='bold')
    bax.legend(loc='upper center', prop={'weight': 'bold'})
    plt.savefig('speedupsOverFD.pdf')
    # plt.show()


def buildTable(fd, gc, fpc):
    fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    fpcMap = classifyByApkName(fpc)
    integratedTable = PrettyTable()
    markdownTable = MarkDownTable(
        ["APK", "FlowDroid (s)", "CleanDroid (s)", "FPC (s)"])
    integratedTable.field_names = [
        "APK", "FlowDroid (s)", "CleanDroid (s)", "FPC (s)"]
    fdovgc = []
    fdovfpc = []
    for k in benchmarks:
        fdElem = fdMap[k]
        gcElem = gcMap[k]
        fpcElem = fpcMap[k]
        fdStr = "OoT" if fdElem.to else "OoM" if fdElem.oom else str(
            fdElem.dataSolverTime)
        gcStr = "OoT" if gcElem.to else "OoM" if gcElem.oom else str(
            gcElem.dataSolverTime)
        fpcStr = "OoT" if fpcElem.to else "OoM" if fpcElem.oom else str(
            fpcElem.dataSolverTime)
        otom = ["OoT", "OoM"]
        if fdStr not in otom and gcStr not in otom and fpcStr not in otom:
            gcsu = fdElem.dataSolverTime * 1.0 / gcElem.dataSolverTime
            fdovgc.append(gcsu)
            fpcsu = fdElem.dataSolverTime * 1.0 / fpcElem.dataSolverTime
            fdovfpc.append(fpcsu)
            gcStr = gcStr + "({v:.1f}X)".format(v=gcsu)
            fpcStr = fpcStr + "({v:.1f}X)".format(v=fpcsu)
        integratedTable.add_row([k, fdStr, gcStr, fpcStr])
        markdownTable.addRow([k, fdStr, gcStr, fpcStr])
    print(integratedTable)
    markdownTable.print()


def buildTexTable(gc, fpc):
    gcMap = classifyByApkName(gc)
    fpcMap = classifyByApkName(fpc)
    head = [
        r"\documentclass{article}",
        r"\usepackage{multicol, multirow, xcolor, adjustbox}",
        r"\begin{document}",
        r"\begin{table*}",
        r"\begin{adjustbox}{angle=90, max height=\textheight}",
        r"\centering",
        r"\begin{tabular}{c|l|r|r|r|r|r|r|r} \hline",
        r"\multicolumn{1}{c|}{\multirow{2}{*}{Group}} & \multicolumn{1}{|c|}{\multirow{2}{*}{APP}} & \multicolumn{1}{|c|}{\multirow{2}{*}{Version}} & \multicolumn{2}{c|}{Analysis Time (s)} & \multicolumn{2}{c|}{Memory Usage (GB)} & \multicolumn{2}{c}{$|PathEdge_{max}|$ (K)} \\ \cline{4-9}",
        r" & & & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c|}{\textsc{Fpc}} & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c|}{\textsc{Fpc}} & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c}{\textsc{Fpc}} \\ \hline   \hline",
    ]
    tail = [r"\end{tabular}",
            r"\end{adjustbox}",
            r"\end{table*}",
            r"\end{document}"]
    tableRows = []
    gcSpeedUps = []
    fpcSpeedUps = []
    gcMemPercs = []
    fpcMemPercs = []
    gcPEPercs = []
    fpcPEPercs = []

    for k in benchmarks:
        gc = gcMap[k]
        fpc = fpcMap[k]
        gct = "\\textcolor{blue}{OoT}" if gc.to else str(gc.dataSolverTime)
        gct = "-" if gc.oom else gct
        time = gc.dataSolverTime
        fpct = "\\textcolor{blue}{OoT}" if fpc.to else str(fpc.dataSolverTime)
        if gc.to == False and gc.oom == False and fpc.to == False:
            sd = time * 1.0 / fpc.dataSolverTime
            fpcSpeedUps.append(sd)
            fpct = fpct + " (" + "{:.1f}".format(sd) + "$\\times$)"
        gce = gc.recordedFWPECnt + gc.recordedBWPECnt
        fpce = fpc.recordedFWPECnt + fpc.recordedBWPECnt
        fpcep = ''
        if fpc.to == False and fpc.oom == False and gc.to == False and gc.oom == False:
            tmp = gce * 1.0 / fpce
            fpcPEPercs.append(tmp)
            fpcep = " (" + "{:.1f}".format(tmp) + "$\\times$)"

        gcm = "\\textcolor{red}{OoM}" if gc.oom else "{:.1f}".format(
            gc.maxmemory / 1024.0)
        if gc.to and not gc.oom:
            gcm = '-'
        fpcm = "\\textcolor{red}{OoM}" if fpc.oom else "{:.1f}".format(
            fpc.maxmemory / 1024.0)
        if fpc.to and not fpc.oom:
            fpcm = '-'
        fpcmp = ''
        if fpc.to == False and fpc.oom == False and gc.to == False and gc.oom == False:
            tmp = gc.maxmemory * 1.0 / fpc.maxmemory
            fpcMemPercs.append(tmp)
            fpcmp = " (" + "{:.1f}".format(tmp) + "$\\times$)"
        tableRows.append([ben2name[k], ben2version[k], gct, fpct,
                          gcm, fpcm + fpcmp,
                          "-" if gc.to or gc.oom else str(
                              "{:.1f}".format(gce / 1000.0)),
                          "-" if fpc.to or fpc.oom else str(
                              "{:.1f}".format(fpce / 1000.0)) + fpcep
                          ])

    gmAvgRow = ['Geometric Mean', '-', '-', '-',
                "{:.1f}".format(np.prod(fpcSpeedUps) **
                                (1.0 / len(fpcSpeedUps))) + "$\\times$", '-',
                "{:.1f}".format(np.prod(fpcMemPercs) **
                                (1.0 / len(fpcMemPercs))) + "$\\times$", '-',
                "{:.1f}".format(np.prod(fpcPEPercs) **
                                (1.0 / len(fpcPEPercs))) + "$\\times$"
                ]
    tableRows.append(gmAvgRow)

    content = "\n".join(head)
    content += "\n"
    for l in tableRows:
        if 'com.emn8.mobilem8.nativeapp.bk' in l:
            content += "\\multirow{-13}{*}{$\leq 3$ mins} &"
            content += "&".join(l)
            content += r"\\ \hline \hline"
        elif 'nya.miku.wishmaster' in l:
            content += "\\multirow{-12}{*}{$> 3$ mins} &"
            content += "&".join(l)
            content += r"\\ \hline \hline"
        elif 'com.github.axet.bookreader' in l:
            content += "\\multirow{-3}{*}{Unscalable} &"
            content += "&".join(l)
            content += r"\\ \hline \hline"
        elif 'Geometric Mean' in l:
            # do nothing
            content += "&".join(l)
            content += r"\\ \hline"
        else:
            content += "& "
            content += "&".join(l)
            content += r"\\ \cline{2-9}"
        content += "\n"
    content += "\n".join(tail)
    f = open("table1.tex", "w")
    f.write(content)
    f.close()
    print("table 1 is written into table1.tex")
    # print(content)


def adgEdgeOverPERatio(fpc):
    print("generate adgSize.pdf ...")
    fpcMap = classifyByApkName(fpc)
    ansList = []
    for k in benchmarks:
        fpc = fpcMap[k]
        if not fpc.to and not fpc.oom:
            tmp = fpc.adgEdgeCnt * 1.0 / \
                (fpc.forwardPECount + fpc.backwardPECount)
            ansList.append(tmp)
    print("average (GM) adge Edge Over PE ratio is %s" %
          np.prod(ansList) ** (1.0 / len(ansList)))
    ind = range(1, len(ansList) + 1)
    width = 0.5  # the width of the bars: can also be len(x) sequence
    plt.figure(figsize=(8, 2.5))
    p1 = plt.bar(ind, ansList, width, color='gray')
    plt.yticks(np.arange(0, 0.05, 0.01), weight='bold')
    plt.xlim([0, len(ansList) + 1])
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.xticks(ind, ind, weight='bold')
    plt.ylabel("ADG's #Edges /\n Processed #Path Edges", weight='bold')
    plt.savefig('adgSize.pdf')
    # plt.show()


def scatterPlotSpeedUpAndPE(gc, fpc):
    gcMap = classifyByApkName(gc)
    fpcMap = classifyByApkName(fpc)
    spList = []
    peList = []
    memList = []
    for k in benchmarks:
        gc = gcMap[k]
        fpc = fpcMap[k]
        if not gc.to and not gc.oom:
            speedUp = gc.dataSolverTime * 1.0 / fpc.dataSolverTime
            rcdPE = (gc.recordedFWPECnt + gc.recordedBWPECnt) * \
                1.0 / (fpc.recordedFWPECnt + fpc.recordedBWPECnt)
            memRatio = gc.maxmemory * 1.0 / fpc.maxmemory
            spList.append(speedUp)
            peList.append(rcdPE)
            memList.append(memRatio)
    print("generate tp.pdf ...")
    x = range(1, len(spList) + 1)
    plt.figure(figsize=(8, 2.5))
    plt.scatter(x, peList, c="r", alpha=0.5, marker='o',
                label="CleanDroid's $|PathEdge|_{max}$ / Fpc's $|PathEdge|_{max}$")
    plt.scatter(x, spList, c="k", alpha=0.5, marker='+',
                label="CleanDroid's Time / Fpc's Time")
    # print(peList)
    # print(spList)
    plt.xticks(x, x, weight='bold')
    plt.yticks(weight='bold')
    plt.legend(loc='upper left', prop={'weight': 'bold'})
    plt.savefig('tp.pdf')
    # plt.show()

    print("generate mp.pdf ...")
    plt.figure(figsize=(8, 2.5))
    plt.scatter(x, peList, c="r", alpha=0.5, marker='o',
                label="CleanDroid's $|PathEdge|_{max}$ / Fpc's $|PathEdge|_{max}$")
    plt.scatter(x, memList, c="k", alpha=0.5, marker='*',
                label="CleanDroid's Memory Usage / Fpc's Memory Usage")
    # print(peList)
    # print(memList)
    plt.xticks(x, x, weight='bold')
    ax = plt.gca()
    plt.yticks(weight='bold')
    plt.legend(loc='upper left', prop={'weight': 'bold'})
    plt.savefig('mp.pdf')
    # plt.show()

# merge three runs into one


def mergeRuns(run1, run2, run3, scaleOnly):
    run1Map = classifyByApkName(run1)
    run2Map = classifyByApkName(run2)
    run3Map = classifyByApkName(run3)
    ret = []
    filters = ['com.github.axet.bookreader_375',
               'org.openpetfoodfacts.scanner_2.9.8', 'bus.chio.wishmaster_1002']
    for k, v1 in run1Map.items():
        if scaleOnly and k in filters:
            continue
        v2 = run2Map[k]
        v3 = run3Map[k]
        if v1.oom or v1.to:
            ret.append(v1)
        else:
            vx = v1.clone()
            vx.leakCount = int(
                mean([v1.leakCount, v2.leakCount, v3.leakCount]))
            vx.resultsCount = int(
                mean([v1.resultsCount, v2.resultsCount, v3.resultsCount]))
            vx.dataSolverTime = int(
                mean([v1.dataSolverTime, v2.dataSolverTime, v3.dataSolverTime]))
            vx.maxmemory = int(
                mean([v1.maxmemory, v2.maxmemory, v3.maxmemory]))
            vx.forwardPECount = int(
                mean([v1.forwardPECount, v2.forwardPECount, v3.forwardPECount]))
            vx.backwardPECount = int(
                mean([v1.backwardPECount, v2.backwardPECount, v3.backwardPECount]))
            vx.recordedFWPECnt = int(
                mean([v1.recordedFWPECnt, v2.recordedFWPECnt, v3.recordedFWPECnt]))
            vx.recordedBWPECnt = int(
                mean([v1.recordedBWPECnt, v2.recordedBWPECnt, v3.recordedBWPECnt]))
            vx.adgEdgeCnt = int(
                mean([v1.adgEdgeCnt, v2.adgEdgeCnt, v3.adgEdgeCnt]))
            ret.append(vx)
    return ret

# compute dummyCnt/summayCnt and dummyCnt/#pathedge


def computeDummyRatio(fpc):
    fpcMap = classifyByApkName(fpc)
    dumSumRatio = []
    dumPERatio = []
    for k in benchmarks:
        parser = fpcMap[k]
        dumSumRatio.append(parser.dummySumCnt * 1.0 / parser.sumEdgeCnt)
        dumPERatio.append(parser.dummySumCnt * 1.0 /
                          (parser.forwardPECount + parser.backwardPECount))
    print("average (GM) redundancy-avoiding edge over all summary edge ratio is %s" %
          np.prod(dumSumRatio) ** (1.0 / len(dumSumRatio)))
    print("average (GM) redundancy-avoiding edge over all path edge ratio is %s" %
          np.prod(dumPERatio) ** (1.0 / len(dumPERatio)))


def intervalAnalysisOnSpeedUpsAndMemoryOverCleandroid(fpcDatas, cleandroidDatas):
    print("generate SpeedUpMemInterval.pdf ...")
    FPCMaps = []
    cleanDroidMaps = []
    speedUps = []
    memoryReductions = []
    for data in fpcDatas:
        FPCMaps.append(classifyByApkName(data))
        memoryReductions.append([])
        speedUps.append([])
    for data in cleandroidDatas:
        cleanDroidMaps.append(classifyByApkName(data))

    for k in benchmarks:
        if k in ['org.openpetfoodfacts.scanner_2.9.8', 'bus.chio.wishmaster_1002', 'com.github.axet.bookreader_375']:
            continue
        idx = 0
        for fpcMap in FPCMaps:
            baseline = cleanDroidMaps[idx][k]  # the base line is fixed.
            appx = fpcMap[k]
            speedUps[idx].append(baseline.dataSolverTime *
                                 1.0 / appx.dataSolverTime)
            # memoryReductions[idx].append(appx.maxmemory * 1.0 / baseline.maxmemory)
            memoryReductions[idx].append(
                baseline.maxmemory * 1.0 / appx.maxmemory)
            idx = idx + 1

    gmSpeedUpList = []
    for su in speedUps:
        gmSpeedUpList.append(np.prod(su) ** (1.0 / len(su)))
    gmMemReducList = []
    for mr in memoryReductions:
        gmMemReducList.append(np.prod(mr) ** (1.0 / len(mr)))

    print("memory reduction list (one for a sleep interval):")
    print(gmMemReducList)
    print("memory standard deviation is %s, mean is %s" %
          (stdev(gmMemReducList), mean(gmMemReducList)))
    print("speedup list (one for a sleep interval):")
    print(gmSpeedUpList)
    print("SpeedUps standard deviation is %s, mean is %s" %
          (stdev(gmSpeedUpList), mean(gmSpeedUpList)))

    x = range(1, len(gmSpeedUpList) + 1)
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    ax1.scatter(x, gmSpeedUpList, c='black', alpha=1.0, marker='x')
    ax1.set_ylim(1.0, 2.0)
    # gmGm1 = np.prod(gmSpeedUpList) ** (1.0 / len(gmSpeedUpList))
    gmGm1 = mean(gmSpeedUpList)
    ax1.axhline(y=gmGm1, linestyle='--', alpha=0.5, color='black')
    ax1.set_xlabel("GC intervals (s)", weight='bold')
    ax1.set_ylabel("Average Speedups", weight='bold', color='black')

    x = range(1, len(gmMemReducList) + 1)
    orange = "chocolate"
    ax2.scatter(x, gmMemReducList, c=orange, alpha=1.0, marker='+')
    ax2.set_ylim(1.1, 1.9)
    # gmGm2 = np.prod(gmMemReducList) ** (1.0 / len(gmMemReducList))
    gmGm2 = mean(gmMemReducList)
    ax2.axhline(y=gmGm2, color=orange, alpha=0.5, linestyle='--')
    ax2.set_ylabel("Average Memory Reduction", weight='bold', color=orange)

    plt.savefig('SpeedUpMemInterval.pdf')
    # plt.show()


def loadRun(runPath):
    fdRun = loadParserList(os.path.join(runPath, "FD1/"), "FlowDroid")
    fpcRun = loadParserList(os.path.join(runPath, "FPC1/"), "FPC")
    fpc2Run = loadParserList(os.path.join(runPath, "FPC2/"), "FPC")
    fpc3Run = loadParserList(os.path.join(runPath, "FPC3/"), "FPC")
    fpc4Run = loadParserList(os.path.join(runPath, "FPC4/"), "FPC")
    fpc5Run = loadParserList(os.path.join(runPath, "FPC5/"), "FPC")
    fpc6Run = loadParserList(os.path.join(runPath, "FPC6/"), "FPC")
    fpc7Run = loadParserList(os.path.join(runPath, "FPC7/"), "FPC")
    fpc8Run = loadParserList(os.path.join(runPath, "FPC8/"), "FPC")
    gcRun = loadParserList(os.path.join(runPath, "GC1"), "CleanDroid")
    gc2Run = loadParserList(os.path.join(runPath, "GC2/"), "CleanDroid")
    gc3Run = loadParserList(os.path.join(runPath, "GC3/"), "CleanDroid")
    gc4Run = loadParserList(os.path.join(runPath, "GC4/"), "CleanDroid")
    gc5Run = loadParserList(os.path.join(runPath, "GC5/"), "CleanDroid")
    gc6Run = loadParserList(os.path.join(runPath, "GC6/"), "CleanDroid")
    gc7Run = loadParserList(os.path.join(runPath, "GC7/"), "CleanDroid")
    gc8Run = loadParserList(os.path.join(runPath, "GC8/"), "CleanDroid")
    return fdRun, gcRun, gc2Run, gc3Run, gc4Run, gc5Run, gc6Run, gc7Run, gc8Run, fpcRun, fpc2Run, fpc3Run, fpc4Run, fpc5Run, fpc6Run, fpc7Run, fpc8Run

def filterBenchmarks(benchmarks, runLists):
    ret = []
    runMaps = []
    for run in runLists:
        run1Map = classifyByApkName(run)
        runMaps.append(run1Map)
    
    for app in benchmarks:
        flag = True
        for runMap in runMaps:
            if app not in runMap:
                flag = False
        if flag:
            ret.append(app)
    return ret

'''
The grammar for running this script:
cmd := ./genFigTabs.py argumentList
argumentList := argument | argument argumentList
argument := -sample | -out={RUN-PATH}
'''
useSample = False
OUTPUTPATH = None
if __name__ == '__main__':
    if "-print" in sys.argv:
        useSample = True
    for arg in sys.argv:
        if arg.startswith("-out="):
            OUTPUTPATH = arg[len('-out='):]
    if useSample or OUTPUTPATH is None:
        run1Path = "sample/run1"
        run2Path = "sample/run2"
        run3Path = "sample/run3"
    else:
        run1Path = OUTPUTPATH
        run2Path = OUTPUTPATH
        run3Path = OUTPUTPATH
    fdRun1, gcRun1, gc2Run1, gc3Run1, gc4Run1, gc5Run1, gc6Run1, gc7Run1, gc8Run1, fpcRun1, fpc2Run1, fpc3Run1, fpc4Run1, fpc5Run1, fpc6Run1, fpc7Run1, fpc8Run1 = loadRun(
        run1Path)
    fdRun2, gcRun2, gc2Run2, gc3Run2, gc4Run2, gc5Run2, gc6Run2, gc7Run2, gc8Run2, fpcRun2, fpc2Run2, fpc3Run2, fpc4Run2, fpc5Run2, fpc6Run2, fpc7Run2, fpc8Run2 = loadRun(
        run2Path)
    fdRun3, gcRun3, gc2Run3, gc3Run3, gc4Run3, gc5Run3, gc6Run3, gc7Run3, gc8Run3, fpcRun3, fpc2Run3, fpc3Run3, fpc4Run3, fpc5Run3, fpc6Run3, fpc7Run3, fpc8Run3 = loadRun(
        run3Path)

    fdMerge = mergeRuns(fdRun1, fdRun2, fdRun3, False)

    gcMerge = mergeRuns(gcRun1, gcRun2, gcRun3, False)
    gc2Merge = mergeRuns(gc2Run1, gc2Run2, gc2Run3, True)
    gc3Merge = mergeRuns(gc3Run1, gc3Run2, gc3Run3, True)
    gc4Merge = mergeRuns(gc4Run1, gc4Run2, gc4Run3, True)
    gc5Merge = mergeRuns(gc5Run1, gc5Run2, gc5Run3, True)
    gc6Merge = mergeRuns(gc6Run1, gc6Run2, gc6Run3, True)
    gc7Merge = mergeRuns(gc7Run1, gc7Run2, gc7Run3, True)
    gc8Merge = mergeRuns(gc8Run1, gc8Run2, gc8Run3, True)

    fpcMerge = mergeRuns(fpcRun1, fpcRun2, fpcRun3, False)
    fpc2Merge = mergeRuns(fpc2Run1, fpc2Run2, fpc2Run3, True)
    fpc3Merge = mergeRuns(fpc3Run1, fpc3Run2, fpc3Run3, True)
    fpc4Merge = mergeRuns(fpc4Run1, fpc4Run2, fpc4Run3, True)
    fpc5Merge = mergeRuns(fpc5Run1, fpc5Run2, fpc5Run3, True)
    fpc6Merge = mergeRuns(fpc6Run1, fpc6Run2, fpc6Run3, True)
    fpc7Merge = mergeRuns(fpc7Run1, fpc7Run2, fpc7Run3, True)
    fpc8Merge = mergeRuns(fpc8Run1, fpc8Run2, fpc8Run3, True)

    benchmarks = filterBenchmarks(benchmarks, [fdMerge, gcMerge, gc2Merge, gc3Merge, gc4Merge, gc5Merge, gc6Merge, gc7Merge, gc8Merge,
                                               fpcMerge, fpc2Merge, fpc3Merge, fpc4Merge, fpc5Merge, fpc6Merge, fpc7Merge, fpc8Merge])
    # buildTable(fdMerge, gcMerge, fpcMerge)
    buildTexTable(gcMerge, fpcMerge)
    adgEdgeOverPERatio(fpcMerge)
    computeDummyRatio(fpcMerge)
    scatterPlotSpeedUpAndPE(gcMerge, fpcMerge)
    speedupOverFd(fdMerge, gcMerge, fpcMerge)
    fpcList = [fpcMerge, fpc2Merge, fpc3Merge, fpc4Merge,
               fpc5Merge, fpc6Merge, fpc7Merge, fpc8Merge]
    gcList = [gcMerge, gc2Merge, gc3Merge, gc4Merge,
              gc5Merge, gc6Merge, gc7Merge, gc8Merge]
    intervalAnalysisOnSpeedUpsAndMemoryOverCleandroid(fpcList, gcList)

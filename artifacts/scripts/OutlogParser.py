#!/usr/bin/python3
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from prettytable import PrettyTable
from statistics import mean

class LogParser():
    def __init__(self):
        self.solver = ''
        self.apkName = ''
        self.leakCount = -1
        self.resultsCount = -1
        self.dataSolverTime = -1 # in seconds
        self.maxmemory = -1 # in MB
        self.forwardPECount = -1
        self.backwardPECount = -1
        self.recordedFWPECnt = -1
        self.recordedBWPECnt = -1
        self.adgEdgeCnt = -1
        self.sumEdgeCnt = -1
        self.dummySumCnt = -1
        self.oom = False
        self.to = False

    def clone(self):
        logParser = LogParser()
        logParser.solver = self.solver
        logParser.apkName = self.apkName
        logParser.leakCount = self.leakCount
        logParser.resultsCount = self.resultsCount
        logParser.dataSolverTime = self.dataSolverTime
        logParser.maxmemory = self.maxmemory
        logParser.forwardPECount = self.forwardPECount
        logParser.backwardPECount = self.backwardPECount
        logParser.recordedFWPECnt = self.recordedFWPECnt
        logParser.recordedBWPECnt = self.recordedBWPECnt
        logParser.adgEdgeCnt = self.adgEdgeCnt
        logParser.sumEdgeCnt = self.sumEdgeCnt
        logParser.dummySumCnt = self.dummySumCnt
        logParser.oom = self.oom
        logParser.to = self.to
        return logParser

    def parseAppName(self, file):
        self.apkName = file[file.rfind('/') + 1: -4]

    def parseLogFile(self, file, solver):
        self.solver = solver
        self.parseAppName(file)
        f = open(file)
        for line in f:
            ln = line.strip()
            if 'IFDS problem with' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                self.forwardPECount = tmp[0]
                self.backwardPECount = tmp[1]
                self.dataSolverTime = tmp[2]
                self.resultsCount = tmp[3]
            if 'Maximum memory consumption:' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                self.maxmemory = tmp[1]
            if 'Found' in ln and 'leaks' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                self.leakCount = tmp[0]
            if 'Recorded Maximum Path edges count is' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                if self.recordedFWPECnt == -1:
                    self.recordedFWPECnt = tmp[0]
                else:
                    self.recordedBWPECnt = tmp[0]
            if 'Running out of memory, solvers terminated' in ln:
                self.oom = True
            if 'Timeout reached, stopping the solvers' in ln:
                self.to = True
            if '#edges of forward Abstraction Dependency Graph:' in ln or '#edges of backward Abstraction Dependency Graph:' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                if self.adgEdgeCnt == -1:
                    self.adgEdgeCnt = tmp[0]
                else:
                    self.adgEdgeCnt += tmp[0]
            if '#dummy end summary edges of backward:' in ln or '#dummy end summary edges of forward:' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                if self.dummySumCnt == -1:
                    self.dummySumCnt = tmp[0]
                else:
                    self.dummySumCnt += tmp[0]
            if '#end summary edges of forward:' in ln or '#end summary edges of backward:' in ln:
                tmp = [int(s) for s in ln.split() if s.isdigit()]
                if self.sumEdgeCnt == -1:
                    self.sumEdgeCnt = tmp[0]
                else:
                    self.sumEdgeCnt += tmp[0]

        if self.maxmemory == -1:
            self.oom = True


# logDir should be an absolute path.
def loadParserList(logDir, solver):
    filter = []
    # filter = ['F-Droid', 'de.k3b.android.androFotoFinder_44', 'com.nianticlabs.pokemongo_0.139.3', 'com.microsoft.office.outlook_3.0.46', 
    #         'com.ichi2.anki_2.8.4', 'acr.browser.lightning_4.5.1', 'com.zeapo.pwdstore_10303']
    ret = []
    for r, _, fs in os.walk(logDir):
        for file in fs:
            path = os.path.join(r, file)
            parser = LogParser()
            parser.parseLogFile(path, solver)
            if parser.apkName not in filter:
                ret.append(parser)
    return ret

def classifyByApkName(parsersList):
    ret = {}
    for elem in parsersList:
        ret[elem.apkName] = elem
    return ret

def stats(parser):
    if parser.oom:
        return 'OoM'
    if parser.to:
        return 'TO'
    return 'SUCC'

def buildTable(gc, ngc):
    gcMap = classifyByApkName(gc)
    # agcMap = classifyByApkName(agc)
    ngcMap = classifyByApkName(ngc)

    # flowdroidTable = PrettyTable()
    # flowdroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#Leaks", "#Results", "Status"]
    # for k, v in sorted(fdMap.items()):
    #     flowdroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.backwardPECount, v.leakCount, v.resultsCount, stats(v)])
    # print(flowdroidTable)

    # cleandroidTable = PrettyTable()
    # cleandroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results", "Status"]
    # for k, v in sorted(gcMap.items()):
    #     cleandroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.backwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount, stats(v)])
    # print(cleandroidTable)

    # aggressiveFGTable = PrettyTable()
    # aggressiveFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(agcMap.items()):
    #     aggressiveFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.backwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(aggressiveFGTable)

    # normalFGTable = PrettyTable()
    # normalFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(ngcMap.items()):
    #     normalFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.backwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(normalFGTable)

    # integratedTable = PrettyTable()
    # integratedTable.field_names = ["APK", "FDT(s)", "MaxM(MB)", "#PE", "#Leaks", "#Results", "CDT(s)", "CDMaxM(MB)", "#CDRDPEs", "AGCT(s)", "AGCMaxM(MB)", "#AGCRDPEs", "NGCT(s)", "NGCMaxM(MB)", "#NGCRDPEs"]
    # for k, v in sorted(fdMap.items()):
    #     gcElem = gcMap[k]
    #     agcElem = agcMap[k]
    #     ngcElem = ngcMap[k]
    #     integratedTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.backwardPECount, v.leakCount, v.resultsCount,
    #                              gcElem.dataSolverTime, gcElem.maxmemory, gcElem.recordedFWPECnt + gcElem.recordedBWPECnt,
    #                              agcElem.dataSolverTime, agcElem.maxmemory, agcElem.recordedFWPECnt + agcElem.recordedBWPECnt,
    #                              ngcElem.dataSolverTime, ngcElem.maxmemory, ngcElem.recordedFWPECnt + ngcElem.recordedBWPECnt])
    # print(integratedTable)
    
    integratedTable = PrettyTable()
    integratedTable.field_names = ["APK", "CDT(s)", "NGCT(s)", "CDMaxM(MB)", "NGCMaxM(MB)", "#CDRDPEs", "#NGCRDPEs"]
    for k, v in sorted(gcMap.items(), key = lambda x : x[1].dataSolverTime):
        gcElem = gcMap[k]
        ngcElem = ngcMap[k]
        integratedTable.add_row([v.apkName, gcElem.dataSolverTime, ngcElem.dataSolverTime, 
                                 gcElem.maxmemory, ngcElem.maxmemory, 
                                 gcElem.recordedFWPECnt + gcElem.recordedBWPECnt,
                                 ngcElem.recordedFWPECnt + ngcElem.recordedBWPECnt])
    print(integratedTable)

benchmarks = [ 'com.github.yeriomin.dumbphoneassistant_5', 'org.csploit.android', 'com.ilm.sandwich_2.2.4f', 
                'com.kunzisoft.keepass.libre_2.5.0.0beta18', 'dk.jens.backup_0.3.4', 'org.gateshipone.odyssey_30',
               'com.alfray.timeriffic_10905', 'org.decsync.sparss.floss_1.13.4',  'com.github.axet.callrecorder_219', 
               'org.materialos.icons_2.1', 'com.app.Zensuren_1.21', 'name.myigel.fahrplan.eh17_1.33.16', 
               'com.emn8.mobilem8.nativeapp.bk_5.0.10', 'com.genonbeta.TrebleShot_98', 'com.microsoft.office.word_16.0.11425.20132', 
               'org.secuso.privacyfriendlytodolist_2.1',  'com.vonglasow.michael.satstat', 'com.igisw.openmoneybox.3.4.1.8',
               'com.kanedias.vanilla.metadata_5', 'org.secuso.privacyfriendlyweather_6', 'com.adobe.reader_19.2.1.9183', 
               'org.totschnig.myexpenses', 'org.fdroid.fdroid_1008000', 'org.lumicall.android_190', 'nya.miku.wishmaster_54',   
               'org.openpetfoodfacts.scanner_2.9.8', 'bus.chio.wishmaster_1002', 'com.github.axet.bookreader_375', 
               ]

def buildTexTable(gc, ngc):
    # fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    ngcMap = classifyByApkName(ngc)
    head = [
            r"\begin{table*}",
            r"\centering",
            r"\begin{tabular}{|l|r|r|r|r|r|r|r|} \hline",
            r"\multicolumn{1}{|c|}{\multirow{2}{*}{APP}} & \multicolumn{1}{|c|}{\multirow{2}{*}{Version}} & \multicolumn{2}{c|}{Analysis Time (s)} & \multicolumn{2}{c|}{Memory Usage (GB)} & \multicolumn{2}{c|}{\#Path Edges (K)} \\ \cline{3-8}",
            r" & & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c|}{\textsc{Fpc}} & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c|}{\textsc{Fpc}} & \multicolumn{1}{|c|}{\textsc{CleanDroid}} & \multicolumn{1}{|c|}{\textsc{Fpc}} \\ \hline",
            ]
    tail = [r"\end{tabular}",
            r"\end{table*}"]
    tableRows = []
    ben2name = {
        'bus.chio.wishmaster_1002': 'bus.chio.wishmaster',
        'com.adobe.reader_19.2.1.9183': 'com.adobe.reader',
        'com.alfray.timeriffic_10905': 'com.alfray.timeriffic',
        'com.app.Zensuren_1.21': 'com.app.Zensuren',
        'com.emn8.mobilem8.nativeapp.bk_5.0.10': 'com.emn8.mobilem8.nativeapp.bk',
        'com.genonbeta.TrebleShot_98': 'com.genonbeta.TrebleShot',
        'com.github.axet.bookreader_375': 'com.github.axet.bookreader',
        'com.github.axet.callrecorder_219': 'com.github.axet.callrecorder',
        'com.github.yeriomin.dumbphoneassistant_5': 'com.github.yeriomin.dumbphoneassistant',
        'com.igisw.openmoneybox.3.4.1.8': 'com.igisw.openmoneybox',
        'com.ilm.sandwich_2.2.4f': 'com.ilm.sandwich',
        'com.kanedias.vanilla.metadata_5': 'com.kanedias.vanilla.metadata',
        'com.kunzisoft.keepass.libre_2.5.0.0beta18': 'com.kunzisoft.keepass.libre',
        'com.microsoft.office.word_16.0.11425.20132': 'com.microsoft.office.word',
        'com.vonglasow.michael.satstat': 'com.vonglasow.michael.satstat',
        'dk.jens.backup_0.3.4': 'dk.jens.backup',
        'name.myigel.fahrplan.eh17_1.33.16': 'name.myigel.fahrplan.eh17',
        'nya.miku.wishmaster_54': 'nya.miku.wishmaster',
        'org.csploit.android': 'org.csploit.android',
        'org.totschnig.myexpenses': 'org.totschnig.myexpenses',
        'org.decsync.sparss.floss_1.13.4': 'org.decsync.sparss.floss',
        'org.fdroid.fdroid_1008000': 'org.fdroid.fdroid',
        'org.gateshipone.odyssey_30': 'org.gateshipone.odyssey',
        'org.lumicall.android_190': 'org.lumicall.android',
        'org.materialos.icons_2.1': 'org.materialos.icons',
        'org.openpetfoodfacts.scanner_2.9.8': 'org.openpetfoodfacts.scanner',
        'org.secuso.privacyfriendlytodolist_2.1': 'org.secuso.privacyfriendlytodolist',
        'org.secuso.privacyfriendlyweather_6': 'org.secuso.privacyfriendlyweather'
    }
    ben2version = {
        'bus.chio.wishmaster_1002': '1.0.2',
        'com.adobe.reader_19.2.1.9183': '19.2.1.9183',
        'com.alfray.timeriffic_10905': '1.09.05',
        'com.app.Zensuren_1.21': '1.21',
        'com.emn8.mobilem8.nativeapp.bk_5.0.10': '5.0.10',
        'com.genonbeta.TrebleShot_98': '1.4.2',
        'com.github.axet.bookreader_375': '1.12.14',
        'com.github.axet.callrecorder_219': '1.7.13',
        'com.github.yeriomin.dumbphoneassistant_5': '0.5',
        'com.igisw.openmoneybox.3.4.1.8': '3.4.1.8', # this is also the newer version than the one used in SparseDroid.
        'com.ilm.sandwich_2.2.4f': '2.2.4f',
        'com.kanedias.vanilla.metadata_5': '1.0.4',
        'com.kunzisoft.keepass.libre_2.5.0.0beta18': '2.5.0.0beta18',
        'com.microsoft.office.word_16.0.11425.20132': '16.0.11425.20132',
        'com.vonglasow.michael.satstat': '3.3',
        'dk.jens.backup_0.3.4': '0.3.4',
        'name.myigel.fahrplan.eh17_1.33.16': '1.33.16',
        'nya.miku.wishmaster_54': '1.5.0',
        'org.csploit.android': '1.6.5',
        'org.totschnig.myexpenses': '3.0.1.2',
        'org.decsync.sparss.floss_1.13.4': '1.13.4',
        'org.fdroid.fdroid_1008000': '1.8-alpha0',
        'org.gateshipone.odyssey_30': '1.1.18',
        'org.lumicall.android_190': '1.13.1',
        'org.materialos.icons_2.1': '2.1',
        'org.openpetfoodfacts.scanner_2.9.8': '2.9.8',
        'org.secuso.privacyfriendlytodolist_2.1': '2.1',
        'org.secuso.privacyfriendlyweather_6': '2.1.1'
    }
    gcSpeedUps = []
    ngcSpeedUps = []
    gcMemPercs = []
    ngcMemPercs = []
    gcPEPercs = []
    ngcPEPercs = []

    for k in benchmarks:
        # fd = fdMap[k]
        gc = gcMap[k]
        ngc = ngcMap[k]
        # fdt = "\\textcolor{blue}{OoT}" if fd.to else str(fd.dataSolverTime)
        # if fd.oom and not fd.to:
        #     fdt = '-'
        gct = "\\textcolor{blue}{OoT}" if gc.to else str(gc.dataSolverTime)
        gct = "-" if gc.oom else gct
        time = gc.dataSolverTime
        # if fd.to == False and fd.oom == False and gc.to == False:
        #     if gc.oom:
        #         gct = '-'
        #     else:
        #         sd = time * 1.0 / gc.dataSolverTime
        #         gcSpeedUps.append(sd)
        #         gct = gct + " (" + "{:.1f}".format(sd) + "$\\times$)"
        ngct = "\\textcolor{blue}{OoT}" if ngc.to else str(ngc.dataSolverTime)
        if gc.to == False and gc.oom == False and ngc.to == False:
            sd = time * 1.0 / ngc.dataSolverTime
            ngcSpeedUps.append(sd)
            ngct = ngct + " (" + "{:.1f}".format(sd) + "$\\times$)"
        # fde = fd.forwardPECount + fd.backwardPECount
        gce = gc.recordedFWPECnt + gc.recordedBWPECnt
        # gcep = ''
        # if gc.to == False and gc.oom == False and fd.to == False and fd.oom == False:
        #     tmp = gce * 1000.0 / fde
        #     gcPEPercs.append(tmp)
        #     gcep = " ("+ "{:.1f}".format(tmp) + "\\textperthousand)"
        ngce = ngc.recordedFWPECnt + ngc.recordedBWPECnt
        ngcep = ''
        if ngc.to == False and ngc.oom == False and gc.to == False and gc.oom == False:
            tmp = gce * 1.0 / ngce
            ngcPEPercs.append(tmp)
            ngcep = " ("+ "{:.1f}".format(tmp) + "$\\times$)"

        # fdm = "\\textcolor{red}{OoM}" if fd.oom else "{:.1f}".format(fd.maxmemory / 1024.0)
        # if fd.to and not fd.oom:
        #     fdm = '-'
        gcm = "\\textcolor{red}{OoM}" if gc.oom else "{:.1f}".format(gc.maxmemory / 1024.0)
        if gc.to and not gc.oom:
            gcm = '-'
        ngcm = "\\textcolor{red}{OoM}" if ngc.oom else "{:.1f}".format(ngc.maxmemory / 1024.0)
        if ngc.to and not ngc.oom:
            ngcm = '-'
        # gcmp = ''
        # if gc.to == False and gc.oom == False and fd.to == False and fd.oom == False:
        #     tmp = gc.maxmemory * 100.0 / fd.maxmemory
        #     gcMemPercs.append(tmp)
        #     gcmp = " ("+ "{:.1f}".format(tmp) + "\%)"
        ngcmp = ''
        if ngc.to == False and ngc.oom == False and gc.to == False and gc.oom == False:
            tmp = gc.maxmemory * 1.0 / ngc.maxmemory
            ngcMemPercs.append(tmp)
            ngcmp = " ("+ "{:.1f}".format(tmp) + "$\\times$)"
        tableRows.append([ben2name[k], ben2version[k], gct, ngct,
                          gcm, ngcm + ngcmp,
                          "-" if gc.to or gc.oom else str("{:.1f}".format(gce / 1000.0)),
                          "-" if ngc.to or ngc.oom else str("{:.1f}".format(ngce / 1000.0)) + ngcep
                        ])

    gmAvgRow = ['Geometric Mean', '-', '-',
                    "{:.1f}".format(np.prod(ngcSpeedUps) ** (1.0 / len(ngcSpeedUps))) + "$\\times$", '-',
                    "{:.1f}".format(np.prod(ngcMemPercs) ** (1.0 / len(ngcMemPercs))) + "$\\times$", '-',
                "{:.1f}".format(np.prod(ngcPEPercs) ** (1.0 / len(ngcPEPercs))) + "$\\times$"
                ]
    tableRows.append(gmAvgRow)

    content = "\n".join(head)
    content += "\n"
    for l in tableRows:
        content += "&".join(l)
        content += r"\\ \hline"
        content += "\n"
    content += "\n".join(tail)
    print(content)

def adgEdgeOverPERatio(ngc):
    ngcMap = classifyByApkName(ngc)
    ansList = []
    for k in benchmarks:
        ngc = ngcMap[k]
        if not ngc.to and not ngc.oom:
            # print(ngc.adgEdgeCnt, ngc.forwardPECount + ngc.backwardPECount)
            tmp = ngc.adgEdgeCnt * 1.0 / (ngc.forwardPECount + ngc.backwardPECount)
            ansList.append(tmp)
    print(ansList)
    print(np.prod(ansList) ** (1.0 / len(ansList)))
    ind = range(1, len(ansList) + 1)
    width = 0.5  # the width of the bars: can also be len(x) sequence
    plt.figure(figsize=(11, 4.2))
    # plt.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.2)
    # plt.hlines(0.01, 0, len(ansList) + 1, color='red', linestyle='dotted')
    p1 = plt.bar(ind, ansList, width, color='gray')
    plt.yticks(np.arange(0, 0.05, 0.01), weight='bold')
    plt.xlim([0, len(ansList) + 1] )
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.xticks(ind, ind, weight='bold')
    plt.ylabel("ADG's #Edges / Processed #Path Edges")
    # plt.show()
    plt.savefig('adgSize.pdf')

# benchmarks2 = [
#     # 'org.materialos.icons_2.1',
#     #            'com.app.Zensuren_1.21', 'name.myigel.fahrplan.eh17_1.33.16', 'com.github.axet.callrecorder_219',
#
#                'com.emn8.mobilem8.nativeapp.bk_5.0.10', 'com.microsoft.office.word_16.0.11425.20132', 'com.igisw.openmoneybox.3.4.1.8',
#                'org.secuso.privacyfriendlytodolist_2.1', 'com.genonbeta.TrebleShot_98', 'com.kanedias.vanilla.metadata_5',
#                'com.adobe.reader_19.2.1.9183', 'com.vonglasow.michael.satstat', 'org.secuso.privacyfriendlyweather_6',
#                'org.totschnig.myexpenses', 'nya.miku.wishmaster_54',  'org.fdroid.fdroid_1008000', 'org.lumicall.android_190',
#                'bus.chio.wishmaster_1002', 'com.github.axet.bookreader_375', 'org.openpetfoodfacts.scanner_2.9.8',
#                ]
def scatterPlotSpeedUpAndPE(gc, ngc):
    gcMap = classifyByApkName(gc)
    ngcMap = classifyByApkName(ngc)
    spList = []
    peList = []
    memList = []
    for k in benchmarks:
        gc = gcMap[k]
        ngc = ngcMap[k]
        if not gc.to and not gc.oom:
            speedUp = gc.dataSolverTime * 1.0 / ngc.dataSolverTime
            rcdPE = (gc.recordedFWPECnt + gc.recordedBWPECnt) * 1.0 / (ngc.recordedFWPECnt + ngc.recordedBWPECnt)
            memRatio = gc.maxmemory * 1.0/ ngc.maxmemory
            spList.append(speedUp)
            peList.append(rcdPE)
            memList.append(memRatio)
    # print(spList)
    # print(peList)
    # print(memList)
    x = range(1, len(spList) + 1)
    # plt.figure(figsize=(8,2.5))
    # plt.scatter(x, spList, c="k", alpha=0.5, marker='+', label="CleanDroid's Time / Fpc's Time")
    # plt.scatter(x, peList, c="r", alpha=0.5, marker='.', label="CleanDroid's #Path Edges / Fpc's #Path Edges")
    # plt.xticks(x, x)
    # plt.legend(loc='upper left')
    # plt.savefig('tp.pdf')
    # plt.show()

    plt.figure(figsize=(8,2.5))
    plt.scatter(x, memList, c="k", alpha=0.5, marker='*', label="CleanDroid's Memory / Fpc's Memory")
    plt.scatter(x, peList, c="r", alpha=0.5, marker='.', label="CleanDroid's #Path Edges / Fpc's #Path Edges")
    plt.xticks(x, x)
    plt.legend(loc='upper left')
    plt.savefig('mp.pdf')
    plt.show()


def ngcIntervalAnalysis(gc, ngc, ngc2, ngc3, ngc4, ngc5, ngc6, ngc7, ngc8):
    gcMap = classifyByApkName(gc)
    # ngc0Map = classifyByApkName(ngc0)
    ngcMap = classifyByApkName(ngc)
    ngc2Map = classifyByApkName(ngc2)
    ngc3Map = classifyByApkName(ngc3)
    ngc4Map = classifyByApkName(ngc4)
    ngc5Map = classifyByApkName(ngc5)
    ngc6Map = classifyByApkName(ngc6)
    ngc7Map = classifyByApkName(ngc7)
    ngc8Map = classifyByApkName(ngc8)
    # speedUps0 = []
    speedUps = []
    speedUps2 = []
    speedUps3 = []
    speedUps4 = []
    speedUps5 = []
    speedUps6 = []
    speedUps7 = []
    speedUps8 = []
    # memoryReductions0 = []
    memoryReductions = []
    memoryReductions2 = []
    memoryReductions3 = []
    memoryReductions4 = []
    memoryReductions5 = []
    memoryReductions6 = []
    memoryReductions7 = []
    memoryReductions8 = []
    for k in benchmarks:
        if k in ['org.openpetfoodfacts.scanner_2.9.8', 'bus.chio.wishmaster_1002', 'com.github.axet.bookreader_375']:
            continue
        appgc = gcMap[k]
        # appngc0 = ngc0Map[k]
        appngc = ngcMap[k]
        appngc2 = ngc2Map[k]
        appngc3 = ngc3Map[k]
        appngc4 = ngc4Map[k]
        appngc5 = ngc5Map[k]
        appngc6 = ngc6Map[k]
        appngc7 = ngc7Map[k]
        appngc8 = ngc8Map[k]
        # In case where interval = 0, FPC could not analyze this app successfully.
        if appgc.to or appgc.oom:
            continue
        # if k != "com.emn8.mobilem8.nativeapp.bk_5.0.10":
        #     print(k)
        #     speedUps0.append(appngc.dataSolverTime * 1.0 / appngc0.dataSolverTime)
        #     memoryReductions0.append(appngc0.maxmemory * 1.0 / appngc.maxmemory)
        speedUps2.append(appngc.dataSolverTime * 1.0 / appngc2.dataSolverTime)
        memoryReductions2.append(appngc2.maxmemory * 1.0 / appngc.maxmemory)
        speedUps3.append(appngc.dataSolverTime * 1.0 / appngc3.dataSolverTime)
        memoryReductions3.append(appngc3.maxmemory * 1.0 / appngc.maxmemory)
        speedUps4.append(appngc.dataSolverTime * 1.0 / appngc4.dataSolverTime)
        memoryReductions4.append(appngc4.maxmemory * 1.0 / appngc.maxmemory)
        speedUps5.append(appngc.dataSolverTime * 1.0 / appngc5.dataSolverTime)
        memoryReductions5.append(appngc5.maxmemory * 1.0 / appngc.maxmemory)
        speedUps6.append(appngc.dataSolverTime * 1.0 / appngc6.dataSolverTime)
        memoryReductions6.append(appngc6.maxmemory * 1.0 / appngc.maxmemory)
        speedUps7.append(appngc.dataSolverTime * 1.0 / appngc7.dataSolverTime)
        memoryReductions7.append(appngc7.maxmemory * 1.0 / appngc.maxmemory)
        speedUps8.append(appngc.dataSolverTime * 1.0 / appngc8.dataSolverTime)
        memoryReductions8.append(appngc8.maxmemory * 1.0 / appngc.maxmemory)
    gmSpeedUpList = []
    gmMemReducList = []
    # gmSpeedUpList.append(np.prod(speedUps0) ** (1.0 / len(speedUps0)))
    # gmMemReducList.append(np.prod(memoryReductions0) ** (1.0 / len(memoryReductions0)))
    gmSpeedUpList.append(1.0)
    gmMemReducList.append(1.0)
    # gmSpeedUpList.append(np.prod(speedUps) ** (1.0 / len(speedUps)))
    # gmMemReducList.append(np.prod(memoryReductions) ** (1.0 / len(memoryReductions)))
    gmSpeedUpList.append(np.prod(speedUps2) ** (1.0 / len(speedUps2)))
    gmMemReducList.append(np.prod(memoryReductions2) ** (1.0 / len(memoryReductions2)))
    gmSpeedUpList.append(np.prod(speedUps3) ** (1.0 / len(speedUps3)))
    gmMemReducList.append(np.prod(memoryReductions3) ** (1.0 / len(memoryReductions3)))
    gmSpeedUpList.append(np.prod(speedUps4) ** (1.0 / len(speedUps4)))
    gmMemReducList.append(np.prod(memoryReductions4) ** (1.0 / len(memoryReductions4)))
    gmSpeedUpList.append(np.prod(speedUps5) ** (1.0 / len(speedUps5)))
    gmMemReducList.append(np.prod(memoryReductions5) ** (1.0 / len(memoryReductions5)))
    gmSpeedUpList.append(np.prod(speedUps6) ** (1.0 / len(speedUps6)))
    gmMemReducList.append(np.prod(memoryReductions6) ** (1.0 / len(memoryReductions6)))
    gmSpeedUpList.append(np.prod(speedUps7) ** (1.0 / len(speedUps7)))
    gmMemReducList.append(np.prod(memoryReductions7) ** (1.0 / len(memoryReductions7)))
    gmSpeedUpList.append(np.prod(speedUps8) ** (1.0 / len(speedUps8)))
    gmMemReducList.append(np.prod(memoryReductions8) ** (1.0 / len(memoryReductions8)))
    # print(speedUps0)
    # print(memoryReductions0)
    print(gmSpeedUpList)
    print(gmMemReducList)
    # x = range(1, len(gmSpeedUpList) + 1)
    # plt.figure(figsize=(8, 4.0))
    # plt.yticks(np.arange(0.6, 1.6, 0.1), weight='bold')
    # plt.scatter(x, gmSpeedUpList, c="b", alpha=0.5, marker='x')
    # plt.ylim((0.8,1.2))
    # plt.xlabel("Collecting intervals (s)", weight='bold')
    # plt.ylabel("Average Speedups", weight='bold')
    # plt.savefig('SpeedupInterval.pdf')
    # plt.show()

    x = range(1, len(gmMemReducList) + 1)
    plt.figure(figsize=(8, 4.0))
    plt.yticks(np.arange(0, 1.5, 0.05), weight='bold')
    plt.scatter(x, gmMemReducList, c="b", alpha=0.5, marker='x')
    plt.ylim((0.85, 1.1))
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1))
    plt.xlabel("Collecting intervals (s)")
    plt.ylabel("Average Memory Consumption")
    plt.savefig('MemInterval.pdf')
    plt.show()


# merge three runs into one
def mergeRuns(run1, run2, run3):
    run1Map = classifyByApkName(run1)
    run2Map = classifyByApkName(run2)
    run3Map = classifyByApkName(run3)
    ret = []
    for k, v1 in run1Map.items():
        v2 = run2Map[k]
        v3 = run3Map[k]
        if v1.oom or v1.to:
            ret.append(v1)
        else:
            vx = v1.clone()
            vx.leakCount = int(mean([v1.leakCount, v2.leakCount, v3.leakCount]))
            vx.resultsCount = int(mean([v1.resultsCount, v2.resultsCount, v3.resultsCount]))
            vx.dataSolverTime = int(mean([v1.dataSolverTime, v2.dataSolverTime, v3.dataSolverTime]))
            vx.maxmemory = int(mean([v1.maxmemory, v2.maxmemory, v3.maxmemory]))
            vx.forwardPECount = int(mean([v1.forwardPECount, v2.forwardPECount, v3.forwardPECount]))
            vx.backwardPECount = int(mean([v1.backwardPECount, v2.backwardPECount, v3.backwardPECount]))
            vx.recordedFWPECnt = int(mean([v1.recordedFWPECnt, v2.recordedFWPECnt, v3.recordedFWPECnt]))
            vx.recordedBWPECnt = int(mean([v1.recordedBWPECnt, v2.recordedBWPECnt, v3.recordedBWPECnt]))
            vx.adgEdgeCnt = int(mean([v1.adgEdgeCnt, v2.adgEdgeCnt, v3.adgEdgeCnt]))
            ret.append(vx)
    return ret

# compute dummyCnt/summayCnt and dummyCnt/#pathedge
def computeDummyRatio(ngc):
    ngcMap = classifyByApkName(ngc)
    dumSumRatio = []
    dumPERatio = []
    for k in benchmarks:
        parser = ngcMap[k]
        dumSumRatio.append(parser.dummySumCnt * 1.0 / parser.sumEdgeCnt)
        dumPERatio.append(parser.dummySumCnt * 1.0 / (parser.forwardPECount + parser.backwardPECount))
        print(parser.forwardPECount + parser.backwardPECount)
    print(np.prod(dumSumRatio) ** (1.0 / len(dumSumRatio)))
    print(np.prod(dumPERatio) ** (1.0 / len(dumPERatio)))

if __name__ == '__main__':
    gcRun4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/GC", "CleanDroid")
    gcRun5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/GC", "CleanDroid")
    gcRun6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/GC", "CleanDroid")
    gcMerge = mergeRuns(gcRun4, gcRun5, gcRun6)
    ngcRun4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FINEGRAIN/", "FPC")
    ngcRun5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FINEGRAIN/", "FPC")
    ngcRun6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FINEGRAIN/", "FPC")
    ngcMerge = mergeRuns(ngcRun4, ngcRun5, ngcRun6)
    # ngc0Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC0/FINEGRAIN/", "NGC")
    ngc2Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC2/FINEGRAIN/", "NGC")
    ngc3Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC3/FINEGRAIN/", "NGC")
    ngc4Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC4/FINEGRAIN/", "NGC")
    ngc5Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC5/FINEGRAIN/", "NGC")
    ngc6Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC6/FINEGRAIN/", "NGC")
    ngc7Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC7/FINEGRAIN/", "NGC")
    ngc8Run4 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run4/FPC8/FINEGRAIN/", "NGC")

    ngc2Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC2/FINEGRAIN/", "NGC")
    ngc3Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC3/FINEGRAIN/", "NGC")
    ngc4Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC4/FINEGRAIN/", "NGC")
    ngc5Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC5/FINEGRAIN/", "NGC")
    ngc6Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC6/FINEGRAIN/", "NGC")
    ngc7Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC7/FINEGRAIN/", "NGC")
    ngc8Run5 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run5/FPC8/FINEGRAIN/", "NGC")

    ngc2Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC2/FINEGRAIN/", "NGC")
    ngc3Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC3/FINEGRAIN/", "NGC")
    ngc4Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC4/FINEGRAIN/", "NGC")
    ngc5Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC5/FINEGRAIN/", "NGC")
    ngc6Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC6/FINEGRAIN/", "NGC")
    ngc7Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC7/FINEGRAIN/", "NGC")
    ngc8Run6 = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/run6/FPC8/FINEGRAIN/", "NGC")
    # buildTable(gcMerge, ngcMerge)
    # buildTable(ngc8, ngcMerge)
    # buildTexTable(gcMerge, ngcMerge)
    # adgEdgeOverPERatio(ngcMerge)
    # computeDummyRatio(ngcMerge)
    # ngcIntervalAnalysis(gcMerge, ngcMerge, ngc2Run4, ngc3Run4, ngc4Run4, ngc5Run4, ngc6Run4, ngc7Run4, ngc8Run4)
    # ngcIntervalAnalysis(gcMerge, ngcMerge, ngc2Run5, ngc3Run5, ngc4Run5, ngc5Run5, ngc6Run5, ngc7Run5, ngc8Run5)
    ngcIntervalAnalysis(gcMerge, ngcMerge, ngc2Run6, ngc3Run6, ngc4Run6, ngc5Run6, ngc6Run6, ngc7Run6, ngc8Run6)
    # scatterPlotSpeedUpAndPE(gcMerge, ngcMerge)


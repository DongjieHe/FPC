#!/usr/bin/python3
import os
import numpy as np
from prettytable import PrettyTable

class LogParser():
    def __init__(self):
        self.solver = ''
        self.apkName = ''
        self.leakCount = -1
        self.resultsCount = -1
        self.dataSolverTime = -1 # in seconds
        self.maxmemory = -1 # in MB
        self.forwardPECount = -1
        self.barwardPECount = -1
        self.recordedFWPECnt = -1
        self.recordedBWPECnt = -1
        self.oom = False
        self.to = False

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
                self.barwardPECount = tmp[1]
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

# logDir should be an absolute path.
def loadParserList(logDir, solver):
    filter = ['F-Droid', 'de.k3b.android.androFotoFinder_44', 'com.nianticlabs.pokemongo_0.139.3', 'com.microsoft.office.outlook_3.0.46', 
            'com.ichi2.anki_2.8.4', 'acr.browser.lightning_4.5.1', 'com.zeapo.pwdstore_10303']
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

def buildTable(fd, gc, ngc):
    fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    # agcMap = classifyByApkName(agc)
    ngcMap = classifyByApkName(ngc)

    # flowdroidTable = PrettyTable()
    # flowdroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#Leaks", "#Results", "Status"]
    # for k, v in sorted(fdMap.items()):
    #     flowdroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.leakCount, v.resultsCount, stats(v)])
    # print(flowdroidTable)

    # cleandroidTable = PrettyTable()
    # cleandroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results", "Status"]
    # for k, v in sorted(gcMap.items()):
    #     cleandroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount, stats(v)])
    # print(cleandroidTable)

    # aggressiveFGTable = PrettyTable()
    # aggressiveFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(agcMap.items()):
    #     aggressiveFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(aggressiveFGTable)

    normalFGTable = PrettyTable()
    normalFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    for k, v in sorted(ngcMap.items()):
        normalFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    print(normalFGTable)

    # integratedTable = PrettyTable()
    # integratedTable.field_names = ["APK", "FDT(s)", "MaxM(MB)", "#PE", "#Leaks", "#Results", "CDT(s)", "CDMaxM(MB)", "#CDRDPEs", "AGCT(s)", "AGCMaxM(MB)", "#AGCRDPEs", "NGCT(s)", "NGCMaxM(MB)", "#NGCRDPEs"]
    # for k, v in sorted(fdMap.items()):
    #     gcElem = gcMap[k]
    #     agcElem = agcMap[k]
    #     ngcElem = ngcMap[k]
    #     integratedTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.leakCount, v.resultsCount,
    #                              gcElem.dataSolverTime, gcElem.maxmemory, gcElem.recordedFWPECnt + gcElem.recordedBWPECnt,
    #                              agcElem.dataSolverTime, agcElem.maxmemory, agcElem.recordedFWPECnt + agcElem.recordedBWPECnt,
    #                              ngcElem.dataSolverTime, ngcElem.maxmemory, ngcElem.recordedFWPECnt + ngcElem.recordedBWPECnt])
    # print(integratedTable)
    
    integratedTable = PrettyTable()
    integratedTable.field_names = ["APK", "FDT(s)", "MaxM(MB)", "#PE",  "CDT(s)", "CDMaxM(MB)", "#CDRDPEs", "NGCT(s)", "NGCMaxM(MB)", "#NGCRDPEs"]
    for k, v in sorted(fdMap.items()):
        gcElem = gcMap[k]
        ngcElem = ngcMap[k]
        integratedTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount,
                                 gcElem.dataSolverTime, gcElem.maxmemory, gcElem.recordedFWPECnt + gcElem.recordedBWPECnt,
                                 ngcElem.dataSolverTime, ngcElem.maxmemory, ngcElem.recordedFWPECnt + ngcElem.recordedBWPECnt])
    print(integratedTable)

def buildTexTable(fd, gc, ngc): 
    fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    ngcMap = classifyByApkName(ngc)
    head = [
            r"\begin{table*}",
            r"\centering",
            r"\begin{tabular}{|l|r|r|r|r|r|r|r|r|r|r|} \hline",
            r"\multicolumn{1}{|c|}{\multirow{2}{*}{APP}} & \multirow{2}{*}{Version} & \multicolumn{3}{c|}{Analysis Time (s)} & \multicolumn{3}{c|}{Memory Usage (GB)} & \multicolumn{3}{c|}{\#Path Edges (K)} \\ \cline{3-11}",
            r" & & \textsc{FlowDroid} & \textsc{CleanDroid} & \textsc{Fpc} & \textsc{FlowDroid} & \textsc{CleanDroid} & \textsc{Fpc} & \textsc{FlowDroid} & \textsc{CleanDroid} & \textsc{Fpc} \\ \hline",
            ]
    tail = [r"\end{tabular}",
            r"\end{table*}"]
    tableRows = []
    benchmarks = [ 'com.ilm.sandwich_2.2.4f', 'com.github.yeriomin.dumbphoneassistant_5', 'dk.jens.backup_0.3.4',
                   'org.csploit.android', 'com.kunzisoft.keepass.libre_2.5.0.0beta18', 'org.gateshipone.odyssey_30',
                   'org.decsync.sparss.floss_1.13.4', 'com.alfray.timeriffic_10905', 'org.materialos.icons_2.1',
                  'com.app.Zensuren_1.21', 'name.myigel.fahrplan.eh17_1.33.16', 'com.github.axet.callrecorder_219',
                   'com.emn8.mobilem8.nativeapp.bk_5.0.10', 'com.microsoft.office.word_16.0.11425.20132', 'com.igisw.openmoneybox.3.4.1.8',
                  'org.secuso.privacyfriendlytodolist_2.1', 'com.genonbeta.TrebleShot_98', 'com.kanedias.vanilla.metadata_5',
                   'com.adobe.reader_19.2.1.9183', 'com.vonglasow.michael.satstat', 'org.secuso.privacyfriendlyweather_6',
                   'org.totschnig.myexpenses', 'nya.miku.wishmaster_54',  'org.fdroid.fdroid_1008000', 'org.lumicall.android_190',
                   'bus.chio.wishmaster_1002', 'com.github.axet.bookreader_375', 'org.openpetfoodfacts.scanner_2.9.8',
            ]
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
        fd = fdMap[k]
        gc = gcMap[k]
        ngc = ngcMap[k]
        fdt = "\\textcolor{blue}{OoT}" if fd.to else str(fd.dataSolverTime)
        if fd.oom and not fd.to:
            fdt = '-'
        gct = "\\textcolor{blue}{OoT}" if gc.to else str(gc.dataSolverTime)
        time = fd.dataSolverTime
        if fd.to == False and fd.oom == False and gc.to == False:
            if gc.oom:
                gct = '-'
            else:
                sd = time * 1.0 / gc.dataSolverTime
                gcSpeedUps.append(sd)
                gct = gct + " (" + "{:.1f}".format(sd) + "$\\times$)"
        ngct = "\\textcolor{blue}{OoT}" if ngc.to else str(ngc.dataSolverTime)
        if fd.to == False and fd.oom == False and ngc.to == False:
            sd = time * 1.0 / ngc.dataSolverTime
            ngcSpeedUps.append(sd)
            ngct = ngct + " (" + "{:.1f}".format(sd) + "$\\times$)"
        fde = fd.forwardPECount + fd.barwardPECount
        gce = gc.recordedFWPECnt + gc.recordedBWPECnt
        gcep = ''
        if gc.to == False and gc.oom == False and fd.to == False and fd.oom == False:
            tmp = gce * 1000.0 / fde
            gcPEPercs.append(tmp)
            gcep = " ("+ "{:.1f}".format(tmp) + "\\textperthousand)"
        ngce = ngc.recordedFWPECnt + ngc.recordedBWPECnt
        ngcep = ''
        if ngc.to == False and ngc.oom == False and fd.to == False and fd.oom == False:
            tmp = ngce * 1000.0 / fde
            ngcPEPercs.append(tmp)
            ngcep = " ("+ "{:.1f}".format(tmp) + "\\textperthousand)"

        fdm = "\\textcolor{red}{OoM}" if fd.oom else "{:.1f}".format(fd.maxmemory / 1024.0)
        if fd.to and not fd.oom:
            fdm = '-'
        gcm = "\\textcolor{red}{OoM}" if gc.oom else "{:.1f}".format(gc.maxmemory / 1024.0)
        if gc.to and not gc.oom:
            gcm = '-'
        ngcm = "\\textcolor{red}{OoM}" if ngc.oom else "{:.1f}".format(ngc.maxmemory / 1024.0)
        if ngc.to and not ngc.oom:
            ngcm = '-'
        gcmp = ''
        if gc.to == False and gc.oom == False and fd.to == False and fd.oom == False:
            tmp = gc.maxmemory * 100.0 / fd.maxmemory
            gcMemPercs.append(tmp)
            gcmp = " ("+ "{:.1f}".format(tmp) + "\%)"
        ngcmp = ''
        if ngc.to == False and ngc.oom == False and fd.to == False and fd.oom == False:
            tmp = ngc.maxmemory * 100.0 / fd.maxmemory
            ngcMemPercs.append(tmp)
            ngcmp = " ("+ "{:.1f}".format(tmp) + "\%)"
        tableRows.append([ben2name[k], ben2version[k], fdt, gct, ngct,
                          fdm, gcm + gcmp, ngcm + ngcmp,
                          "-" if fd.to or fd.oom else str("{:.1f}".format(fde / 1000.0)),
                          "-" if gc.to or gc.oom else str("{:.1f}".format(gce / 1000.0)) + gcep,
                          "-" if ngc.to or ngc.oom else str("{:.1f}".format(ngce / 1000.0)) + ngcep
                        ])

    gmAvgRow = ['Geometric Mean', '-', '-', "{:.1f}".format(np.prod(gcSpeedUps) ** (1.0 / len(gcSpeedUps))) + "$\\times$",
                    "{:.1f}".format(np.prod(ngcSpeedUps) ** (1.0 / len(ngcSpeedUps))) + "$\\times$", '-',
                    "{:.1f}".format(np.prod(gcMemPercs) ** (1.0 / len(gcMemPercs))) + "\%",
                    "{:.1f}".format(np.prod(ngcMemPercs) ** (1.0 / len(ngcMemPercs))) + "\%", '-',
                "{:.1f}".format(np.prod(gcPEPercs) ** (1.0 / len(gcPEPercs))) + "\\textperthousand",
                "{:.1f}".format(np.prod(ngcPEPercs) ** (1.0 / len(ngcPEPercs))) + "\\textperthousand"
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



if __name__ == '__main__':
    fd = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout2/FlowDroid", "FlowDroid")
    gc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout2/GC", "CleanDroid")
    # agc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/AGC/", "AGC")
    ngc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout2/FINEGRAIN/NGC/", "NGC")
    # buildTable(fd, gc, ngc)
    buildTexTable(fd, gc, ngc)


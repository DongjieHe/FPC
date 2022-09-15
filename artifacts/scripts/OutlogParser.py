#!/usr/bin/python3
import os
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
            r"\begin{table}",
            r"\centering",
            r"\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|} \hline",
            r"\multirow{2}{*}{APP} & \multicolumn{3}{c}{Analysis Time (s)} & \multicolumn{3}{c}{Memory Usage (MB)} & \multicolumn{3}{c}{\#Path Edges} \\ \hline",
            r" & FlowDroid & CleanDroid & FPC & FlowDroid & CleanDroid & FPC & FlowDroid & CleanDroid & FPC \\ \hline",
            ]
    tail = [r"\end{tabular}"
            r"\end{table}"]
    tableRows = []
    benchmarks = ['dk.jens.backup_0.3.4', 'org.csploit.android', 'bus.chio.wishmaster_1002']
    for k in benchmarks:
        fd = fdMap[k]
        gc = gcMap[k]
        ngc = ngcMap[k]
        tableRows.append([k, str(fd.dataSolverTime), str(gc.dataSolverTime), str(ngc.dataSolverTime), str(fd.maxmemory), str(gc.maxmemory), str(ngc.maxmemory), 
            str(fd.forwardPECount + fd.barwardPECount), str(gc.recordedFWPECnt + gc.recordedBWPECnt), str(ngc.recordedFWPECnt + ngc.recordedBWPECnt)])
    content = "\n".join(head)
    for l in tableRows:
        content += "&".join(l)
        content += r"\\ \hline"
    content += "\n".join(tail)
    print(content)



if __name__ == '__main__':
    fd = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FlowDroid", "FlowDroid")
    gc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/GC", "CleanDroid")
    # agc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/AGC/", "AGC")
    ngc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/NGC/", "NGC")
    # buildTable(fd, gc, ngc)
    buildTexTable(fd, gc, ngc)


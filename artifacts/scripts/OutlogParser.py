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

# logDir should be an absolute path.
def loadParserList(logDir, solver):
    ret = []
    for r, _, fs in os.walk(logDir):
        for file in fs:
            path = os.path.join(r, file)
            parser = LogParser()
            parser.parseLogFile(path, solver)
            ret.append(parser)
    return ret

def classifyByApkName(parsersList):
    ret = {}
    for elem in parsersList:
        ret[elem.apkName] = elem
    return ret

def buildTable(fd, gc, agc, ngc):
    fdMap = classifyByApkName(fd)
    gcMap = classifyByApkName(gc)
    agcMap = classifyByApkName(agc)
    ngcMap = classifyByApkName(ngc)

    # flowdroidTable = PrettyTable()
    # flowdroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#Leaks", "#Results"]
    # for k, v in sorted(fdMap.items()):
    #     flowdroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.leakCount, v.resultsCount])
    # print(flowdroidTable)

    # cleandroidTable = PrettyTable()
    # cleandroidTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(gcMap.items()):
    #     cleandroidTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(cleandroidTable)

    # aggressiveFGTable = PrettyTable()
    # aggressiveFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(agcMap.items()):
    #     aggressiveFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(aggressiveFGTable)

    # normalFGTable = PrettyTable()
    # normalFGTable.field_names = ["APK", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#RecordedPEs", "#Leaks", "#Results"]
    # for k, v in sorted(ngcMap.items()):
    #     normalFGTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.recordedFWPECnt + v.recordedBWPECnt, v.leakCount, v.resultsCount])
    # print(normalFGTable)

    integratedTable = PrettyTable()
    integratedTable.field_names = ["APK", "FDTime(s)", "MaxMem(MB)", "#PE", "#Leaks", "#Results", "CDTime(s)", "CDMaxMem(MB)", "#CDRDPEs", "AGCTime(s)", "AGCMaxMem(MB)", "#AGCRDPEs", "NGCTime(s)", "NGCMaxMem(MB)", "#NGCRDPEs"]
    for k, v in sorted(fdMap.items()):
        gcElem = gcMap[k]
        agcElem = agcMap[k]
        ngcElem = ngcMap[k]
        integratedTable.add_row([v.apkName, v.dataSolverTime, v.maxmemory, v.forwardPECount + v.barwardPECount, v.leakCount, v.resultsCount,
                                 gcElem.dataSolverTime, gcElem.maxmemory, gcElem.recordedFWPECnt + gcElem.recordedBWPECnt,
                                 agcElem.dataSolverTime, agcElem.maxmemory, agcElem.recordedFWPECnt + agcElem.recordedBWPECnt,
                                 ngcElem.dataSolverTime, ngcElem.maxmemory, ngcElem.recordedFWPECnt + ngcElem.recordedBWPECnt])
    print(integratedTable)

if __name__ == '__main__':
    file = '/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/AGC/com.emn8.mobilem8.nativeapp.bk_5.0.10.log'
    fd = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FlowDroid", "FlowDroid")
    gc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/GC", "CleanDroid")
    agc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/AGC/", "AGC")
    ngc = loadParserList("/home/hedj/Work/CleanPathEdge/artifacts/myout/FINEGRAIN/NGC/", "NGC")
    buildTable(fd, gc, agc, ngc)

#!/usr/bin/python3
import os

# This class is used to store the key information in the output log file of each app under each solver.
class LogParser():
    def __init__(self):
        self.solver = '' # solver name
        self.apkName = '' # App name
        self.leakCount = -1
        self.resultsCount = -1 # the number of taint values at the sink statements.
        self.dataSolverTime = -1 # in seconds
        self.maxmemory = -1 # in MB
        self.forwardPECount = -1 # |PathEdge| in the forward IFDS solver
        self.backwardPECount = -1
        self.recordedFWPECnt = -1 # |PathEdge_max| in the forward IFDS solver
        self.recordedBWPECnt = -1
        self.adgEdgeCnt = -1 # the number of ADG edges
        self.sumEdgeCnt = -1 # the number of summary edges
        self.dummySumCnt = -1 # the number of dummy summary edges
        self.oom = False # Out of memory?
        self.to = False # Out of Time?

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
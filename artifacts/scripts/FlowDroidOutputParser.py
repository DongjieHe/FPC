#!/usr/bin/python3

import os
import xml.etree.ElementTree as ET
# pip3 install prettytable
from prettytable import PrettyTable

def extractXmlMap(xml):
    tree = ET.parse(xml)
    root = tree.getroot()
    perf = root.find("PerformanceData")
    ret = {}
    if perf is None:
        print(xml)
    for perfEntry in perf:
        entryMap = perfEntry.items()
        if perfEntry.tag == "PerformanceEntry":
            ret[entryMap[0][1]] = entryMap[1][1]
    results = root.find("Results")
    if results is not None:
        ret["LeakNum"] = len(results)
    else:
        ret["LeakNum"] = 0
    if "TaintPropagationSeconds" not in ret:
        ret["TaintPropagationSeconds"] = 0
    if "SourceCount" not in ret:
        ret["SourceCount"] = 0
    if "SinkCount" not in ret:
        ret["SinkCount"] = 0
    if "PropagationCount" not in ret:
        ret["PropagationCount"] = 0
    return ret

def outputList(outdir):
    ret = []
    for f in os.listdir(outdir):
        filePath = os.path.join(outdir, f)
        if os.path.isfile(filePath) and f.endswith(".xml"):
            xmlMap = extractXmlMap(filePath)
            xmlMap["APP"] = f[:-4]
            ret.append(xmlMap)
    return ret

def outputMap(outdir):
    ret = {}
    for f in os.listdir(outdir):
        filePath = os.path.join(outdir, f)
        if os.path.isfile(filePath) and f.endswith(".xml"):
            xmlMap = extractXmlMap(filePath)
            ret[f[:-4]] = xmlMap
    return ret

def buildTable(outList):
    table = PrettyTable()
    table.field_names = ["APP", "CG construction time (s)", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#Leaks", "#Sources", "#Sinks"]
    for xmlMap in outList:
        table.add_row([xmlMap["APP"], xmlMap["CallgraphConstructionSeconds"], xmlMap["TaintPropagationSeconds"], xmlMap["MaxMemoryConsumption"], xmlMap["PropagationCount"], xmlMap["LeakNum"], xmlMap["SourceCount"], xmlMap["SinkCount"]])
    return table

def buildTable2(outMap, outMap2):
    table = PrettyTable()
    table.field_names = ["APP", "CG construction time (s)", "IFDS Time (s)", "Max Memory (MB)", "#PathEdges", "#Leaks", "#Sources", "#Sinks"]
    for app in outMap:
        if app in outMap2:
            xmlMap = outMap[app]
            xmlMap2 = outMap2[app]
            table.add_row([app, xmlMap["CallgraphConstructionSeconds"], xmlMap["TaintPropagationSeconds"], xmlMap["MaxMemoryConsumption"], xmlMap["PropagationCount"], xmlMap["LeakNum"], xmlMap["SourceCount"], xmlMap["SinkCount"]])
            table.add_row(["", xmlMap2["CallgraphConstructionSeconds"], xmlMap2["TaintPropagationSeconds"], xmlMap2["MaxMemoryConsumption"], xmlMap2["PropagationCount"], xmlMap2["LeakNum"], xmlMap2["SourceCount"], xmlMap2["SinkCount"]])
    return table

# Main
if __name__ == '__main__':
    # outputxml = "/home/hedj/Work/OnlineIFDS/artifacts/output/run1/graphics.xml"
    # print(extractXmlMap(outputxml))
    # outdir = "/home/hedj/Work/OnlineIFDS/artifacts/output/run1"
    # outdir2 = "/home/hedj/Work/OnlineIFDS/artifacts/output/run2"
    outdir = "/home/hedj/Work/OnlineIFDS/artifacts/output/qilin/FDroid/graphics/"
    outdir2 = "/home/hedj/Work/OnlineIFDS/artifacts/output/tower/FDroid/graphics/"
    table = buildTable2(outputMap(outdir), outputMap(outdir2))
    print(table)

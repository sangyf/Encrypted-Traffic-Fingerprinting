#!/usr/bin/python2

import feature_extraction as fe
import itertools
from copy import copy

MTU = 1500
DATA_THRESHOLD = 100

def padTraces(traces, smart=False):
    paddedTraces = []
    for t in traces:
        pt = copy(t)
        pt.packetsizes = []
        for p in t.packetsizes:
            if not smart or abs(p) >= DATA_THRESHOLD:
                pt.packetsizes.append(MTU * abs(p) / p)
            else:
                pt.packetsizes.append(p)
        paddedTraces.append(pt)
    return paddedTraces

if __name__ == "__main__":
    allTraces = fe.window_all_traces(fe.load_traces())
    print("Saving %d traces to full_traces.dat" % len(allTraces))
    #allTraces = fe.load_pickled_traces("tor", "tor_traces/full_traces.dat")
    fe.pickle_traces(allTraces, "tor_traces/http_traces.dat")
    grouppedTraces = itertools.groupby(allTraces, key=lambda x: x.label)
    maxLen = 9999999999999999999999
    for label, traces in grouppedTraces:
        numTraces = len(list(traces))
        print("Have %d %s traces..." % (numTraces, label))
        maxLen = min(numTraces, maxLen)
    print("Taking the first %d traces of each label" % maxLen)
    grouppedTraces = itertools.groupby(allTraces, key=lambda x: x.label)
    narrowedTraces = []
    for label, traces in grouppedTraces:
        narrowedTraces.extend(list(traces)[0:maxLen])
    print("Saving %d traces to narrowed_traces.dat" % len(narrowedTraces))
    fe.pickle_traces(narrowedTraces, "tor_traces/narrowed_http_traces.dat")
    print("Padding all traces...")
    paddedTraces = padTraces(allTraces)
    print("Saving %d padded traces to padded_traces.dat" % len(paddedTraces))
    fe.pickle_traces(paddedTraces, "tor_traces/padded_http_traces.dat")
    print("Smart padding all traces...")
    smartPaddedTraces = padTraces(narrowedTraces, True)
    print("Saving %d padded traces to smart_traces.dat" % len(smartPaddedTraces))
    fe.pickle_traces(paddedTraces, "tor_traces/smart_http_traces.dat")

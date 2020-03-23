#Author: Sergio Schmiegelow (sergio.schmiegeloe@gmail.com)
import time
import threading
import sys
import math
import functools

try:
    import numpy as np
    NUMPY = True
except:
    NUMPY = False
#-------------------------------------------------------------------------
class loopTimeMeasureClass:
    '''Class to measure code segments execution time in loops'''
#-------------------------------------------------------------------------
    def __init__(self, timeFunction='clock', mode = 'timeSum'):
        self.lock = threading.Lock()
        self.lock.acquire()
        self.timeMetersDict = {}
        if timeFunction == 'clock':
            self.timeFunction = time.clock
        elif timeFunction == 'time':
            self.timeFunction = time.time
        else:
            print ("Error: timeFunction must be 'clock' or 'time'")
            self.lock.release()
            sys.exit(1)
        if mode in ['timeSum', 'stats']:
            self.mode = mode
        else: #stats
            print ("Error: mode must be 'timeSum' or 'stats'")
            self.lock.release()
            sys.exit(2)
        self.lock.release()
        #elements format: [startTimestamp, accumulated time | time list]
#-------------------------------------------------------------------------
    def start(self, id):
        '''Start/create timeMeter'''
        self.lock.acquire()
        if id in self.timeMetersDict.keys():
            if self.timeMetersDict[id][0] is not None:
                print ("ERROR: double loopTimeMeasure timeMeter inicialization")
                self.lock.release()
                return
            self.timeMetersDict[id][0] = self.timeFunction()
        else:
            if self.mode == 'timeSum':
                self.timeMetersDict[id] = [self.timeFunction(), 0]
            else:
                self.timeMetersDict[id] = [self.timeFunction(), []]
        self.lock.release()
#-------------------------------------------------------------------------
    def stop(self, id):
        '''Stop timeMeter and sum on total time'''
        self.lock.acquire()
        if not id in self.timeMetersDict.keys():
            print ("ERROR: stopping inexistent loopTimeMeasure timeMeter")
            self.lock.release()
            return
        timeMeter = self.timeMetersDict[id]
        elapsed = self.timeFunction() - timeMeter[0]
        if self.mode == 'timeSum':
            timeMeter[1] += elapsed
        else: #stats
            timeMeter[1].append(elapsed)
        timeMeter[0] = None
        self.lock.release()
#-------------------------------------------------------------------------
    pause = stop
#-------------------------------------------------------------------------
    def getTime(self, id):
        '''Returns the amount of time or time list on the meter'''
        self.lock.acquire()
        if not id in self.timeMetersDict.keys():
            print ("ERROR: Inexistent loopTimeMeasure timeMeter")
            self.lock.release()
            return
        timeMeter = self.timeMetersDict[id]
        if timeMeter[0] is not None:
            #Timer is running
            partialTime = self.timeFunction() - timeMeter[0]
        else:
            #Timer is stopped
            partialTime = None
        if partialTime:
            if self.mode == 'timeSum':
                timeMeter[1] += elapsed
            else: #stats
                timeMeter[1].append(elapsed)
        totalTime = timeMeter[1]
        self.lock.release()
        return totalTime
#-------------------------------------------------------------------------
    def reset(self, id):
        '''Reset timeMeter totalTime'''
        self.lock.acquire()
        if not id in self.timeMetersDict.keys():
            print ("ERROR: reseting inexistent loopTimeMeasure timeMeter")
            self.lock.release()
            return
        timeMeter = self.timeMetersDict[id]
        timeMeter[0] = None
        if self.mode == 'timeSum':
            timeMeter[1] = 0
        else: #stats
            timeMeter[1] = []
        self.lock.release()
#-------------------------------------------------------------------------
    def report(self, sortMode = 'time', reverse = True):
        '''Show all the accumulated times'''
        self.lock.acquire()
        if self.mode == 'timeSum':
            if sortMode == 'time':
                sortedTimeMeters = sorted(self.timeMetersDict.items(), key=lambda x: x[1][1], reverse = reverse)
            elif sortMode == 'id':
                sortedTimeMeters = sorted(self.timeMetersDict.items(), key=lambda x: x)
            else:
                print("Error: sortMode must be 'id' or 'time'. Using 'time'")
                sortedTimeMeters = sorted(self.timeMetersDict.items(), key=lambda x: x[1][1], reverse = reverse)
            for element in sortedTimeMeters:
                print ("%s:%fs"%(element[0], element[1][1]))
        else: #stats
            if NUMPY:
                sumFunc, avgFunc, minFunc, maxFunc, stdFunc = sum, internalAverage, min, max, internalStdev
            else:
                sumFunc, avgFunc, minFunc, maxFunc, stdFunc = np.sum, np.mean, np.min, np.max, np.std
            idsList = list(self.timeMetersDict.keys())
            sumsList   = []
            avgsList  = []
            minsList   = []
            maxsList   = []
            stdevsList = []
            numSamplesList = []
            for id in idsList:
                if NUMPY:
                    timeArray = np.array(self.timeMetersDict[id][1])
                else:
                    timeArray = self.timeMetersDict[id][1]
                if len(timeArray) > 0:
                    sumsList.append(sumFunc(timeArray))
                    avgsList.append(avgFunc(timeArray))
                    minsList.append(minFunc(timeArray))
                    maxsList.append(maxFunc(timeArray))
                    stdevsList.append(stdFunc(timeArray))
                    numSamplesList.append(len(timeArray))
                else:
                    sumsList.append(float('NaN'))
                    avgsList.append(float('NaN'))
                    minsList.append(float('NaN'))
                    maxsList.append(float('NaN'))
                    stdevsList.append(float('NaN'))
                    numSamplesList.append(0)
            joinedList = zip(idsList, sumsList, avgsList, minsList, maxsList, stdevsList, numSamplesList)
            try:
                sortIndex = ['id', 'time', 'average', 'min', 'max', 'stdev', 'num_samples'].index(sortMode)
            except:
                print("Error: sortMode must be 'id', 'time', 'average', 'min', 'max', 'stdev' or 'num_samples'")
                sortIndex = 1
            joinedList = sorted(joinedList, key=lambda x: x[sortIndex], reverse = reverse)
            print("id, total_time, average_time, min_time, max_time, std_time, num_samples")
            for idLine in joinedList:
                print("%s, %f, %f, %f, %f, %f, %d"%idLine)
        print("")

        self.lock.release()
#-------------------------------------------------------------------------
# DECORATOR
#-------------------------------------------------------------------------
decoratedFunctionsObject = None
#-------------------------------------------------------------------------
def measureFunctionTime(timeFunction = 'clock', mode = 'timeSum'):
    def decorator(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            global decoratedFunctionsObject
            if decoratedFunctionsObject is None:
                decoratedFunctionsObject = loopTimeMeasureClass(timeFunction, mode)
            decoratedFunctionsObject.start(function.__name__)
            result = function(*args, **kwargs)
            decoratedFunctionsObject.stop(function.__name__)
            return result
        return wrapper
    return decorator
#-------------------------------------------------------------------------
def reportFunctionsTimes(sortMode = 'time'):
    decoratedFunctionsObject.report(sortMode)
#-------------------------------------------------------------------------
# Statistical functions in case of numpy is missing
#-------------------------------------------------------------------------
def internalAverage(timeList):
    if len(timeList) == 0:
        return 0
    return sum(timeList) / float(len(timeList))
#-------------------------------------------------------------------------
def internalStdev(timeList):
    if len(timeList) < 2:
        return 0
    avg = internalAverage(timeList)
    sumOfSquares = 0
    for timeSample in timeList:
        sumOfSquares += (timeSample - avg) ** 2
    return math.sqrt(sumOfSquares / (len(timeList -1)))
#-------------------------------------------------------------------------

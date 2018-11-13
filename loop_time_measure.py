#Author: Sergio Schmiegelow (sergio.schmiegeloe@gmail.com)
import time
import threading
class loopTimeMeasureClass:
    '''Class to measure code segments execution time in loops'''
#-------------------------------------------------------------------------
    def __init__(self, timeFunction='clock'):
        self.lock = threading.Lock()
        self.lock.acquire()
        self.timeMetersDict = {}
        self.lock.release()
        if timeFunction == 'clock':
            self.timeFunction = time.clock
        elif timeFunction == 'time':
            self.timeFunction = time.time
        else:
            print ("Error: timeFunction must be 'clock' or 'time'")
        #elements format: [startTimestamp, accumulated time]
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
            self.timeMetersDict[id] = [self.timeFunction(), 0]
        self.lock.release()
#-------------------------------------------------------------------------
    def stop(self, id):
        '''Stop timeMeter and sum total time'''
        self.lock.acquire()
        if not id in self.timeMetersDict.keys():
            print ("ERROR: stopping inexistent loopTimeMeasure timeMeter")
            self.lock.release()
            return
        timeMeter = self.timeMetersDict[id]
        timeMeter[1] += self.timeFunction() - timeMeter[0]
        timeMeter[0] = None
        self.lock.release()
#-------------------------------------------------------------------------
    pause = stop
#-------------------------------------------------------------------------
    def getTime(self, id):
        '''Returns the amount of time on the meter'''
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
            partialTime = 0
        totalTime = timeMeter[1] + partialTime
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
        timeMeter[1] = 0
        timeMeter[0] = None
        self.lock.release()
#-------------------------------------------------------------------------
    def report(self, sort = 'time'):
        self.lock.acquire()
        if sort == 'time':
            sortedTimeMeters = sorted(self.timeMetersDict.items(), key=lambda x: x[1][1], reverse = True)
        if sort == 'id':
            sortedTimeMeters = sorted(self.timeMetersDict.items(), key=lambda x: x)
        for element in sortedTimeMeters:
            print ("%s:%fs"%(element[0], element[1][1]))
        self.lock.release()

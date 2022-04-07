# Loop Time Measure

## Introduction
**loop_time_measure** is a very simple Python thread safe library to measure the time spent in segments of code in single or repeated executions.

## How it works
The meters are identified by an string and can be nested and/or interleaved.
The time amounts spent between the **start** and the **stop** methods are added to the respective id.
The **getTime** method can be used the get the current amount of time (or the list of times in "stats" mode) on a given id.
The **report** method prints the amount of time of all ids.

## Compatibility
* Python 3

## Dependencies
* time
* threading
* sys
* numpy (or math)
* functools

## Usage example:
### As functions:
```python
import loop_time_measure

ltm = loop_time_measure.loopTimeMeasureClass()

ltm.start('Total time')
for i in range(200):

    ltm.start('code A')
    for j in range(100):
        print('Time consumming code A')
    ltm.stop('code A')

    ltm.start('code B')
    for k in range(50):
        print('Time consumming code B')
    ltm.stop('code B')

ltm.stop('Total time')
ltm.report()
```
Output:
```
Time consumming code A
Time consumming code A
(...)
Time consumming code A
(...)
Time consumming code B
Time consumming code B
(...)
Time consumming code B
-----------------
Time statistics:
-----------------
all:0.232278s
codeA:0.153208s
codeB:0.077236s

```
### As decorator:
```python
from loop_time_measure import measureFunctionTime, reportFunctionsTimes

@measureFunctionTime(mode = 'stats') #the first decorator rules the parameters
def myFunction():
    print('Time consumming code')

@measureFunctionTime()
def myOtherFunction(text):
    text = text[::-1] #bogus processing
    print(text)
    return text

for i in range(25):
    myFunction()

for i in range(50):
    res = myOtherFunction('Other text')
    print("res =", res)

print("-----------------")
print("Time statistics:")
print("-----------------")
reportFunctionsTimes()
```
Output:
```
Time consumming code
Time consumming code
(...)
Time consumming code
(...)
txet rehtO
res = txet rehtO
txet rehtO
res = txet rehtO
(...)
txet rehtO
res = txet rehtO
-----------------
Time statistics:
-----------------
id, total_time, average_time, min_time, max_time, std_time, num_samples
myOtherFunction, 0.000592, 0.000012, 0.000011, 0.000014, 0.000001, 50
myFunction, 0.000308, 0.000012, 0.000010, 0.000041, 0.000006, 25
```
## Documentation

### Class
* **loopTimeMeasureClass(timeFunction='process_time', mode = 'timeSum')**

    Class for the time measurements. You need only one object for all meters.

    The timeFunction parameter selects the function used to get the time.

    * The default timeFunction is **"process_time"** ( time.process_time() ) and it measures CPU time.

    * The alternative is **"time"** ( time.time() ), for real time measurement.

    The mode parameter selects the time storing mode.

    * The default timeFunction is **"timeSum"**. It keeps only the sum of times.

    * The alternative is **"stats"**. It keeps a list with all time measurement and, on the report, the output is a CSV with several statistical data.
---
### Methods
* **start(id)**

    Starts a meter.
---
* **stop(id)**

    Stop (or pause) a meter
---
* **pause(id)**

    Alias to **stop**
---
* **reset(id)**

    Reset (set to zero the time amount) a meter
---
* **report([sort])**

    Print a report of all meters. The time unit is seconds. The parameter **sort** indicates the sort criteria to be used to determine the meters print order.
    In **"timeSum"** mode, the default is **"time"**, to sort by descending total time values. The alternative is **"id"**, to sort by the id strings.
    In **"stats"** mode, the default is **"time"**, to sort by descending total time values. The alternatives are:
    * **"id"** - Meter Id (or function name, in decorator mode);
    * **"average"** - Average of the registered times (between starts and stops);
    * **"min"** - Minimum registered time;
    * **"max"** - Maximum registered time;
    * **"stdev"** - Standard deviation of the registered times;
    * **"num_samples"** - Number of registered times.

### Decorator
* @measureFunctionTime(timeFunction='process_time', mode = 'timeSum')

Wraps a function in a time measurement

The first decorator parameters are replicated to all the other decorators.
### Functions
* reportFunctionsTimes(sort = 'time')

Report the measured times on all decorated functions
## Author
* Sergio Schmiegelow
* sergio.schmiegelow@gmail.com

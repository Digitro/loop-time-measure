# Loop Time Measure

## Introduction
**loop_time_measure** is a very simple Python thread safe library to measure the time spent in segments of code in single or repeated executions.

## How it works
The meters are identified by an string and can be nested and/or interleaved.
The time amounts spent between the **start** and the **stop** methods are added to the respective id.
The **getTime** method can be used the get the current amount of tine on a given id.
The **report** method prints the amount of time of all ids.

## Compatibility
* Python 2
* Python 3

## Dependencies
* time
* threading

## Usage example:
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
(...)
Total time:0.141112s
code A:0.092167s
code B:0.046937s

```
## Documentation

### Class
* **loopTimeMeasureClass([timeFunction])**

    Class for the time measurements. You need only one object for all meters.

    The timeFunction parameter selects the function used to get the time.

    * The default function is **"clock"** ( time.clock() ) and it measures CPU time.

    * The alternative is **"time"** ( time.time() ), for real time measurement.
---
### Methods
* **start(id)**

    Starts a meter.
---
* **stop(id)**

    Stop (or pause) a meter
---
* **pause(id)**

    Alias to *stop*
---
* **reset(id)**

    Reset (set to zero the time amount) a meter
---
* **report([sort])**

    Print a report of all meters. The parameter **sort** indicates the sort criteria to be used to determine the meters print order. The default is **"time"**, to sort by descending meters values. The alternative is **"id"**, to sort by the id strings.

## Author
* Sergio Schmiegelow
* sergio.schmiegelow@gmail.com

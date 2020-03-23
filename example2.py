from loop_time_measure import measureFunctionTime, reportFunctionsTimes

@measureFunctionTime
def myFunction(n):
    for j in range(n):
        print('Time consumming code')

@measureFunctionTime
def myOtherFunction(n, text):
    for j in range(n):
        print(text)

myFunction(100)
myOtherFunction(50, 'Other text')
reportFunctionsTimes()

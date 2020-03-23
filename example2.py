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

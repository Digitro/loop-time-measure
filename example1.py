import loop_time_measure

ltm = loop_time_measure.loopTimeMeasureClass()

ltm.start('all')

for i in range(200):
    ltm.start('codeA')
    for j in range(100):
        print('Time consumming code A')
    ltm.stop('codeA')

    ltm.start('codeB')
    for k in range(50):
        print('Time consumming code B')
    ltm.stop('codeB')
    
print("-----------------")
print("Time statistics:")
print("-----------------")
ltm.stop('all')
ltm.report()

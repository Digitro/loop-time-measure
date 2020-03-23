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

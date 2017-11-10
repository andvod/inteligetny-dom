
import time
from general import general
import temperature
from constants import *
import mybase
import webbrowser
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

class Run(object):
        """
        program biegnie po srodkowych urzadzeniach
        :param czas: integer
        :return: void
        """
        def __init__(self, timeBreak=1):
            self.timeBreak = timeBreak

        def rfid(self):
            if MainClass.RFID():
                MainClass.Closing(PinActivity)
                MainClass.LightDiods(LightCardOpen)
                MainClass.Opening(PinActivity)
            return None

        def click(self):
            if MainClass.button(VerificationOutputPin, VerificationInputPin):
                MainClass.Opening(ButtonClick)
                time.sleep(self.timeBreak)
                MainClass.Closing(ButtonClick)
                print ('button passed')

                SQLQuery = 'SELECT website FROM Cards where Codes="%s"' % MainClass.card
                Mysql = mybase.Mysql()
                Mysql.configuration()
                WebSite = Mysql.query_select(SQLQuery)
                try:
                    print (WebSite)
                    ##webbrowser.open(WebSite[0]['website'])
                except KeyError:
                    pass

            return None

if __name__ == "__main__":
    MainClass = general()
    project = Run(2)

    start = time.clock()
    finish = start + TimeRuning
    while ((finish - start) > 0):
        project.rfid()
        project.click()
        start = time.clock()

    start = time.clock()
    finish = start + TimeRuning
    while ((finish - start) > 0):
        print(temperature.read_temp())                 # Print temperature
        time.sleep(1)
        start = time.clock()
    
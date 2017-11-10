
import time
from py532lib.i2c import *
from py532lib.frame import *
from py532lib.constants import *
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
import pymysql
import excel
import mybase
from constants import *



class general():
    """
    idzie glowny program
    """
    def __init__(self):
        self.card = None
    def __del__(self):
        pass

    def run(self, czas=0):
        """
        program biegnie po srodkowych urzadzeniach
        :param czas: integer
        :return: void
        """
        start = time.clock()
        finish = start + czas
        while ((finish - start) > 0):

            if self.RFID():
                self.Closing(PinActivity)
                self.LightDiods(LightCardOpen)
                self.Opening(PinActivity)

            if self.button(VerificationOutputPin, VerificationInputPin):
                self.Opening(ButtonClick)
                time.sleep(2)
                self.Closing(ButtonClick)
                print ('button passed')

                SQLQuery = 'SELECT website FROM Cards where Codes="%s"' % self.card
                Mysql = mybase.Mysql()
                Mysql.configuration()
                WebSite = Mysql.query_select(SQLQuery)
                try:
                    print (WebSite)
                    ##webbrowser.open(WebSite[0]['website'])
                except KeyError:
                    pass

            start = time.clock()
        return None

    def RFID(self):
        """
        Program uses I2C and reads code card's
        :return: bool
        """
        pn532 = Pn532_i2c()
        pn532.SAMconfigure()
        print ('card')
        card_data = pn532.read_mifare().get_data()
        self.card = str(card_data)

        if self.ReviseCod(card_data):
            return True
        else:
            print ("Denied permission, card isn't defined")
            time.sleep(1)
            print ("time left")
            return False

    def ReviseCod(self, code, SQLQuery='SELECT title FROM Cards where Codes="%s"'):
        """
        This function checks obtained code from rfid with database's codes
        :param code: bytearray
        :return: bool
        """
        Mysql = mybase.Mysql()
        Mysql.configuration()
        CardData = Mysql.query_select(SQLQuery % str(code))

        if (len(CardData) > 0):
            for i in range(len(CardData)):
                print (CardData[i]['title'])
            return True
        else:
            print ("EroorCard")
            return False


    def Opening(self, pin):
        """
        :param pin: integer
        Sends a signal to the selected pin
        :return: void
        """
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)
        return None

    def Closing(self, pin):
        """
        :param pin: integer
        Sends a signal to the selected pin
        :return: void
        """
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, False)
        return None

    def Reading(self, pin):
        """
        Receives a signal from a selected pin
        :param pin: integer
        :return: integer
        """
        GPIO.setup(pin, GPIO.IN)
        input_value = GPIO.input(pin)
        return input_value

    def LightDiods(self, pin):
        """
        It's lights show
        :return: void
        """
        GPIO.setup(pin, GPIO.OUT)

        for i in range(5):
            GPIO.output(pin, True)
            time.sleep(1)

            GPIO.output(pin, False)
            time.sleep(1)
        return None

    def get_excel_table(self, name_table = 'outfile.xlsx', user = 'root',
                    passwd = '12345',
                    host = 'localhost',
                    db = 'mybase',
                    table = 'users'):
        excel.write_in_excel(name_table, user, passwd, host, db, table)
        return None

    def button(self, pinOutput, pinInput):
        """
        This function check was button pushed or not
        :param pinOutput: int
        :param pinIntut: int
        :return: bool
        """
        self.Opening(pinOutput)
        self.Opening(LightCardError)
        GPIO.setup(pinInput, GPIO.IN)

        start = time.clock()
        finish = start + 5
        one = 0
        zero = 0
        while (finish>start):
            input_gpio = GPIO.input(pinInput)
            if (input_gpio == 1):
                one += 1
            elif (input_gpio == 0):
                zero += 1
            start = time.clock()

        self.Closing(LightCardError)
        if (zero == 0) or (float(one)/zero > 1.2):
            return True
        else:
            return False




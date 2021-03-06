class si5338POST:
    def __init__(self, address = None, option = False, i2c = None, regs = None, interrupt = None, gpio = None):
        self._address = address
        self._option = option
        self._BUS = i2c
        self._REGS = regs
        self._interrupt = interrupt
        self._GPIO = gpio

        self._init()
    
    def _init(self):
        # Setting LVDS
        self._BUS.write_byte_data(self._address, 36, 0x06)
        self._BUS.write_byte_data(self._address, 37, 0x06)
        
        if self._option == True:
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x10)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x08)
            self._BUS.write_byte_data(self._address, self._REGS["PFDDIV"], 0x42)
            self._BUS.write_byte_data(self._address, self._REGS["PFDFB"], 0xB0)
            self._BUS.write_byte_data(self._address, self._REGS["PFDREFIN"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNFB1S1"], 0x26)
            self._BUS.write_byte_data(self._address, self._REGS["MSNFB2S1"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNFB2S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNFB3S1"], 0x01)
            self._BUS.write_byte_data(self._address, self._REGS["MSNFB3S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNSTATE"], 0x40)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x0C)

        self._GPIO.setup(self._interrupt, self._GPIO.IN)
    def check(self):
        if self._GPIO.input(self._interrupt) == True:
            print "Warning LoL"
            return True
        else:
            return False         
    
    

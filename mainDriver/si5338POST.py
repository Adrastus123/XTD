# -*- coding: utf-8 -*-

class si5338POST:

    def __init__(self, address = None, option = False, i2c = None, regs = None, interrupt = None, gpio = None):
        self._address = address
        self._option = option
        self._BUS = i2c
        self._REGS = regs
        self._interrupt = interrupt
        self._GPIO = gpio
        self._GPIO.setmode(gpio.BCM)
        self._CLKOUT_FMT = 'LVPECL'
        self._PFD_EXTFB = True
        self._MPPC_CLKOUT_EN = True
        self._init()
    
    def _init(self):
        # Output Channel Option Selection
        #Format : R2DIV_IN[7:5] R2DIV[4:2] MS2_PDN[1] DRV2_PDN[0]
        #Clk 0 - 0xc0 - Selected_Multisynth_out=selected  Output_Divider_0=enabled  Multisynth0=enabled Driver0=enabled
        self._BUS.write_byte_data(self._address, 31, 0xc0)
        #Clk 1 - same as above
        self._BUS.write_byte_data(self._address, 32, 0xc0)
        #Clk 2 - MPPC Clock Output
        if self._MPPC_CLKOUT_EN == True:
            self._BUS.write_byte_data(self._address, 33, 0xc0)
        else:
            self._BUS.write_byte_data(self._address, 33, 0xe3)
        
        self._BUS.write_byte_data(self._address, 34, 0xe3)
        
        # Setting LVDS Output Clks
        #Signal Format CLK0 
        self._BUS.write_byte_data(self._address, 36, 0x06)
        #Signal Format CLK1 
        self._BUS.write_byte_data(self._address, 37, 0x06)
        #Signal Format CLK2 
        self._BUS.write_byte_data(self._address, 38, 0x06)
        
        # Trimbits For Output Clk Drivers.
        #CLK 0 & 1 - 011 00011 - DRV1_TRIM 75 DRV0_TRIM 40
        self._BUS.write_byte_data(self._address, 40, 0x63)
        #trimbit for clk 1 n 2‬ 
        self._BUS.write_byte_data(self._address, 41, 0x8c)
        #TrimBits for CLK 3
        self._BUS.write_byte_data(self._address, 42, 0x23)

        # Setting PLL bypass
        #self._BUS.write_byte_data(self._address, 31, 0x08)        
        #Julien : This is completely wrong  Reg [31] is clock divider 0 output
        
        # Settting PLL PFD feedback input (External|Internal)
        if self._PFD_EXTFB == True:
            self._BUS.write_byte_data(self._address, 48, 0x2c)
        else:
            self._BUS.write_byte_data(self._address, 48, 0xac)
        
        # Setting Reference Clock Multiplex Output (P2CLKDIV_OUT|P1CLKDIV_OUT)
        if self._option == False:
            #self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x10)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x1D)
            #REG[28]=0x03 ‭00-Reserved[7:6]  0-R2DIV_IN[0]  000-R1DIV_IN[4:2]  11
            self._BUS.write_byte_data(self._address, 28, 0x03)
            #REG[29]=PFD_IN_REF[7:5],P1DIV_IN[4:3],P1DIV[2:0] ‭
            #011 P2DIV_OUT selected 00 100‬ Divided by 16 
            self._BUS.write_byte_data(self._address, self._REGS["PFDDIV"], 0x64)
            #REG[30]=PFD_IN_FB[7:5],P2DIV_IN[4:3],P2DIV[2:0]
            #Selects the external input applied to the PFD feedback input. See Reg48
            #‭101 reserved 00   100‬ Divided by 16
            self._BUS.write_byte_data(self._address, self._REGS["PFDFB"], 0xA4)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S1"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S2"], 0x26)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S4"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S1"], 0x01)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S4"], 0x80)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x0C)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x00)
        else:
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x1D)
            #Reg[28] = works just fine. 0x03
            self._BUS.write_byte_data(self._address, 28, 0x03)
            #‭Reg[29] = 010 P1DIV_OUT 00 differential Referecnce In 010 P1 Divide by 4‬
            self._BUS.write_byte_data(self._address, self._REGS["PFDDIV"], 0x42)
            #Reg[30] = ‭101 NoClockSelect  10 No Clockinput to P2 000 P2 Divided By 1‬
            self._BUS.write_byte_data(self._address, self._REGS["PFDFB"], 0xB0)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S1"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S2"], 0x26)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP1S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP2S4"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S1"], 0x01)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S2"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S3"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MSNP3S4"], 0x80)
            self._BUS.write_byte_data(self._address, self._REGS["ENOUTS"], 0x0C)
            self._BUS.write_byte_data(self._address, self._REGS["PLLWPASS"], 0x00)
            self._BUS.write_byte_data(self._address, self._REGS["MULTSYNMRST"], 0x08)                                
    
        self._GPIO.setup(self._interrupt, self._GPIO.IN)
    def check(self):
        if self._GPIO.input(self._interrupt) == True:
            print "Warning LoL"
            print "Reg [247] " + str(self.self._BUS.read_byte_data(self._address, 247))
            print "Reg [218] " + str(self.self._BUS.read_byte_data(self._address, 218))
            return True
        else:
            return False         
    
    def program(self, filename):
        #Use Clockbuilder Desktop 6.4 to generate the Reg mapping
        #filename map.txt is default file
        Reg = []
        with open(filename) as f:
            for line in f:
                line = line.partition("#")[0]
                line = line.rstrip()
                line = line.split(",")
                Reg.append(line)
        
        add_reg = [x for x in Reg if x != ['']] # address & reg sorted
        
        #Programming the reg value.
        for n in range(len(add_reg)):
            addr = int(add_reg[n][0])
            reg = int(add_reg[n][1][:-1], 16)
            if addr == 255: # Change Page number register if Reg > 256
                self._BUS.write_byte_data(self._address, addr, 0x1)
            else : 
                if(addr >= 256):
                    addr = addr - 256 # if Reg > 256 
                else : 
                    addr = addr # if Reg < 256
                self._BUS.write_byte_data(self._address, addr, reg)
        
        #Soft Reset After RAM programmmed - DO NOT REMOVE
        self._BUS.write_byte_data(self._address, 246, 0x02)
        self._BUS.write_byte_data(self._address, 246, 0x00)
      
    def regcheck(self, filename):
        #compare the register mapping map.txt with the current value.
        Reg = []
        with open(filename) as f:
            for line in f :
                line = line.partition("#")[0]
                line = line.rstrip()
                line = line.split(",")
                Reg.append(line)

        add_reg = [x for x in Reg if x != ['']]
        tmp = []

        test = self._BUS.read_byte_data(self._address, 255)
        test = hex(test)
        print test
        
        # checking 
        if test == 0x1:
            self._BUS.write_byte_data(self._address, 255, 0x00)
        else:
            pass
        
        for n in range(len(add_reg)):
            addr = int(add_reg[n][0])
            reg = int(add_reg[n][1][:-1], 16)
            if addr == 255 :
                value = self._BUS.write_byte_data(self._address, addr, 0x1)
                #print "The Register Values for " + str(addr) + " is " + str(hex(value))           
            else :
                if (addr >= 256):
                    addr = addr - 256
                    regN = hex(self._BUS.read_byte_data(self._address, addr))
                    if (int(regN) != reg):
                        tmp.append([addr, reg, int(regN)])
                    else:
                        pass
                else :
                    addr = addr
                    regN = self._BUS.read_byte_data(self._address, addr)
                    if (int(regN) != reg):
                        tmp.append([addr, reg, int(regN)])
                    else:
                        pass
        print tmp
     

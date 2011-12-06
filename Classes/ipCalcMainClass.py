import repoze.lru

__author__ = 'laithzahid'
__version__ = "0.1"



class ipCalcMainClass(object):
    """
    This class is the main IPv4 address management and calculations.
    """

#------------------Initialization & Presentation----------------------



    _maskList = {
        0:'0.0.0.0',
        1:'128.0.0.0',
        2:'192.0.0.0',
        3:'224.0.0.0',
        4:'240.0.0.0',
        5:'248.0.0.0',
        6:'252.0.0.0',
        7:'254.0.0.0',
        8:'255.0.0.0',
        9:'255.128.0.0',
        10:'255.192.0.0',
        11:'255.224.0.0',
        12:'255.240.0.0',
        13:'255.248.0.0',
        14:'255.252.0.0',
        15:'255.254.0.0',
        16:'255.255.0.0',
        17:'255.255.128.0',
        18:'255.255.192.0',
        19:'255.255.224.0',
        20:'255.255.240.0',
        21:'255.255.248.0',
        22:'255.255.252.0',
        23:'255.255.254.0',
        24:'255.255.255.0',
        25:'255.255.255.128',
        26:'255.255.255.192',
        27:'255.255.255.224',
        28:'255.255.255.240',
        29:'255.255.255.248',
        30:'255.255.255.252',
        31:'255.255.255.254',
        32:'255.255.255.255',
        }





    def __init__(self, givenIP = ''):
        """

        """
        
        # workingValues variable initialization
        self.workingIP = [0, 0, 0, 0]
        self.workingMask = 0
        self.workingMaskInt = [0, 0, 0, 0]
        # ----------------------------------

        # Split user's input based on '/', to separate the IP from the mask
        self.ipmask = givenIP.split('/')
        self.splitMask = self.ipmask[1]
        # ---------------------------------

        # Split IP segments based on '.'
        self.splitIP = self.ipmask[0].split('.')
        # ----------------------------------

        # IP address initialization.
        # To check if character is given instead of integer, and convert to integer
        # To check if segment is greater than 255
        # To check if more than 4 segments are given
        
        for index in range(len(self.splitIP)):
            self.workingIP[index] = int(self.splitIP[index])
            if self.workingIP[index] > 255: raise ValueError
            if index > 3: raise ValueError
        # --------------------------


        # Mask initialization
        self.workingMask = int(self.splitMask)
        if self.workingMask > 32 or self.workingMask < 0: raise ValueError
        if not self.workingMask:
            test = self.getClass()
            if test == 'A':
                self.workingMask = 8
            if test == 'B':
                self.workingMask = 16
            if test == 'C':
                self.workingMask = 24
            if test == 'D':
                print('Multicast Address, using /24')
                self.workingMask = 24
            if test == 'E':
                print('Reserved Address, using /24')
                self.workingMask = 24
            del test
        self.workingMaskListSplit = (self._maskList.get(self.workingMask)).split('.')
        self.workingMaskDotted = self._maskList.get(self.workingMask)
        for index in range(len(self.workingMaskListSplit)):
            self.workingMaskInt[index] = int(self.workingMaskListSplit[index])
        # ----------------------------


# ---------------------Representation---------------------


    def representOutput(self, givenIP):
        print(givenIP)
        print('->')
        print('Address:   {:15}  -  {:35}'.format(self.ipIntCalc(), self.ipBinCalc()))
        print('Netmask:   {:15}  -  {:35}'.format(self.workingMaskDotted, self.maskBinCalc()))
        print('Wildcard:  {:15}  -  {:35}'.format(self.wildNetCalcInt(), self.wildNetCalcBin()))
        print('->')
        print('Network:   {:15}  -  {:35}'.format(self.netCalcInt(), self.netCalcBin()))
        print('Broadcast: {:15}  -  {:35}'.format(self.broadcastCalcInt(), self.broadcastCalcBin()))
        print('->')
        print('# of Hosts: {}  '.format(self.hostsCalc()[0], self.hostsCalc()[1]))
        # Assigned it like that to avoid calculating the returned values multiple times.
        temp = self.rangeCalc()
        print('1st Host:   {}'.format(temp[1]))
        print('Last Host:  {}'.format(temp[2]))
        print(temp[0])
        print('Class: {}, Designation: {}'.format(self.getClass(), self.getDesignation()))
        print('Finished')
        

        

#------------------Conversion--------------------------
    def getClass(self):
        """
        This method calculates the class of the given IP address.
        1. It works on a dotted binary string IP address.
        2. Returns a string 'A', 'B', 'C', 'D' or 'E'
        """

        self.ipClass = ''
        test = self.ipBinCalc()
        if test[0] == '0':
            self.ipClass = 'A'

        if test[:2] == '10':
            self.ipClass = 'B'

        if test[:3] == '110':
            self.ipClass =  'C'

        if test[:4] == '1110':
            self.ipClass = 'D'

        if test[:4] == '1111':
            self.ipClass = 'E'

        return self.ipClass

    def getDesignation(self):
        """
        1. Works on various variables to find the designation of the given IP
        2. Return the designation self.ipDesignation as a string
        """

        self.ipDesignation = ''
        test = self.ipBinCalc()
        if test[0] == '0' and self.workingMask == 0:
            self.ipDesignation = 'Internet Block'

        elif test[0] == '0' and self.workingIP[0] == 10 and self.workingMask >= 8:
            self.ipDesignation = 'Internet Private Address'

        elif test[0] == '0' and self.workingIP[0] == 10 and self.workingMask <= 8:
            self.ipDesignation = 'Internet Private Address - Supernetting'

        elif test[0] == '0' and self.workingMask <= 8:
            self.ipDesignation = 'Internet Public Address - Supernetting'
            
        elif test[0] == '0' and self.workingIP[0] == 127:
            self.ipDesignation = 'Local Host Address'

        elif test[:2] == '10' and self.workingIP[0] == 172 and self.workingIP[1] == 16 and self.workingMask >= 12:
            self.ipDesignation = 'Internet Private Address'

        elif test[:2] == '10' and self.workingIP[0] == 172 and self.workingIP[1] == 16 and self.workingMask <= 12:
            self.ipDesignation = 'Internet Private Address - Supernetting'

        elif test[:2] == '10' and self.workingMask <= 16:
            self.ipDesignation = 'Internet Public Address - Supernetting'

        elif test[:3] == '110' and self.workingIP[0] == 192 and self.workingIP[2] == 2 and self.workingMask == 24:
            self.ipDesignation =  'TEST-NET'

        elif test[:3] == '110' and self.workingIP[0] == 192 and self.workingIP[1] == 168 and self.workingMask >= 16:
            self.ipDesignation =  'Internet Private Address'

        elif test[:3] == '110' and self.workingIP[0] == 192 and self.workingIP[1] == 168 and self.workingMask <= 16:
                self.ipDesignation =  'Internet Private Address - Supernetting'

        elif test[:3] == '110' and self.workingIP[0] == 169 and self.workingIP[1] == 254 and self.workingMask == 16:
            self.ipDesignation =  'Link Local'

        elif test[:3] == '110' and self.workingMask <= 24:
            self.ipDesignation =  'Internet Public Address - Supernetting'

        elif test[:4] == '1110':
            self.ipDesignation = 'Multi-Cast'

        elif test[:4] == '1111':
            self.ipDesignation = 'Reserved'

        else:
            self.ipDesignation = 'Internet Public Address'

        return self.ipDesignation



    def ipIntCalc(self):
        """
        1. Calculates the dotted-decimal version of the IP address, based on the value of the list self.workingIP
        2. Returns self.intIP as string in the form of d.d.d.d
        """

        self.intIP = '{}.{}.{}.{}'.format(self.workingIP[0], self.workingIP[1],
                                          self.workingIP[2], self.workingIP[3])

        return self.intIP

    def ipBinCalc(self):
        """
        1. Calculates the dotted-binary version of the IP address, based on the value of the list self.workingIP
        2. Returns self.binIP as string in the form of b.b.b.b
        """

        self.binIP = '{:08b}.{:08b}.{:08b}.{:08b}'.format(self.workingIP[0], self.workingIP[1],
                                                          self.workingIP[2], self.workingIP[3])

        return self.binIP


    def maskBinCalc(self):
        """
        1. Calculates the dotted-binary version of the mask given, based on the value of self.workingMaskListSplit
        2. Returns self.binMask as string in the form of b.b.b.b
        """

        self.binMask = '{:08b}.{:08b}.{:08b}.{:08b}'.format(self.workingMaskInt[0], self.workingMaskInt[1],
                                                            self.workingMaskInt[2], self.workingMaskInt[3])

        return self.binMask


    def ipHexCalc(self):
        """
        1. Calculates the dotted-hexa version of the IP address, based on the value of self.workingIP
        2. Returns self.hexIP as string in the form of h.h.h.h
        """

        self.hexIP = '{:02x}.{:02x}.{:02x}.{:02x}'.format(self.workingIP[0], self.workingIP[1],
                                                          self.workingIP[2], self.workingIP[3])

        return  self.hexIP


    def maskHexCalc(self):
        """
        1. Calculates the dotted-hexa version of the mask given, based on the value of self.workingMaskListSplit
        2. Returns self.hexMask as string in the form of h.h.h.h
        """

        self.hexMask = '{:02x}.{:02x}.{:02x}.{:02x}'.format(self.workingMaskListSplit[0], self.workingMaskListSplit[1],
                                                            self.workingMaskListSplit[2], self.workingMaskListSplit[3])

        return self.hexMask





    
# ------------------- Calculation -----------------------


    def netCalcInt(self):
        """
        1. Calculates the net ID of the given IP address, by ANDing the corresponding value of self.workingIP and self.workignMaskInt
        2. Returns self.netID as list in the form of [d, d, d, d]
        3. Stores the form of d.d.d.d as string in self.netIDInt
        """
        self.netID = [0, 0, 0, 0]

        for index in range(len(self.workingIP)):
            self.netID[index] = self.workingIP[index] & self.workingMaskInt[index]

        self.netIDInt = "{}.{}.{}.{}".format(self.netID[0], self.netID[1],
                                             self.netID[2], self.netID[3])

        return self.netIDInt


    def netCalcBin(self):
        """
        1. Calculates the net ID of the given IP address, by ANDing the corresponding value of self.workingIP and self.workignMaskInt
        2. Returns self.netID as list in the form of [d, d, d, d]
        3. Stores the form of b.b.b.b as string in self.netIDBin
        """
        self.netID = [0, 0, 0, 0]

        for index in range(len(self.workingIP)):
            self.netID[index] = self.workingIP[index] & self.workingMaskInt[index]

        self.netIDBin = '{:08b}.{:08b}.{:08b}.{:08b}'.format(self.netID[0], self.netID[1],
                                                             self.netID[2], self.netID[3])

        return self.netIDBin

    def wildNetCalcInt(self):
        """
        1. Calculates the wild net ID of the given IP address, by subtracting the corresponding value of self.workingMaskInt from 255
        2. Returns self.wildNet as list in the form of [d, d, d, d]
        3. Stores the form of d.d.d.d as string in self.wildNetInt
        """

        self.wildNet = [0, 0, 0, 0]

        for index in range(len(self.workingMaskInt)):
            self.wildNet[index] = 255 - self.workingMaskInt[index]
#            self.wildnet[index] = 255 ^ self.workingMaskInt[index]

        self.wildNetInt = '{}.{}.{}.{}'.format(self.wildNet[0], self.wildNet[1], self.wildNet[2],
                                               self.wildNet[3])

        return self.wildNetInt

    def wildNetCalcBin(self):
        """
        1. Calculates the wild net ID of the given IP address, by subtracting the corresponding value of self.workingMaskInt from 255
        2. Returns self.wildNet as list in the form of [d, d, d, d]
        3. Stores the form of b.b.b.b as string in self.wildNetBin
        """

        self.wildNet = [0, 0, 0, 0]

        for index in range(len(self.workingMaskInt)):
            self.wildNet[index] = 255 - self.workingMaskInt[index]
#            self.wildnet[index] = 255 ^ self.workingMaskInt[index]

        self.wildNetBin = '{:08b}.{:08b}.{:08b}.{:08b}'.format(self.wildNet[0], self.wildNet[1],
                                                               self.wildNet[2], self.wildNet[3])

        return self.wildNetBin

    def broadcastCalcInt(self):
        """
        1. Calculates the broadcast address, by ORing the corresponding value of self.workingIP with self.wildNet
        2. Returns self.broadcast as list in the form of [d, d, d, d]
        3. Stores the form of d.d.d.d as string in self.broadcastInt
        """

        self.broadcast = [0, 0, 0, 0]
        self.wildNetCalcInt()
        for index in range(len(self.workingMaskInt)):
            self.broadcast[index] = self.workingIP[index] | self.wildNet[index]

        self.broadcastInt = '{}.{}.{}.{}'.format(self.broadcast[0], self.broadcast[1],
                                                 self.broadcast[2], self.broadcast[3])

        return self.broadcastInt

    def broadcastCalcBin(self):
        """
        1. Calculates the broadcast address, by ORing the corresponding value of self.workingIP with self.wildNet
        2. Returns self.broadcast as list in the form of [d, d, d, d]
        3. Stores the form of b.b.b.b as string in self.broadcastBin
        """

        self.broadcast = [0, 0, 0, 0]
        self.wildNetCalcInt()
        for index in range(len(self.workingMaskInt)):
            self.broadcast[index] = self.workingIP[index] | self.wildNet[index]

        self.broadcastBin = '{:08b}.{:08b}.{:08b}.{:08b}'.format(self.broadcast[0], self.broadcast[1],
                                                                 self.broadcast[2], self.broadcast[3])

        return self.broadcastBin

    def rangeCalc(self):
        """
        1. Check if the IP given is host IP or P2P.
        2. Otherwise, it calculates the first and last IP address in the range:
                        self.firstIP = self.netCalcInt() + 1
                        self.lastIP = self.broadcastCalc() - 1
        3. Returns the first and last IP addresses in the range in the format of '{} - {}' - str
        """

        self.firstIP = self.netID
        self.firstIP[3] += 1

        self.lastIP = self.broadcast
        self.lastIP[3] -= 1


        self.firstIPInt = '{}.{}.{}.{}'.format(self.firstIP[0], self.firstIP[1],
                                               self.firstIP[2], self.firstIP[3])
        self.lastIPInt = '{}.{}.{}.{}'.format(self.lastIP[0], self.lastIP[1],
                                              self.lastIP[2], self.lastIP[3])


        if self.workingMask == 32:
            host_route = 'Host route - Single host'
            return host_route, self.ipIntCalc(), 'None'
            # Host route - One host, e.g. 192.168.1.1/255.255.255.255
        elif self.workingMask == 31:
            # Point to Point (RFC 3021) - Two IPs - Should return netID and BroadcastID
            point_to_point = 'Point to Point (RFC 3021) - Two IP addresses, only valid if zero-subnet is enabled'
            return point_to_point, self.netIDInt, self.broadcastInt
        else:
            # A typical IP address range
            return '', self.firstIPInt, self.lastIPInt



    def hostsCalc(self):
        """
        1. Calculates the host bits by subtracting the self.workingMask form 32
        2. Returns self.hostBits and self.hosts as integer values
        """

        self.hostsBits = 32 - self.workingMask
        self.hosts = (2 ** self.hostsBits) - 2

        if self.workingMask == 32:
            # Host route - One host, e.g. 192.168.1.1/255.255.255.255
            return 1, 0

        elif self.workingMask == 31:
            # Point to Point (RFC 3021) - Two IPs
            return 2, 1

        if self.workingMask <= 30:
            # A typical IP address range
            return self.hosts, self.hostsBits



        
### Glossary ###
#
# reg8b   - 8 bit register: AL, CL, ... AH, CH, ...
# reg16b  - 16 bit register: AX, CX, ...
# val8b   - 8 bit value
# val16b  - 16 bit value
# dist8b  - jump distance from current position, range: -128 - +127
#

### Registers ###

AL = 0x00
CL = 0x01
DL = 0x02
BL = 0x03
AH = AL | 0x04
CH = CL | 0x04
DH = DL | 0x04
BH = BL | 0x04

AX = 0x08
CX = 0x09
DX = 0x0A
BX = 0x0B
SP = 0x0C
BP = 0x0D
SI = 0x0E
DI = 0x0F

class Asm:
    _LABEL = '1:'
    _REL8  = '2:'

    def __init__(self):
        self._IP = 0x100
        self._bytecode = []
        self._labels = {}

    ### Assembly Instructions ###

    def NOP(self):
        """No Operation
        """
        self._bytecode.extend([0x90])
        self._IP += 1

    def INT(self, val8b):
        """"Call interrupt

        val8b: 8 bit interrupt number
        """
        self._bytecode.extend([0xCD, val8b & 0xFF])
        self._IP += 2

    def MOVR8(self, reg8b, val8b):
        """Move 8 bit value to register

        reg8b: destination register: AL, CL, ... AH, CH, ...
        val8b: 8 bit value
        """
        self._bytecode.extend([0xB0 | reg8b, val8b & 0xFF])
        self._IP += 2

    def MOVR16(self, reg16b, val16b):
        """Move 16 bit value to register

        reg16b: destination register: AX, CX, ...
        val16b: 16 bit value
        """
        self._bytecode.extend([0xB0 | reg16b])
        if type(val16b) == int:
            self._bytecode.extend([val16b & 0xFF, (val16b & 0xFF00) >> 8])
        else:
            self._bytecode.extend([self._LABEL + val16b])
        self._IP += 3

    def INC(self, reg16b):
        """Increment 16 bit register by one

        reg16b: register to be incremented: AX, CX, ...
        """
        self._bytecode.extend([0x40 | reg16b >> 4])
        self._IP += 1

    def DEC(self, reg16b):
        """Decrement 16 bit register by one

        reg16b: register to be decremented: AX, CX, ...
        """
        self._bytecode.extend([0x40 | reg16b])
        self._IP += 1

    def POP(self, reg16b):
        """Pop value from stack to 16 bit register

        reg16b: AX, CX, ...
        """
        self._bytecode.extend([0x50 | reg16b])
        self._IP += 1

    def PUSH(self, reg16b):
        """Push value from register to stack

        reg16b: AX, CX, ...
        """
        self._bytecode.extend([0x50 | (reg16b >> 4)])
        self._IP += 1

    def JMPN(self, dist8b):
        """Jump near

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0xEB])
        if type(dist8b) == str:
            self._bytecode.extend([self._REL8 + str(self._IP) + ':' + dist8b])
        else:
            self._bytecode.extend([dist8b & 0xFF])
        self._IP += 2

    def CMPAL(self, val8b):
        """Compare AL to value

        val8b: 8 bit value to be compared to
        """
        self._bytecode.extend([0x3C, val8b & 0xFF])
        self._IP += 2

    def CMPAX(self, val16b):
        """Compare AX to value

        val8b: 16 bit value to be compared to
        """
        self._bytecode.extend([0x3D, val16b & 0xFFFF])
        self._IP += 3

    def JZ(self, dist8b):
        """Jump is Zero flag is set

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x74, dist8b & 0xFF])
        self._IP += 2

    def JNZ(self, dist8b):
        """Jump if Zero flag is not set

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x75, dist8b & 0xFF])
        self._IP += 2

    def JL(self, dist8b):
        """Jump if Less than

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x7C, dist8b & 0xFF])
        self._IP += 2

    def JGE(self, dist8b):
        """Jump if Less than or Equal

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x7D, dist8b & 0xFF])
        self._IP += 2

    def JLE(self, dist8b):
        """Jump if Less than or Equal

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x7E, dist8b & 0xFF])
        self._IP += 2

    def JG(self, dist8b):
        """Jump if Greater than

        dist8b: relative distance in 8 bits
        """
        self._bytecode.extend([0x7F, dist8b & 0xFF])
        self._IP += 2

    ## Aliases ###

    def JE(self, dist8b):
        """Jump if Equal

        dist8b: relative distance in 8 bits
        """
        self.JZ(dist8b)

    def JNE(self, dist8b):
        """Jump if Not Equal

        dist8b: relative distance in 8 bits
        """
        self.JNZ(dist8b)

    ### Higher Level Assembler Support ###

    def LABEL(self, label):
        self._labels[label] = self._IP

    def DATA(self, data):
        self._bytecode.extend(data)

    ### Helper Functions ###

    def INPUTCH(self):
        self.MOVR8(AH, 0x01)
        self.INT(0x21)

    def PRINTCH(self, value):
        self.MOVR8(AH, 0x02)
        self.MOVR8(DL, value)
        self.INT(0x21)

    def EXIT(self, code=0):
        self.MOVR8(AH, 0x4C)
        self.MOVR8(AL, code)
        self.INT(0x21)

    def _byte(self, value):
        return [value & 0xFF]

    def _word(self, value):
        return [value & 0xFF, (value & 0xFF00) >> 8]

    ### Compiler Methods ###

    def getBytecode(self):
        return self._bytecode

    def compile(self):
        result = []
        for cell in self._bytecode:
            if type(cell) == str:
                if cell[:2] == self._LABEL:
                    result.extend(self._word(self._labels[cell[2:]]))
                if cell[:2] == self._REL8:
                    data = cell.split(':')
                    result.extend(self._byte(self._labels[data[2]] - int(data[1])))
            else:
                result.extend([cell])
        return result


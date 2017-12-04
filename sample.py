from asm8086 import *

### Sample Program ###

asm = asm()

asm.PRINTCH(ord('A'))                # Print 'A'
asm.JMPN("START")                    # Jump over next line to the label 'START'
asm.EXIT()                           # If we reach this line, then we have a bug somewhere
asm.LABEL("START")                   # Label representing a point in memory
asm.PRINTCH(ord('B'))                # Print 'B', if we see this character, then the code generator works!
asm.MOVR8(AH, 0x09)                  # Select string printing function provided by DOS
asm.MOVR16(DX, "DATA")               # Set address, where the printable string is located
asm.INT(0x21)                        # Call interrupt, printing the string to stdout
asm.EXIT()                           # Quit program
asm.LABEL("DATA")                    # Label pointing the beginning of the string
asm.DATA(list(b'\r\nHello World!$')) # String to be printed

print(asm.getBytecode())
print(asm.compile())

if __name__ == "__main__":
    f = open("test.com", "wb")
    f.write(bytes(asm.compile()))
    f.close()


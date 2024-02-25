# asm8086
A small 8086 toy assembler written in Python.

This is a small toy, which I whipped up one night.

With this library you can write very simple 8086 programs (DOS .COM programs)
that will work either under MS-DOS or DOSBOX. COM binaries are not supported
under modern 64-bit Windows environments :(

Design:

Assembler opcodes are appended as-is in integer format to the bytecode array.
If there is a label, then the label address is stored to a separate lookup
table. If there is a reference to a label, depending on a use-case a opcode, a
flag and label name are stored as a string to the bytecode array. Compiling
process simply extracts bytecodes one by one and stores them to the compiled
binary array, if the opcode is an integer. Otherwise it is assumed that the
"byte code" is actually a string containing a label. In that case, depending on
the flag value, a label value is looked up from the lookup table and possible
pointer arithmetic is performed. Then the opcode and resulting address
information is appended to the compiled array.

Check sample.py for a small example.


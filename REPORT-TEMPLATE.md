# Capstone Project Report
## Make the Computer Draw a Box

**Name:** Bhowmik Vij  
**Roll number:** 2501010195  
**Course:** Nand to Tetris – I (ETCCNT301)  
**Personal number:** K = 95  
**School:** School of Engineering & Technology, K.R. Mangalam University

## 1. Project objective
Build the Hack computer from its hardware components, implement a two-pass assembler in Python, and write a Hack assembly program that displays a black rectangle while a key is pressed and clears it when released.

For roll number **2501010195**, K = 95. Since 95 mod 4 = 3, the box width is 16 × (3 + 1) = **64 pixels**.

## 2. Part A — Build the computer
- **CPU.hdl:** connects the A register, D register, ALU, program counter, instruction decoder, memory output, and jump-control logic.
- **Memory.hdl:** maps RAM, screen memory, and keyboard memory-mapped input. Screen begins at 16384; keyboard is at 24576.
- **Computer.hdl:** connects CPU, ROM32K instruction memory, and Memory.

Record actual Hardware Simulator results and insert genuine screenshots:

| Official test | Actual result | Screenshot |
|---|---|---|
| CPU.tst | [Fill after running] | [Insert screenshot] |
| Memory.tst | [Fill after running] | [Insert screenshot] |
| ComputerAdd.tst | [Fill after running] | [Insert screenshot] |
| ComputerMax.tst | [Fill after running] | [Insert screenshot] |
| ComputerRect.tst | [Fill after running] | [Insert screenshot] |

## 3. Part B — Python assembler
The two-pass assembler first records labels and ROM addresses, then encodes A-instructions and C-instructions into 16-bit machine code. It supports predefined symbols and allocates variables from RAM address 16.

Run `python -m unittest -v test_assembler.py` and record the actual result. Compare Add.asm, Max.asm, Rect.asm, and Pong.asm with the official assembler and record genuine results.

## 4. Part C — Personalized box program
The box begins at row **95**, is **20 rows** tall, and is **64 pixels** wide. Each screen row contains 32 words, and each word represents 16 horizontal pixels. The box therefore occupies four words per row.

First screen address: **SCREEN + 32 × K = 16384 + 32 × 95 = 19424**

The program checks KBD (24576). When a key is pressed, it writes -1 to four consecutive screen words for each of 20 rows. When no key is pressed, it writes 0 to those same 80 words to clear the rectangle.

**Box dimensions:** 64 pixels wide × 20 rows high  
**Top-left screen row:** 95  
**First screen address:** 19424

**CPU Emulator screenshot — key pressed:** [Insert genuine screenshot]  
**CPU Emulator screenshot — key released:** [Insert genuine screenshot]

## 5. Conclusion
This capstone combines digital logic, computer architecture, assembly language, and Python programming. Include genuine simulator results, assembler comparison results, and CPU Emulator screenshots after completing local verification.

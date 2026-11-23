import re
import sys
from pathlib import Path

DEST = {"": "000", "M": "001", "D": "010", "MD": "011", "A": "100", "AM": "101", "AD": "110", "AMD": "111"}
JUMP = {"": "000", "JGT": "001", "JEQ": "010", "JGE": "011", "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111"}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010", "D": "0001100", "A": "0110000", "M": "1110000",
    "!D": "0001101", "!A": "0110001", "!M": "1110001", "-D": "0001111", "-A": "0110011", "-M": "1110011",
    "D+1": "0011111", "A+1": "0110111", "M+1": "1110111", "D-1": "0001110", "A-1": "0110010", "M-1": "1110010",
    "D+A": "0000010", "D+M": "1000010", "D-A": "0010011", "D-M": "1010011", "A-D": "0000111", "M-D": "1000111",
    "D&A": "0000000", "D&M": "1000000", "D|A": "0010101", "D|M": "1010101"
}
PREDEFINED = {"SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4, "SCREEN": 16384, "KBD": 24576}
PREDEFINED.update({f"R{i}": i for i in range(16)})
SYMBOL_PATTERN = re.compile(r"^[A-Za-z_.$:][A-Za-z0-9_.$:]*$")


class AssemblyError(Exception):
    pass


def clean_source(source):
    instructions = []
    for line_number, raw_line in enumerate(source.splitlines(), start=1):
        line = raw_line.split("//", 1)[0].strip()
        if line:
            instructions.append((line_number, line))
    return instructions


def assemble(source):
    instructions = clean_source(source)
    symbols = dict(PREDEFINED)
    rom_address = 0
    for line_number, line in instructions:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1].strip()
            if not SYMBOL_PATTERN.fullmatch(label) or label in symbols:
                raise AssemblyError(f"Line {line_number}: invalid or duplicate label")
            symbols[label] = rom_address
        elif line.startswith("(") or line.endswith(")"):
            raise AssemblyError(f"Line {line_number}: invalid label")
        else:
            rom_address += 1

    output = []
    next_variable = 16
    for line_number, line in instructions:
        if line.startswith("(") and line.endswith(")"):
            continue
        if line.startswith("@"):
            value = line[1:].strip()
            if not value:
                raise AssemblyError(f"Line {line_number}: invalid A-instruction")
            if value.isdigit():
                address = int(value)
            elif SYMBOL_PATTERN.fullmatch(value):
                if value not in symbols:
                    symbols[value] = next_variable
                    next_variable += 1
                address = symbols[value]
            else:
                raise AssemblyError(f"Line {line_number}: invalid symbol")
            if not 0 <= address <= 32767:
                raise AssemblyError(f"Line {line_number}: A-instruction value out of range")
            output.append(f"{address:016b}")
            continue
        try:
            if line.count("=") > 1 or line.count(";") > 1:
                raise ValueError
            instruction, separator, jump = line.partition(";")
            if separator and not jump.strip():
                raise ValueError
            if "=" in jump:
                raise ValueError
            dest, equals, comp = instruction.partition("=")
            if equals and not dest.strip():
                raise ValueError
            dest = dest.strip() if equals else ""
            comp = comp.strip() if equals else instruction.strip()
            jump = jump.strip() if separator else ""
            if comp not in COMP or dest not in DEST or jump not in JUMP:
                raise ValueError
            output.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except ValueError:
            raise AssemblyError(f"Line {line_number}: invalid instruction")
    return output, symbols


def main():
    if len(sys.argv) != 2:
        print("Usage: python assembler.py <file.asm>")
        raise SystemExit(1)
    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix(".hack")
    try:
        machine_code, _ = assemble(input_path.read_text(encoding="utf-8"))
        output_path.write_text("\n".join(machine_code) + "\n", encoding="utf-8")
        print(f"Assembly successful: {output_path} ({len(machine_code)} instructions)")
    except (OSError, AssemblyError) as error:
        print(error)
        raise SystemExit(1)


if __name__ == "__main__":
    main()

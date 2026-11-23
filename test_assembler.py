import unittest
from assembler import AssemblyError, assemble


class AssemblerTests(unittest.TestCase):
    def test_a_instruction(self):
        machine, _ = assemble("@21")
        self.assertEqual(machine, ["0000000000010101"])

    def test_c_instruction(self):
        machine, _ = assemble("D=M")
        self.assertEqual(machine, ["1111110000010000"])

    def test_label_resolution(self):
        machine, _ = assemble("@LOOP\n0;JMP\n(LOOP)\n@LOOP")
        self.assertEqual(machine, ["0000000000000010", "1110101010000111", "0000000000000010"])

    def test_variable_allocation(self):
        machine, _ = assemble("@counter\nM=1\n@counter")
        self.assertEqual(machine, ["0000000000010000", "1110111111001000", "0000000000010000"])

    def test_line_numbered_error(self):
        with self.assertRaisesRegex(AssemblyError, "Line 3: invalid instruction"):
            assemble("// heading\n@2\nD=Q")

    def test_duplicate_label_error(self):
        with self.assertRaisesRegex(AssemblyError, "Line 3: invalid or duplicate label"):
            assemble("(LOOP)\n@0\n(LOOP)")

    def test_missing_jump_condition(self):
        with self.assertRaisesRegex(AssemblyError, "Line 1: invalid instruction"):
            assemble("D;")

    def test_missing_destination(self):
        with self.assertRaisesRegex(AssemblyError, "Line 1: invalid instruction"):
            assemble("=D")


if __name__ == "__main__":
    unittest.main()

import unittest
from compiler.parser import XfawaParser

class TestParser(unittest.TestCase):
    def test_basic_parsing(self):
        source = """
#Python [[
print("Hello Python")
]]

#C [[
#include <stdio.h>
int main() {
    printf("Hello C\\n");
    return 0;
}
]]

#Main [[
xfawa.run("Python")
xfawa.run("C")
]]
"""
        parser = XfawaParser(source, "test.xfml")
        result = parser.parse()
        
        self.assertIn('Python', result['blocks'])
        self.assertIn('C', result['blocks'])
        self.assertIn('Main', result['blocks'])
        self.assertEqual(len(result['blocks']['Python']), 1)
        self.assertEqual(len(result['blocks']['C']), 1)
        self.assertEqual(len(result['blocks']['Main']), 1)
        
    def test_data_parsing(self):
        source = """
#data [[
{
    "Define_Output": true,
    "Entry_Point": "Python.main"
}
]]
"""
        parser = XfawaParser(source, "test.xfml")
        result = parser.parse()
        
        self.assertTrue(result['data']['define_output'])
        self.assertEqual(result['data']['entry_point'], 'Python.main')
        
    def test_multiple_blocks(self):
        source = """
#Python [[
print("Block 1")
]]

#Python [[
print("Block 2")
]]
"""
        parser = XfawaParser(source, "test.xfml")
        result = parser.parse()
        
        self.assertEqual(len(result['blocks']['Python']), 2)

if __name__ == '__main__':
    unittest.main()

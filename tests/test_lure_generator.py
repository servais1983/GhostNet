import unittest
from lure_generator.lure_generator import LureGenerator

class TestLureGenerator(unittest.TestCase):
    def test_generate_file_lure(self):
        lg = LureGenerator()
        result = lg.generate_file_lure("test.txt")
        self.assertEqual(result["filename"], "test.txt")
        self.assertIn("leurre", result["content"])

    def test_generate_service_lure(self):
        lg = LureGenerator()
        result = lg.generate_service_lure(12345)
        self.assertEqual(result["port"], 12345)

if __name__ == "__main__":
    unittest.main()
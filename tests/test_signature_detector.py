import unittest
from detection.signature_detector import SignatureDetector

class TestSignatureDetector(unittest.TestCase):
    def test_detect_known_signature(self):
        detector = SignatureDetector()
        log = "Tentative de connexion SSH échouée: Failed password"
        result = detector.analyze(log)
        self.assertTrue(result["detected"])
        self.assertEqual(result["type"], "signature")

    def test_no_detection(self):
        detector = SignatureDetector()
        log = "Connexion réussie"
        result = detector.analyze(log)
        self.assertFalse(result["detected"])

if __name__ == "__main__":
    unittest.main()
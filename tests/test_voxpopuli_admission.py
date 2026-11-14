import unittest
from scripts.admit_voxpopuli_cc0 import bands, CONFIGS, SOURCE, REVISION

class VoxPopuliAdmissionTests(unittest.TestCase):
    def test_scope_is_exact_and_train_only(self):
        self.assertEqual(SOURCE, "facebook/voxpopuli")
        self.assertEqual(CONFIGS, {"es","en","de","fr","it","pl"})
        self.assertEqual(REVISION, "42f01879c780b4a2e90ec0b4f616c2ece526e4f1")

    def test_simhash_band_partition(self):
        self.assertEqual(len(bands(0)), 4)
        self.assertEqual(bands(0), [(0,0),(1,0),(2,0),(3,0)])

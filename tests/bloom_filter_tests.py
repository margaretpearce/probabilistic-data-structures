import unittest
import mmh3
from bloom_filter import BloomFilter


class BloomFilterTests(unittest.TestCase):
    def test_set_optimal_m(self):
        expected = 95850    # Manually calculated given n=10000 p=0.01
        bf = BloomFilter(n=10000)
        actual = bf.m
        self.assertEqual(expected, actual)

    def test_set_optimal_k(self):
        expected = 6        # Manually calculated given p=0.01
        bf = BloomFilter()
        actual = bf.k
        self.assertEqual(expected, actual)

    def test_compute_hash(self):
        expected = mmh3.hash("10", 0) % 1000    # 0th hash of element "10" with m=1000
        bf = BloomFilter()
        actual = bf.compute_hash(0, 10)
        self.assertEqual(expected, actual)

    def test_add(self):
        elem_to_add = 10
        bf = BloomFilter(m=5, k=2)
        bits = bf.filter

        # Manually add the element "10"
        hash_k0 = mmh3.hash(str(elem_to_add), 0) % bf.m
        hash_k1 = mmh3.hash(str(elem_to_add), 1) % bf.m
        bits[hash_k0] = 1
        bits[hash_k1] = 1

        # Add the element "10" to the object by using the add() method
        bf.add(elem_to_add)

        self.assertEqual(bits, bf.filter)

    def test_check_membership_true(self):
        expected = True
        elem_to_add = "1"
        bf = BloomFilter(m=5, k=2)
        bf.add(elem_to_add)
        actual = bf.check_membership(elem_to_add)
        self.assertEqual(expected, actual)

    def test_check_membership_false(self):
        expected = False
        bf = BloomFilter(m=5, k=2)

        # Add one element, then check for a different element
        bf.add(10)
        actual = bf.check_membership(3)
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()

import mmh3
import math


class BloomFilter(object):
    def __init__(self, m=None, p=0.01, k=None, n=None):
        self.m = m      # Number of bits in the array
        self.p = p      # False positive probability
        self.k = k      # Number of hash functions
        self.n = n      # Number of elements added to the set

        if self.m is None and self.n is not None:
            self.set_optimal_m()
        elif self.m is None and self.n is None:
            self.m = 1000
        if self.k is None:
            self.set_optimal_k()

        self.filter = []
        for bit in range(0, self.m):
            self.filter.append(False)

    def set_optimal_k(self):
        self.k = int(-1 * math.log(self.p) / float(math.log(2)))

    def set_optimal_m(self):
        self.m = int(-1 * self.n * math.log(self.p) / float(math.pow(math.log(2), 2)))

    def compute_hash(self, k, elem):
        # Run elem through the kth hash function and return the value
        return mmh3.hash(str(elem), k) % self.m

    def add(self, elem):
        # Pass to each of the k hash functions to get k array positions
        for f in range(0, self.k):
            # Set bit at all these positions to 1
            self.filter[self.compute_hash(f, elem)] = 1

    def check_membership(self, elem):
        # Pass to each of the k hash functions
        for bit in range(0, self.k):
            # If any bits at these positions is 0, element is not in the set
            if self.filter[self.compute_hash(bit, elem)] == 0:
                return False
        return True

if __name__ == "__main__":
    bloomfilter = BloomFilter(n=3)

    # Basic tests
    bloomfilter.add(5)
    bloomfilter.add(6)
    bloomfilter.add(7)

    print(bloomfilter.check_membership(5))
    print(bloomfilter.check_membership(6))
    print(bloomfilter.check_membership(7))
    print(bloomfilter.check_membership(8))

    # Force false positives
    for i in range(10):
        bloomfilter.add(i)

    for i in range(100):
        print(str(i) + ": " + str(bloomfilter.check_membership(i)))

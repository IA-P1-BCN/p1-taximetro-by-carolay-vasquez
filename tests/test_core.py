import unittest
 
from taximetro import core
 
 
class TestRateForState(unittest.TestCase):
 
    def test_rate_when_stopped(self):
        self.assertEqual(core.rate_for_state(core.STATE_STOPPED), 0.02)
 
    def test_rate_when_moving(self):
        self.assertEqual(core.rate_for_state(core.STATE_MOVING), 0.05)
 
    def test_unknown_state_raises_value_error(self):
        # A typo or a bad value should fail loudly, not silently
        # compute a wrong fare.
        with self.assertRaises(ValueError):
            core.rate_for_state("parked")  # not a valid state
 
 
class TestFareForSegment(unittest.TestCase):
 
    def test_ten_seconds_stopped(self):
        self.assertAlmostEqual(
            core.fare_for_segment(core.STATE_STOPPED, 10), 0.20
        )
 
    def test_ten_seconds_moving(self):
        self.assertAlmostEqual(
            core.fare_for_segment(core.STATE_MOVING, 10), 0.50
        )
 
    def test_zero_seconds_accrues_nothing(self):
        self.assertEqual(
            core.fare_for_segment(core.STATE_MOVING, 0), 0.0
        )
 
    def test_three_seconds_stopped(self):
        # 3s stopped at 0.02 EUR/s = 0.06 EUR
        self.assertAlmostEqual(
            core.fare_for_segment(core.STATE_STOPPED, 3), 0.06
        )
 
    def test_fractional_seconds(self):
        # 2.5s stopped at 0.02 EUR/s = 0.05 EUR
        self.assertAlmostEqual(
            core.fare_for_segment(core.STATE_STOPPED, 2.5), 0.05
        )
 
    def test_unknown_state_propagates_error(self):
        with self.assertRaises(ValueError):
            core.fare_for_segment("parked", 10)
 
 
if __name__ == "__main__":
    unittest.main()

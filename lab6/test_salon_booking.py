import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

# Example test cases:
def test_within_included_time():
    assert extra_time_charge("haircut", 20, "junior", False) == 0

def test_can_book():
    assert can_book(2, 1, False) is True

# Write the rest of the test cases so that the code is 90-100% covered.

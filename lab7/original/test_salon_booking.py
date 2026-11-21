from hypothesis import given, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill

@given(st.text() | st.none())
def test_parse_booking_no_crash(s):

@given(st.text() | st.none())
def test_duration_average_no_crash(s):

@given(st.text() | st.none())
def test_payable_bill_no_crash(s):

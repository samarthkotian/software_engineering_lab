"""Same property tests run against the original and repaired application.

Invalid inputs return None. Valid business results retain the supplied API.
"""
import math
import pytest
from hypothesis import given, settings, strategies as st
from salon_booking import parse_booking, duration_average, payable_bill

settings.register_profile('lab', max_examples=300, derandomize=True, deadline=None, database=None)
settings.load_profile('lab')

arbitrary = st.one_of(st.none(), st.text(), st.integers(), st.floats(),
                      st.booleans(), st.lists(st.integers(),max_size=5),
                      st.dictionaries(st.text(max_size=5),st.integers(),max_size=3))

@given(arbitrary)
def test_parse_booking_no_crash(value):
    result = parse_booking(value)
    assert result is None or (result[0] in {'Haircut','Colour','Spa'} and
                              math.isfinite(result[1]) and result[1] >= 0)

@given(arbitrary)
def test_duration_average_no_crash(value):
    result = duration_average(value)
    assert result is None or (isinstance(result,int) and result >= 0)

@given(arbitrary)
def test_payable_bill_no_crash(value):
    result = payable_bill(value)
    assert result is None or (math.isfinite(result) and result >= 0)

@given(st.sampled_from(['haircut','colour','spa']),st.integers(0,1000000))
def test_valid_booking(service,minutes):
    assert parse_booking(f' {service.upper()} : {minutes} ') == (service.title(),float(minutes))

@given(st.lists(st.integers(0,1000000),min_size=1,max_size=40))
def test_average_matches_integer_mean(values):
    result = duration_average(','.join(map(str,values)))
    assert result == sum(values)//len(values)
    assert min(values) <= result <= max(values)

@given(st.integers(0,1000000),st.integers(0,1000000))
def test_bill_matches_formula(bill,discount):
    assert payable_bill(f'{bill}|{discount}') == pytest.approx(max(bill*1.18-discount,0))

@pytest.mark.parametrize('value', [None,'','haircut','haircut:1:2','unknown:3',
    'haircut:-1','haircut:nan','spa:inf',[],True,'spa:'+('9'*5000)])
def test_invalid_bookings(value):
    assert parse_booking(value) is None

@pytest.mark.parametrize('value', [None,'','1,,3','1,','-1,2','1.5,2','nan','inf',
    'x',{},False,'9'*5000])
def test_invalid_averages(value):
    assert duration_average(value) is None

@pytest.mark.parametrize('value', [None,'','1','1|2|3','-1|0','1|-1','nan|0',
    'inf|0','0|nan',[],True,'1.7e308|0'])
def test_invalid_bills(value):
    assert payable_bill(value) is None

def test_documented_examples():
    assert parse_booking('haircut:45') == ('Haircut',45.0)
    assert duration_average('30,45,60') == 45
    assert payable_bill('800|100') == 844.0
    assert payable_bill('10|100') == 0

"""Line coverage: expected values, invalid inputs, and all executable lines."""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

@pytest.mark.parametrize('service,minutes,level,member,expected', [
    ('haircut',20,'junior',False,0),
    ('haircut',45,'junior',True,0),
    ('haircut',50,'junior',True,50),
    ('colour',70,'senior',False,180),
    ('spa',151,'senior',True,1830),
    ('haircut',91,'junior',False,1098),
])
def test_charges(service,minutes,level,member,expected):
    assert extra_time_charge(service,minutes,level,member) == expected

@pytest.mark.parametrize('service,minutes,message', [
    ('unknown',30,'unknown service'),('haircut',-1,'invalid duration')])
def test_invalid(service,minutes,message):
    with pytest.raises(ValueError, match=message):
        extra_time_charge(service,minutes,'junior',False)

@pytest.mark.parametrize('party,services,walk_in,expected', [
    (2,1,True,True),(5,1,False,False),(4,2,False,True)])
def test_bookings(party,services,walk_in,expected):
    assert can_book(party,services,walk_in) is expected

@pytest.mark.parametrize('early,colour,weekend,expected', [
    (20,True,True,'open'),(0,False,False,'late'),(-11,False,False,'closed')])
def test_arrival(early,colour,weekend,expected):
    assert arrival_status(early,colour,weekend) == expected

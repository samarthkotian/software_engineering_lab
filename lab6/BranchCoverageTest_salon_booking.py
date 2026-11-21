"""Branch coverage: both outcomes and boundary values of each decision."""
import pytest
from salon_booking import extra_time_charge, can_book, arrival_status

@pytest.mark.parametrize('service,included', [('haircut',30),('colour',60),('spa',90)])
@pytest.mark.parametrize('member', [False,True])
@pytest.mark.parametrize('level', ['junior','senior'])
@pytest.mark.parametrize('extra', [0,1,60,61])
def test_charge_boundaries(service,included,member,level,extra):
    allowance = included + (15 if member and service != 'spa' else 0)
    rate = {'junior':10,'senior':18}[level]
    if extra > 60:
        rate += {'junior':8,'senior':12}[level]
    assert extra_time_charge(service,allowance+extra,level,member) == extra*rate

@pytest.mark.parametrize('service,minutes,message', [
    ('invalid',0,'unknown service'),('haircut',-1,'invalid duration')])
def test_rejections(service,minutes,message):
    with pytest.raises(ValueError, match=message):
        extra_time_charge(service,minutes,'junior',False)

@pytest.mark.parametrize('party,services,walk_in,expected', [
    (2,99,True,True),(3,1,True,False),(4,2,False,True),
    (5,1,False,False),(4,3,False,False)])
def test_booking_decisions(party,services,walk_in,expected):
    assert can_book(party,services,walk_in) is expected

@pytest.mark.parametrize('colour,weekend,cutoff', [
    (False,False,5),(True,False,10),(False,True,15),(True,True,20)])
@pytest.mark.parametrize('offset,expected', [(0,'open'),(-1,'late'),(-15,'late'),(-16,'closed')])
def test_arrival_boundaries(colour,weekend,cutoff,offset,expected):
    assert arrival_status(cutoff+offset,colour,weekend) == expected

import pytest
from src.manager import Manager
from src.models import Parameters




from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0

def test_create_apartment_settlement():
    from src.manager import Manager
    from src.models import Parameters, Bill
    
    manager = Manager(Parameters())
    manager.apartments = {'A1': 'Mieszkanie 1', 'A2': 'Mieszkanie 2'}
    
    manager.bills = [
        Bill(apartment='A1', settlement_year=2024, settlement_month=5, amount_pln=100.0, type='rent', date_due='2024-05-10'),
        Bill(apartment='A1', settlement_year=2024, settlement_month=5, amount_pln=200.0, type='electricity', date_due='2024-05-15'),
        Bill(apartment='A1', settlement_year=2024, settlement_month=6, amount_pln=150.0, type='rent', date_due='2024-06-10')
    ]
    
    settlement_a1_may = manager.create_apartment_settlement('A1', 2024, 5)
    
    assert settlement_a1_may is not None
    assert settlement_a1_may.apartment == 'A1'
    assert settlement_a1_may.year == 2024
    assert settlement_a1_may.month == 5
    assert settlement_a1_may.balance == -300.0
    
    settlement_a1_jan = manager.create_apartment_settlement('A1', 2024, 1)
    
    assert settlement_a1_jan is not None
    assert settlement_a1_jan.apartment == 'A1'
    assert settlement_a1_jan.month == 1
    assert settlement_a1_jan.balance == 0.0
    
    settlement_a2 = manager.create_apartment_settlement('A2', 2024, 5)
    
    assert settlement_a2 is not None
    assert settlement_a2.balance == 0.0
    
    settlement_invalid = manager.create_apartment_settlement('A99', 2024, 5)
    assert settlement_invalid is None



import pytest
from src.manager import Manager
from src.models import Parameters

# Klasa pomocnicza do zasymulowania struktury rachunku z Twoich modeli
class MockBill:
    def __init__(self, apartment, year, month, amount):
        self.apartment = apartment
        self.settlement_year = year
        self.settlement_month = month
        self.amount_pln = amount

def test_get_apartment_costs_integration():
    parameters = Parameters()
    manager = Manager(parameters)
    manager.apartments = {'A1': 'Dummy Apartment Data'}
    
    manager.bills = [
        MockBill('A1', 2024, 3, 200.0),   
        MockBill('A1', 2024, 3, 250.0),   
        MockBill('A1', 2024, 4, 100.0),   
        MockBill('A2', 2024, 3, 300.0)    
    ]
    assert manager.get_apartment_costs('B99', 2024, 3) is None

    assert manager.get_apartment_costs('A1', 2024, 5) == 0.0

    assert manager.get_apartment_costs('A1', 2024, 3) == 450.0
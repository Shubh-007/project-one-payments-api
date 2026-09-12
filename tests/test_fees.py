from src.fees import interchange_fee
 
def test_fee_on_1000():
    assert interchange_fee(1000) == 13.50
 
def test_fee_on_250():
    assert interchange_fee(250) == 5.25

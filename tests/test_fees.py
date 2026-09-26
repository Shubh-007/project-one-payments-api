from src.fees import interchange_fee, InvalidAmountError

def test_fee_on_1000():
    assert interchange_fee(1000) == 13.50

def test_fee_on_250():
    assert interchange_fee(250) == 5.25

def test_fee_on_boundary_values():
    """Test edge cases that expose floating-point precision issues."""
    assert interchange_fee(33) == 2.86  # 33 * 0.011 + 2.50 = 2.863 -> 2.86
    assert interchange_fee(67) == 3.24  # 67 * 0.011 + 2.50 = 3.237 -> 3.24
    assert interchange_fee(99) == 3.59  # 99 * 0.011 + 2.50 = 3.589 -> 3.59

def test_fee_on_zero():
    """Test minimum amount."""
    assert interchange_fee(0) == 2.50

def test_fee_on_large_amount():
    """Test large transaction."""
    assert interchange_fee(100000) == 1102.50  # 100000 * 0.011 + 2.50 = 1102.50


def test_fee_rejects_negative_amount():
    """Test that negative amounts are rejected."""
    try:
        interchange_fee(-100)
        assert False, "Should have raised InvalidAmountError"
    except InvalidAmountError as e:
        assert "negative" in str(e).lower()


def test_fee_rejects_none():
    """Test that None is rejected."""
    try:
        interchange_fee(None)
        assert False, "Should have raised InvalidAmountError"
    except InvalidAmountError as e:
        assert "None" in str(e)


def test_fee_rejects_non_numeric():
    """Test that non-numeric input is rejected."""
    try:
        interchange_fee("not a number")
        assert False, "Should have raised InvalidAmountError"
    except InvalidAmountError:
        pass

from src.settlement.rules import settlement_window
from src.legacy.settlement_core import settle
from src.fees import interchange_fee


def test_settlement_window_india():
    """Test T+1 window for India (IN) region."""
    assert settlement_window("IN") == "T+1"


def test_settlement_window_default():
    """Test T+2 default window for non-India regions."""
    assert settlement_window("US") == "T+2"
    assert settlement_window("UK") == "T+2"
    assert settlement_window("AU") == "T+2"


def test_settlement_window_empty_region():
    """Test default window for empty region."""
    assert settlement_window("") == "T+2"


def test_settlement_window_case_sensitive():
    """Test that region lookup is case-sensitive."""
    assert settlement_window("in") == "T+2"  # lowercase "in" returns default
    assert settlement_window("IN") == "T+1"  # uppercase "IN" returns T+1


def test_settle_returns_settled():
    """Test that settle() returns the expected stub response."""
    batch = [
        {"amount": 1000, "currency": "INR"},
        {"amount": 500, "currency": "INR"}
    ]
    result = settle(batch)
    assert result == "settled"


def test_e2e_settlement_pipeline():
    """End-to-end test: fees + settlement_window + settle integration."""
    amount = 5000
    region = "IN"

    # Calculate fee for the amount
    fee = interchange_fee(amount)
    assert fee == 57.50  # 5000 * 0.011 + 2.50 = 57.50

    # Determine settlement window for region
    window = settlement_window(region)
    assert window == "T+1"

    # Execute settlement
    batch = [{"amount": amount, "fee": fee, "region": region}]
    settlement_result = settle(batch)
    assert settlement_result == "settled"


def test_e2e_settlement_default_region():
    """End-to-end test with default region (T+2)."""
    amount = 1000
    region = "US"

    fee = interchange_fee(amount)
    assert fee == 13.50

    window = settlement_window(region)
    assert window == "T+2"

    batch = [{"amount": amount, "fee": fee, "region": region}]
    result = settle(batch)
    assert result == "settled"


def test_e2e_multi_transaction_batch():
    """End-to-end test with multiple transactions."""
    transactions = [
        {"amount": 1000, "region": "IN"},
        {"amount": 5000, "region": "US"},
        {"amount": 250, "region": "IN"}
    ]

    # Calculate fees for each transaction
    fees = [interchange_fee(t["amount"]) for t in transactions]
    assert fees[0] == 13.50   # 1000 * 0.011 + 2.50
    assert fees[1] == 57.50   # 5000 * 0.011 + 2.50
    assert fees[2] == 5.25    # 250 * 0.011 + 2.50

    # Determine settlement windows
    windows = [settlement_window(t["region"]) for t in transactions]
    assert windows == ["T+1", "T+2", "T+1"]

    # Execute batch settlement
    batch = [
        {**t, "fee": fee, "window": window}
        for t, fee, window in zip(transactions, fees, windows)
    ]
    result = settle(batch)
    assert result == "settled"

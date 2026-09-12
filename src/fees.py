def interchange_fee(amount):
    """UniPay spec: 1.10% of amount + Rs 2.50 flat, rounded to 2 decimals."""
    return round(amount * 0.11 + 2.50, 2)  # BUG: should be 0.011, not 0.11

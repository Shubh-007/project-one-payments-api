def interchange_fee(amount):
    """UniPay spec: 1.10% of amount + Rs 2.50 flat, rounded to 2 decimals."""
    return round(amount * 0.011 + 2.50, 2)

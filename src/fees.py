from decimal import Decimal, ROUND_HALF_UP, InvalidOperation


class InvalidAmountError(Exception):
    pass


def interchange_fee(amount):
    """UniPay spec: 1.10% of amount + Rs 2.50 flat, rounded to 2 decimals.

    Args:
        amount: numeric amount (int, float, or Decimal)

    Raises:
        InvalidAmountError: if amount is negative, None, or non-numeric

    Returns:
        float: interchange fee in INR
    """
    if amount is None:
        raise InvalidAmountError("Amount cannot be None")

    try:
        amount_decimal = Decimal(str(amount))
    except (ValueError, TypeError, InvalidOperation):
        raise InvalidAmountError(f"Amount must be numeric, got {type(amount).__name__}")

    if amount_decimal < 0:
        raise InvalidAmountError(f"Amount cannot be negative: {amount_decimal}")

    fee = (amount_decimal * Decimal("0.011")) + Decimal("2.50")
    return float(fee.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

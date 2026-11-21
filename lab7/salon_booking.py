"""Salon input helpers: invalid input returns None instead of crashing.
Durations and money must be finite and nonnegative. Preserve the original
floor-average and 18% tax formula. Limit text to 10000 characters.
"""
import math

SERVICES = {'haircut', 'colour', 'spa'}
MAX_INPUT_LENGTH = 10000


def _parts(text, separator, expected=None):
    if not isinstance(text, str) or not text.strip() or len(text) > MAX_INPUT_LENGTH:
        return None
    parts = [part.strip() for part in text.split(separator)]
    if any(not part for part in parts):
        return None
    if expected is not None and len(parts) != expected:
        return None
    return parts


def _nonnegative_float(value):
    try:
        number = float(value)
    except (ValueError, OverflowError):
        return None
    if not math.isfinite(number) or number < 0:
        return None
    return number


def parse_booking(text):
    """Return (service title, minutes), or None for invalid booking text."""
    parts = _parts(text, ':', 2)
    if parts is None:
        return None
    service, raw_minutes = parts
    if service.lower() not in SERVICES:
        return None
    minutes = _nonnegative_float(raw_minutes)
    if minutes is None:
        return None
    return service.title(), minutes


def duration_average(durations_csv):
    """Return the floor mean of nonnegative integer durations, or None."""
    parts = _parts(durations_csv, ',')
    if parts is None:
        return None
    try:
        values = [int(part) for part in parts]
    except (ValueError, OverflowError):
        return None
    if any(value < 0 for value in values):
        return None
    return sum(values) // len(values)


def payable_bill(text):
    """Apply 18% tax then discount, with a zero floor; invalid input -> None."""
    parts = _parts(text, '|', 2)
    if parts is None:
        return None
    bill, discount = [_nonnegative_float(part) for part in parts]
    if bill is None or discount is None:
        return None
    total = bill * 1.18 - discount
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    """Report invalid data and continue to the next prompt."""
    prompts = [
        ('parse_booking', 'Enter service:duration in min (e.g. haircut:45): ',
         parse_booking, 'Service and Duration:'),
        ('duration_average', 'Enter durations as CSV (e.g. 30,45,60): ',
         duration_average, 'Average Duration:'),
        ('payable_bill', 'Enter bill|discount (e.g. 800|100): ',
         payable_bill, 'Payable Bill:'),
    ]
    for name, prompt, function, label in prompts:
        print(f'\n==== Running {name} ====')
        try:
            result = function(input(prompt))
        except (EOFError, KeyboardInterrupt):
            print('\nInput cancelled.')
            return
        if result is None:
            print('Invalid input. Use the format shown, with finite nonnegative numbers.')
        else:
            print(label, result)


if __name__ == '__main__':
    main()

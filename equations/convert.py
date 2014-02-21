from decimal import Decimal

'''Common conversions performed in a nutrition assessment between
imperial and metric units'''


def to_inches(height_cm):
    return Decimal(height_cm) / Decimal('2.54')


def to_pounds(weight_kg):
    return Decimal(weight_kg) * Decimal('2.2')


def to_kilograms(weight_lbs):
    return Decimal(weight_lbs) / Decimal('2.2')


def to_centimeters(height_in):
    return Decimal(height_in) * Decimal('2.54')


def to_celcius(f):
    return (Decimal(f) - Decimal('32.0')) * (Decimal('5') / Decimal('9'))


def to_decimal(value):
    return Decimal(str(value))

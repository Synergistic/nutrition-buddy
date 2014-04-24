import decimal

'''Common conversions performed in a nutrition assessment between
imperial and metric units'''

def to_inches(height_cm):
    return to_decimal(height_cm) / decimal.Decimal('2.54')

def to_pounds(weight_kg):
    return to_decimal(weight_kg) * decimal.Decimal('2.2')

def to_kilograms(weight_lbs):
    return to_decimal(weight_lbs) / decimal.Decimal('2.2')

def to_centimeters(height_in):
    return to_decimal(height_in) * decimal.Decimal('2.54')

def to_celcius(f):
    return (to_decimal(f) - decimal.Decimal('32.0')) * (decimal.Decimal('5') / decimal.Decimal('9'))

def to_decimal(value):
    return decimal.Decimal(str(value))
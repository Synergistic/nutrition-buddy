from decimal import *


def body_mass_index(weight_kg, height_cm):
    """
    Calculates Body Mass Index(BMI):
    bmi = (weight(kg) / (height(meters)**2))
    Then determines the appropriate category
    """
    bmi = float(weight_kg / ((height_cm / 100) ** 2))
    
    if bmi < 18.50:
        category = "Underweight"
    elif bmi >= 18.5 and bmi <= 24.99:
        category = "Normal"
    elif bmi > 24.99 and bmi <= 29.99:
        category = "Overweight"
    elif bmi > 29.99 and bmi <= 34.99:
        category = "Obese I"
    elif bmi > 34.99 and bmi <= 39.99:
        category = "Obese II"
    elif bmi > 39.99:
        category = "Obese III"
        
    return Decimal(str(bmi)), category

def ideal_body_weight(weight_lbs, height_in, gender):
    """
    Calculates IBW based on Hamwi method;
    Males: 106 + 6x
    Females: 100 + 5x
    X = number of inches over 60inches for height
    """
    if height_in >= 60:
        inches_over_sixty = height_in - 60
        if gender == 'male':
            ibw = (inches_over_sixty * 6) + 106
        elif gender == 'female':
            ibw = (inches_over_sixty * 5) + 100
            
    elif height_in < 60:
        ibw_in = 60 - height_in
        if gender == 'male':
            ibw = 106 - (ibw_in * 3)
        elif gender == 'female':
            ibw = 100 - (ibw_in * (Decimal('2.5')))
            
    percent_ibw = (weight_lbs / ibw) * Decimal('100.0')
    ibw_kg = ibw / Decimal('2.2')
    return ibw, ibw_kg, percent_ibw

def adjust_body_weight(ibw_kg, weight_kg):
    return (((weight_kg - ibw_kg) * Decimal('0.25')) + ibw_kg)
    
def mifflin(weight_kg, height_cm, gender, age):
    """
    Calculates caloric needs based on Mifflin-St.Jeor Equation
    Males: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age(yrs)) + 5.0
    Females: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age(yrs)) - 161
    """
    if gender.lower() == "male":
        rmr = (Decimal('9.99') * weight_kg) + (Decimal('6.25') * height_cm) \
          - (Decimal('4.92') * age) + Decimal('5.0')

    elif gender.lower() == "female":
        rmr = (Decimal('9.99') * weight_kg) + (Decimal('6.25') * height_cm) \
              - (Decimal('4.92') * age) - Decimal('161.0')
    return rmr


def pennstate(weight_kg, height_cm, gender, age, temp_celcius, vent_rate):
    """
    Calculates caloric needs based on Penn St. Equation
    PSU2010: RMR = Mifflin(0.71) + Ve(64) + Tmax(85) - 3085
    PSU2003B: RMR = Mifflin(0.96) + Ve(31) + Tmax(167) - 6212
    2010 is used if BMI >29.9
    """
    equation = ""
    base_needs = mifflin(weight_kg, height_cm, gender, age)
    
    if (bodymassindex(weight_kg, height_cm)[0] > 29.9) and (age > 59):
        rmr = base_needs * Decimal('0.71') + Decimal(vent_rate) * Decimal('64.0')\
              + temp_celcius * Decimal('85') - Decimal('3085')
        equation = "PennSt(2010)"
        
    else:
        rmr = base_needs * Decimal('0.96') + Decimal(vent_rate) * Decimal('31.0')\
              + temp_celcius * Decimal('167') - Decimal('6212')
        equation = "PennSt(2003B)"
    return rmr, equation

def protein(pro_range, weight_kg):
    """
    Calculates protein needs based on a given protein/kg or range
    """
    if len(pro_range) > 1:
        lower_daily_protein = weight_kg * pro_range[0]
        upper_daily_protein = weight_kg * pro_range[1]
        return lower_daily_protein, upper_daily_protein
    
    elif len(pro_range) == 1:
        daily_protein = weight_kg * pro_range
        return daily_protein

def fluid(weight_kg, age):
    """
    Calculates daily fluid needs
    75 years old and above = 25cc/kg
    Under 75 years = 30cc/kg
    """
    if age >= 75:
        daily_fluid = weight_kg * 25
    elif age < 75:
        daily_fluid = weight_kg * 30
    return daily_fluid

def calories_per_kg(weight_kg, calorie_needs):
    """
    Calculates calories per kilogram of body weight
    """
    cal_per_kg = Decimal(str(calorie_needs)) / Decimal(str(weight_kg))
    return cal_per_kg

def cm_to_inch(height_cm):
    return height_cm / Decimal('2.54')

def kg_to_lbs(weight_kg):
	return weight_kg * Decimal('2.2')
	
def lbs_to_kg(weight_lbs):
    return weight_lbs / Decimal('2.2')

def inch_to_cm(height_in):
    return height_in * Decimal('2.54')

def fahren_to_c(f):
    return (f - Decimal('32.0')) * (Decimal('5') / Decimal('9'))

def celcius_to_f(c):
    pass
    
    
    

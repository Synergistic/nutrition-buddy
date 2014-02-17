from decimal import Decimal

def body_mass_index(weight_kg, height_cm):
    """
    Calculates Body Mass Index(BMI):
    bmi = (weight(kg) / (height(meters)**2))
    Then determines the appropriate category
    """
    
    bmi = Decimal( weight_kg ) / ( ( Decimal(height_cm) / 100 ) ** 2 )
    
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
        
    return bmi, category

def ideal_body_weight(weight_lbs, height_in, gender):
    """
    Calculates IBW  in pounds based on Hamwi method;
    Males: 106 + 6x
    Females: 100 + 5x
    X = number of inches over 60inches for height
    """
    if height_in >= 60:
        inches_over_sixty = height_in - 60
        if gender.lower() == 'male':
            ibw = (inches_over_sixty * 6) + 106
        elif gender.lower() == 'female':
            ibw = (inches_over_sixty * 5) + 100
            
    elif height_in < 60:
        ibw_in = 60 - height_in
        if gender.lower() == 'male':
            ibw = 106 - (ibw_in * 3)
        elif gender.lower() == 'female':
            ibw = 100 - (ibw_in * (Decimal('2.5')))
    return ibw

def percent_ideal_body_weight(weight_kg, ibw_kg):  
    return ( Decimal(weight_kg) / Decimal(ibw_kg) ) * Decimal('100.0')
    
def adjust_body_weight(ibw_kg, weight_kg):
    return (((Decimal(weight_kg) - Decimal(ibw_kg)) * Decimal('0.25')) + Decimal(ibw_kg))

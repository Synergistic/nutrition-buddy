from decimal import Decimal


def mifflin(weight_kg, height_cm, gender, age):
    '''Caloric needs based on Mifflin-St.Jeor Equation
    Males: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age) + 5.0
    Females: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age) - 161'''
    if gender.lower() == "male":
        energy = ((Decimal('9.99') * Decimal(weight_kg)) +
                 (Decimal('6.25') * Decimal(height_cm)) -
                 (Decimal('4.92') * Decimal(age)) + Decimal('5.0'))

    elif gender.lower() == "female":
        energy = ((Decimal('9.99') * Decimal(weight_kg)) +
                 (Decimal('6.25') * Decimal(height_cm)) -
                 (Decimal('4.92') * Decimal(age)) - Decimal('161.0'))
    return energy


def pennstate(base_energy, bmi, gender, age, temp_celcius, vent_rate):
    '''Calculates caloric needs based on Penn St. Equation
    PSU2010: RMR = Mifflin(0.71) + Ve(64) + Tmax(85) - 3085
    PSU2003B: RMR = Mifflin(0.96) + Ve(31) + Tmax(167) - 6212
    2010 is used if BMI >29.9'''
    if bmi > 29.9 and age > 59:
        #PennSt(2010)
        energy = (base_energy * Decimal('0.71') + Decimal(vent_rate) *
                  Decimal('64.0') + Decimal(temp_celcius) *
                  Decimal('85') - Decimal('3085'))
    else:
        #PennSt(2003B)
        energy = (base_energy * Decimal('0.96') + Decimal(vent_rate) *
                  Decimal('31.0') + Decimal(temp_celcius) *
                  Decimal('167') - Decimal('6212'))
    return energy


def protein(pro_range, weight_kg):
    '''Calculates protein needs based on a given protein/kg or range'''
    if len(pro_range) > 1:
        lower_daily_protein = weight_kg * pro_range[0]
        upper_daily_protein = weight_kg * pro_range[1]
        return lower_daily_protein, upper_daily_protein
    elif len(pro_range) == 1:
        daily_protein = weight_kg * pro_range
        return daily_protein


def fluid(weight_kg, age):
    '''Calculates daily fluid needs
    75 years old and above = 25cc/kg
    Under 75 years = 30cc/kg'''
    if age >= 75:
        daily_fluid = weight_kg * 25
    elif age < 75:
        daily_fluid = weight_kg * 30
    return daily_fluid


def calories_per_kg(weight_kg, calorie_needs):
    #Calculates calories per kilogram of body weight
    cal_per_kg = Decimal(str(calorie_needs)) / Decimal(str(weight_kg))
    return cal_per_kg

import equations.convert as convert
import equations.anthropometrics as anthro
import equations.nutrientneeds as nutcalc
from decimal import InvalidOperation

def initial_data(ht_value, ht_unit, wt_value, wt_unit, uniques, **kwargs):
    '''Converts appropriate data values, stores in dictionary and utilizes them
    to calculate various data points such as body mass index, ideal body weight,
    energy needs, etc. Returns a dictionary containing all applicable information.'''
    try:
        kwargs['age'] = int(kwargs['age'])
        weights_and_heights = conversions(ht_value, ht_unit, 
                                        wt_value, wt_unit)
    except (InvalidOperation, TypeError, ValueError):
        return 0
    d = kwargs.copy()
    d.update(weights_and_heights)
    
    #determine, bmi, ibw, %ibw, and abw if necessary
    d['bmi'] = anthro.body_mass_index(d['kg'], d['cm'])
    d['ibw_lbs'] = anthro.ideal_body_weight(d['lbs'], d['in'], d['sex'])
    d['ibw_kg'] = convert.to_kilograms(d['ibw_lbs'])
    d['%ibw'] = anthro.percent_ideal_body_weight(d['kg'], d['ibw_kg'])
    if d['%ibw'] >= 125.0:
	    d['abw'] = anthro.adjust_body_weight(d['ibw_kg'], d['kg'])
            d['fluid'] = nutcalc.fluid(d['abw'], d['age'])
    else:
	    d['abw'] = 'N/A'
            d['fluid'] = nutcalc.fluid(d['kg'], d['age'])
            
    #determine energy needs using appropriate equation
    d['calories'] = energy_needs(d, uniques)
    return d
    
def energy_needs(d, eq_uniques):
    #determine base energy needs using mifflin
    needs = nutcalc.mifflin(d['kg'], d['cm'], d['sex'], d['age'])
    
    if 'Penn' in eq_uniques[0]:
    #if using PennSt, we need to get the temperature in celcius
        if eq_uniques[2] == 'F': 
            tmax = convert.to_celcius(eq_uniques[1])
        else: 
            tmax = eq_uniques[1]
        #then we use the base needs from above, max temp, and ventilation rate
	    needs = nutcalc.pennstate(needs, d['bmi'], d['sex'], d['age'], tmax, 
                                vent_rate=eq_uniques[3])
    else: #if just using mifflin, we need to add in an activity/stress factor
        needs *= convert.to_decimal(eq_uniques[2])
        needs *= convert.to_decimal(eq_uniques[1])
    return needs
      
def conversions(ht_value, start_ht_unit, wt_value, start_wt_unit):
    new_values = {}
    if start_ht_unit == 'cm': #convert to inches
        new_values['cm'] = convert.to_decimal(ht_value)
        new_values['in'] = convert.to_inches(ht_value) 
    elif start_ht_unit == 'in': #convert to centimetres
        new_values['in']  = convert.to_decimal(ht_value)
        new_values['cm'] = convert.to_centimeters(ht_value)

    if start_wt_unit == 'kg': #convert to pounds
        new_values['kg'] = convert.to_decimal(wt_value)
        new_values['lbs'] =convert.to_pounds(wt_value)    
    elif start_wt_unit == 'lbs': #convert to kilograms
        new_values['lbs'] =convert.to_decimal(wt_value)
        new_values['kg'] = convert.to_kilograms(wt_value)
    return new_values
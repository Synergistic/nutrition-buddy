import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc
from decimal import Decimal



def calculations(height, height_unit, weight, weight_unit, age, sex, equation, *args):
    '''Method to compute all necessary information and convert'''
    
    d = {}
    
    #convert to opposite units
    anthropometrics = conversions(height, height_unit, weight, weight_unit)
    d['cm'] = anthropometrics[0]
    d['kg'] = anthropometrics[1]
    d['in'] = anthropometrics[2]
    d['lbs'] = anthropometrics[3]
    d['age'] = int(age)
    d['sex'] = sex.lower()
    
    #determine bmi
    d['bmi'] = anthro.body_mass_index( d['kg'], d['cm'] )
    
    #determine ibw and %ibw
    d['ibw_lbs'] = anthro.ideal_body_weight(d['lbs'], d['in'], d['sex'])
    d['ibw_kg'] = convert.to_kilograms(d['ibw_lbs'])
    d['%ibw'] = anthro.percent_ideal_body_weight(d['kg'], d['ibw_kg'])
	    
    #if currently more than 125% IBW, we need an adjusted body weight
    if d['%ibw'] >= 125.0:
	d['abw'] = anthro.adjust_body_weight( d['ibw_kg'], d['kg'] )
    else:
	d['abw'] = None
    return d
  
  

 
def energy_needs(d, equation):

    #determine energy needs using mifflin
    needs = nutcalc.mifflin(d['kg'], d['cm'], d['sex'], d['age'])
    
    if 'Penn' in equation: #if pennstate is selected, use above value to determine pennstate
	if d['temp_unit'] == 'F':
	    tmax = convert.to_celcius(d['tmax'])
	else:
	    tmax = d['tmax']
	    
	needs = nutcalc.pennstate(needs, d['bmi'], d['sex'], d['age'], tmax, d['ventilation'])
	
    return needs
      
def conversions(ht_value, start_ht_unit, wt_value, start_wt_unit):
    
    if start_ht_unit == 'cm': #convert to inches
        metric = [Decimal(ht_value)]
	imperial = [convert.to_inches(ht_value)]
		    
    elif start_ht_unit == 'in': #convert to centimetres
        imperial = [Decimal(ht_value)]
	metric = [convert.to_centimeters(ht_value)]

    
    if start_wt_unit == 'kg': #convert to pounds
	metric.append(Decimal(wt_value))
	imperial.append(convert.to_pounds(wt_value))
		    
    elif start_wt_unit == 'lbs': #convert to kilograms
	imperial.append(Decimal(wt_value))
	metric.append(convert.to_kilograms(wt_value))

    return metric + imperial
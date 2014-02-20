import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc

def initial_data(**kwargs):
    '''Method to compute all necessary information and convert'''
    
    #convert to opposite units
    weights_and_heights = conversions(
      kwargs.pop("ht_value"), kwargs.pop("ht_unit"), 
      kwargs.pop("wt_value"), kwargs.pop("wt_unit"))
    
    d = kwargs.copy()
    d.update(weights_and_heights)
    
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
	d['abw'] = 'N/A'
    return d
  
def energy_needs(d, args):
    #determine energy needs using mifflin
    needs = nutcalc.mifflin(d['kg'], d['cm'], d['sex'], d['age'])
    
    if 'Penn' in args[0]:
	if args[2] == 'F': tmax = convert.to_celcius(args[1])
	else: tmax = args[1]
	
	needs = nutcalc.pennstate(needs, d['bmi'], d['sex'], d['age'], tmax, vent_rate=args[3])
    else:needs *= convert.to_decimal(args[1])
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
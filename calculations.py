import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc

def initial_data(height, height_unit, weight, weight_unit, age, sex):
    '''Method to compute all necessary information and convert'''
    d = {}
    #convert to opposite units
    weights_and_heights = conversions(height, height_unit, weight, weight_unit)
    d['cm'] = weights_and_heights[0]
    d['kg'] = weights_and_heights[1]
    d['in'] = weights_and_heights[2]
    d['lbs'] = weights_and_heights[3]
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
    
    if start_ht_unit == 'cm': #convert to inches
        metric = [convert.to_decimal(ht_value)]
	imperial = [convert.to_inches(ht_value)]    
    elif start_ht_unit == 'in': #convert to centimetres
        imperial = [convert.to_decimal(ht_value)]
	metric = [convert.to_centimeters(ht_value)]

    if start_wt_unit == 'kg': #convert to pounds
	metric.append(convert.to_decimal(wt_value))
	imperial.append(convert.to_pounds(wt_value))	    
    elif start_wt_unit == 'lbs': #convert to kilograms
	imperial.append(convert.to_decimal(wt_value))
	metric.append(convert.to_kilograms(wt_value))

    return metric + imperial
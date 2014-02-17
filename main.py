
from kivy.app import App

import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc


from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

d = {} #This is where we'll store everything

class NutritionCalc(BoxLayout):
    '''Parent widget that holds all labels, text inputs, buttons, etc.'''
    
    title_text = "Nutrition Calculator"
    #values from the height, weight, age text inputs
    user_height   = ObjectProperty('')
    user_weight   = ObjectProperty('')
    user_age      = ObjectProperty('')
  
    #value from the height, weight, sex spinners
    height_unit = ObjectProperty('cm')
    weight_unit = ObjectProperty('kg')
    user_sex    = ObjectProperty('Male')

    
    def run_calculator(self):
        '''Run the calculator by initializing the data dic, gathering
        input from appropriate fields, computing necessary values, and
		finally building the pop up to display output'''

	self.clear_data()
	print 'Data cleared'
	self.collect_input()
	print 'Inputs collected'
	self.calculations()
	print 'Calculations done'
	self.output_popup()
	print 'Popup built'
		
    def clear_data(self):
        '''Method to (re)initialize the d dic'''
	for key in d:
	    d[key] = None
 
    def collect_input(self):
        '''Method to collect & organize the user entered d'''
        #height collection and storage
        d[self.height_unit] = convert.to_decimal(self.user_height)

        #weight collection and storage
        d[self.weight_unit] = convert.to_decimal(self.user_weight)

        #sex collection and storage
        d['age'] = int(self.user_age)

        #age collection and storage
        d['sex'] = self.user_sex.lower()
		
    def calculations(self):
        '''Method to compute all necessary information and convert'''
	
	#convert to opposite units
        self.conversions()
	
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
	
	#determine energy needs using appropriate equation
        self.energy_needs()
        
		
    def conversions(self):
	
        if self.weight_unit == 'kg': #convert to pounds
            d['lbs'] = convert.to_pounds(d['kg'])
			
        elif self.weight_unit == 'lbs': #convert to kilograms
            d['kg'] = convert.to_kilograms(d['lbs'])

        if self.height_unit == 'cm': #convert to inches
            d['in'] = convert.to_inches(d['cm'])
			
        elif self.height_unit == 'in': #convert to centimetres
            d['cm'] = convert.to_centimeters(d['in'])

    def output_popup( self ):
        '''Method to build a pop up for displaying output'''

        #button to close popup
        confirm_button = Button(text = 'Close', size_hint = (1, 0.25))
        
        #making the content based on input/output
        d_layout = self.make_content()

        #Add popup content and open it
        popup_content = BoxLayout( orientation = 'vertical' )
        popup_content.add_widget( d_layout )
        popup_content.add_widget( confirm_button )

        pop_window = Popup(title = self.title_text, size_hint = (0.95, 0.65), 
                            content = popup_content)

        confirm_button.bind(on_release = pop_window.dismiss)   
        pop_window.open()

    def make_content(self):
        '''Method to generate the content show in the popup window'''
        
        #display user input as metric units
        input_d = Label( 
        text = '   Metric:\n\nHeight: {0:.2f}cm\nWeight: {1:.2f}kg'.format( 
        d['cm'], d['kg'] ))
	
        #display user input as imperial units
        input_d_converted = Label(
        text = '  Imperial:\n\nHeight: {0:.2f}in\nWeight: {1:.2f}lbs'.format( 
        d['in'], d['lbs'] ) )
	
        #store the user input d labels in a box layout
        inputbox = BoxLayout(orientation = 'horizontal')
        inputbox.add_widget(input_d)
        inputbox.add_widget(input_d_converted)

        #the output calculations
        output_base_d = Label(text='''Calories: {4:.1f} ({5:.0f}kcal/kg)
BMI: {0:.2f} - {1}\nIBW: {2:.2f}kg ({3:.2f}%)'''.format( d['bmi'][0],
        d['bmi'][1], d['ibw_kg'], d['%ibw'], d['calories'], 
        (d['calories']/d['kg'])
        ))
	
        #if adjusted body weight applicable (>= 125% IBW ) add it in to the output
        if d['abw']:
            output_base_d.text = '''Calories: {4:.1f} ({5:.0f}kcal/kg)
BMI: {0:.2f} - {1}\nIBW: {2:.2f}kg ({3:.2f}%)
ABW: {6:.2f}kg'''.format( d['bmi'][0],
            d['bmi'][1], d['ibw_kg'], d['%ibw'], d['calories'], 
            (d['calories']/d['kg']), d['abw']
            )
    
        #Box layout to organize all input and output d
        d_layout = BoxLayout(orientation = 'vertical')
        d_layout.add_widget(inputbox)
        d_layout.add_widget(output_base_d)

        return d_layout
		
    def reset_fields(self):
        '''Method attached to the reset button to re-initialize all fields'''   
        self.user_height   = ''
        self.user_weight   = ''
        self.user_age      = ''
        self.height_unit   = 'cm'
        self.weight_unit   = 'kg'
        self.user_sex      = 'Male'
        self.stress_factor = '1.0'
        self.max_temp      = ''
        self.ventilation   = ''

class MifflinCalc(NutritionCalc):
    stress_factor = ObjectProperty('1.0')
    title_text = 'Mifflin St. Jeor Equation'

    def energy_needs(self):
        d['calories'] = \
        nutcalc.mifflin(d['kg'], d['cm'], d['sex'], d['age']) * convert.to_decimal(self.stress_factor)
	
class PennCalc(NutritionCalc):
    title_text = 'Penn State Equation'
    max_temp = ObjectProperty('')
    ventilation = ObjectProperty('')
    temp_unit = ObjectProperty('C')

    def energy_needs(self):
	tmax = self.max_temp
	if self.temp_unit == 'F':
	    tmax = convert.to_celcius(self.max_temp)
	    
	base_needs = nutcalc.mifflin(d['kg'], d['cm'], d['sex'], d['age'])
        d['calories'] = \
        nutcalc.pennstate(base_needs, d['bmi'], d['sex'], d['age'], tmax, self.ventilation)
  
class Widgets(TabbedPanel):
    '''Base tabbed panels for holding each calculator. Contains the welcome page as well.'''
    welcome_text = "Welcome to Nutrition Buddy\nI calculate things!\nSelect a calculator below to get started."
        
class NutritionApp(App):
    title = "Nutrition Buddy"
	
    def build(self):
        return Widgets()
		
    def on_pause(self):
        return True
		
if __name__ in ('__main__', '__android__'):
    NutritionApp().run()

	

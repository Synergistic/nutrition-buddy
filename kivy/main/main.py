from kivy.app import App
from nutcalc import *
from decimal import Decimal

from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

data = {} #This is where we'll store everything

Config.set( 'graphics', 'width', '360' )
Config.set( 'graphics', 'height', '640' )

class Widgets( BoxLayout ):
    '''Parent widget that holds all  labels, textinputs, buttons, etc.'''
  
    #values from the height textbox and spinner
    user_height = ObjectProperty()
    height_unit = ObjectProperty()
  
    #values from the weight textbox and spinner
    user_weight = ObjectProperty()
    weight_unit = ObjectProperty()
  
    #value from the age textbox
    user_age = ObjectProperty()
  
    #value from the sex spinner
    user_sex = ObjectProperty()
	
    def collect_input( self ):
        '''Method to collect & organize the user entered data'''
        #height collection and storage
        data[ self.height_unit.text ] = Decimal( self.user_height.text )

        #weight collection and storage
        data[ self.weight_unit.text ] = Decimal( self.user_weight.text )

        #sex collection and storage
        data['age'] = int( self.user_age.text )

        #age collection and storage
        data['sex'] = self.user_sex.text.lower()

    def calculations( self ):
        '''Method to compute all necessary information and convert'''
        if data['kg']: #convert to pounds
            data['lbs'] = kg_to_lbs( data['kg'] )
        elif not data['kg']: #convert to kilograms
            data['kg'] = lbs_to_kg( data['lbs'] )

        if data['cm']: #convert to inches
            data['in'] = cm_to_inch( data['cm'] )
        elif not data['cm']: #convert to centimetres
            data['cm'] = inch_to_cm( data['in'] )

        data['bmi'] = body_mass_index( data['kg'], data['cm'] )
        data['ibw_lbs'], data['ibw_kg']= ideal_body_weight( data['lbs'], data['in'], data['sex'] )
	data['%ibw'] = percent_ideal_body_weight(data['kg'], data['ibw_kg'])
        if data['%ibw'] >= 125.0:
            data['abw'] = adjust_body_weight( data['ibw_kg'], data['kg'] )

        data['calories'] = mifflin(data['kg'], data['cm'], data['sex'], data['age'])


    def reset_fields( self ):
        '''Method attached to the reset button to re-initialize all fields'''   
        self.user_height.text = ''
        self.user_weight.text = ''
        self.user_age.text = ''
        self.height_unit.text = 'cm'
        self.weight_unit.text = 'kg'
        self.user_sex.text = 'Male'
    
    def output_popup( self ):
        '''Method to build a pop up for displaying output'''
        try:
            self.clear_data()
            self.collect_input()
            self.calculations()
    
        except:
            print "Error, something not filled out proper"
            return None

        #button to close popup
        confirm_button = Button( text = 'Close', size_hint = ( 1, 0.25 ) )
        
        #making the content based on input/output
        data_layout = self.make_content()

        #Add popup content and open it
        popup_content = BoxLayout( orientation = 'vertical' )
        popup_content.add_widget( data_layout )
        popup_content.add_widget( confirm_button )

        pop_window = Popup( title = 'Results', size_hint = ( 0.95, 0.65 ), 
                            content = popup_content )

        confirm_button.bind( on_release = pop_window.dismiss )   
        pop_window.open()

    def clear_data(self):
        '''Method to (re)initialize the data dic'''
        global data
        data = {'kg': None, 'lbs': None, 'cm': None, 'in': None, 'bmi': None, 
        'ibw': None, 'abw': None, 'sex': None, 'calories': None } 
 
    def make_content(self):
        '''Method to generate the content show in the popup window'''
        
        #display user input as metric units
        input_data = Label( 
        text = '   Metric:\n\nHeight: {0:.2f}cm\nWeight: {1:.2f}kg'.format( 
        data['cm'], data['kg'] ))

        #display user input as imperial units
        input_data_converted = Label(
        text = '  Imperial:\n\nHeight: {0:.2f}in\nWeight: {1:.2f}lbs'.format( 
        data['in'], data['lbs'] ) )

        #store the user input data labels in a box layout
        inputbox = BoxLayout(orientation = 'horizontal')
        inputbox.add_widget(input_data)
        inputbox.add_widget(input_data_converted)

        #the output calculations
        output_base_data = Label(text= '''Calories: {4:.1f} ({5:.0f}kcal/kg)
BMI: {0:.2f} - {1}\nIBW: {2:.2f}kg ({3:.2f}%)'''.format( data['bmi'][0],
        data['bmi'][1], data['ibw_kg'], data['%ibw'], data['calories'], 
        (data['calories']/data['kg'])
        ))
        #if adjusted body weight applicable (>= 125% IBW ) add it in to the output
        if data['abw']:
            output_base_data.text = '''Calories: {4:.1f} ({5:.0f}kcal/kg)
BMI: {0:.2f} - {1}\nIBW: {2:.2f}kg ({3:.2f}%)
ABW: {6:.2f}kg'''.format( data['bmi'][0],
            data['bmi'][1], data['ibw_kg'], data['%ibw'], data['calories'], 
            (data['calories']/data['kg']), data['abw']
            )
    
        #Box layout to organize all input and output data
        data_layout = BoxLayout( orientation = 'vertical' )
        data_layout.add_widget(inputbox)
        data_layout.add_widget(output_base_data)

        return data_layout
        
class NutritionApp( App ):
  def build( self ):
    return Widgets()
		
buddy = NutritionApp()
NutritionApp().run()

	
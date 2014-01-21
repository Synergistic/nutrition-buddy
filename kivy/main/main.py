from kivy.app import App
from nutcalc import *
from decimal import Decimal

from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

data = {'kg': None, 'lbs': None, 'cm': None, 'in': None,
		'bmi': None, 'ibw': None, 'abw': None, 'sex': None, 
		'calories': None } 


Config.set( 'graphics', 'width', '360' )
Config.set( 'graphics', 'height', '640' )

class Widgets( BoxLayout ):
  
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
	try:
		#height collection and storage
		data[ self.height_unit.text ] = Decimal( self.user_height.text )

		#weight collection and storage
		data[ self.weight_unit.text ] = Decimal( self.user_weight.text )

		#sex collection and storage
		data['age'] = int( self.user_age.text )
		
		#age collection and storage
		data['sex'] = self.user_sex.text.lower()
	except ValueError:
		print 'Something wasn\'t filled out with a proper number'
	self.calculations()
	
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
	data['ibw_lbs'], data['ibw_kg'], data['%ibw'] = ideal_body_weight( data['lbs'], data['in'], data['sex'] )
	
	if data['%ibw'] >= 125.0:
		data['abw'] = adjust_body_weight( data['ibw_kg'], data['kg'] )
	
	
	
	
  def reset_data( self ):
    '''Method attached to the reset button to re-initialize all fields'''   
    self.user_height.text = ''
    self.user_weight.text = ''
    self.user_age.text = ''
    self.height_unit.text = 'cm'
    self.weight_unit.text = 'kg'
    self.user_sex.text = 'Male'
 
  def output_popup( self ):
	'''Method to build a pop up for displaying output'''
	self.collect_input()
	
	confirm_button = Button( text = 'Okay', size_hint = ( 1, 0.5 ) )
	
	input_data = Label( text = 'Height: {0}{1}\nWeight: {2}{3}'.format( 
	data[self.height_unit.text], self.height_unit.text, data[self.weight_unit.text], self.weight_unit.text ) )
	
	output_data = Label( text = 
	'BMI: {0:.2f} - {1}\nIBW: {2:.2f}({3:.2f})'.format(
	data['bmi'][0], data['bmi'][1], data['ibw_kg'], data['%ibw']
	))
	

	output_layout = BoxLayout( orientation = 'horizontal' )
	output_layout.add_widget(input_data)
	output_layout.add_widget(output_data)
	
	popup_content = BoxLayout( orientation = 'vertical' )
	popup_content.add_widget( output_layout )
	popup_content.add_widget( confirm_button )

	pop_window = Popup( title = 'Results', size_hint = ( 0.85, 0.5 ), 
			content = popup_content )
			
	confirm_button.bind( on_release = pop_window.dismiss )   
	pop_window.open()
	
 

class NutritionApp( App ):
  def build( self ):
    return Widgets()
		
buddy = NutritionApp()
NutritionApp().run()

	
from kivy.app import App
from nutcalc import *
from decimal import Decimal

from kivy.config import Config
from kivy.properties import ObjectProperty, StringProperty

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

data = {} #This is where we'll store all our user entry data
#change this to a list of global variables vs. catch key error from dictionary


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
  
  def output_data( self ):
    '''Method to output all user entered data to the console'''
    self.build_popup()
    print 'Height: {0}{1}\nWeight: {2}{3}\nAge: {4}yrs\nSex: {5}'.format( 
    self.user_height.text, self.height_unit.text, 
    self.user_weight.text, self.weight_unit.text,
    self.user_age.text, self.user_sex.text
    )

  def reset_data( self ):
    '''Method attached to the reset button to re-initialize all fields'''
    
    self.user_height.text = ''
    self.user_weight.text = ''
    self.user_age.text = ''
    self.height_unit.text = 'unit'
    self.weight_unit.text = 'unit'
    self.user_sex.text = 'Select sex'
 
  def build_popup( self ):
    confirm_button = Button( text = 'Okay' )
    output_data = Label( text = 'Your BMI, etc. Here' )
 
    popup_content = BoxLayout( orientation = 'vertical' )
    
    popup_content.add_widget( output_data )
    popup_content.add_widget( confirm_button )
    
    pop_window = Popup( title = 'Output!', size_hint = ( 0.85, 0.5 ), 
			content = popup_content )
    confirm_button.bind( on_release = pop_window.dismiss() )
    
    pop_window.open()
    
class NutritionApp( App ):
  def build( self ):
    return Widgets()
		
buddy = NutritionApp()
NutritionApp().run()

	
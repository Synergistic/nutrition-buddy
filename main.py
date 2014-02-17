
from kivy.app import App

import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc
import calculations as calc


from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class NutritionCalc(BoxLayout):
    '''Parent widget that holds all labels, text inputs, buttons, etc.'''
    
    title_text = "Nutrition Calculator"
    #values from the height, weight, age text inputs
    height_value   = ObjectProperty('')
    weight_value   = ObjectProperty('')
    age      = ObjectProperty('')
  
    #value from the height, weight, sex spinners
    height_unit = ObjectProperty('cm')
    weight_unit = ObjectProperty('kg')
    sex    = ObjectProperty('Male')

    
    def run_calculator(self):
        '''Run the calculator by initializing the data dic, gathering
        input from appropriate fields, computing necessary values, and
		finally building the pop up to display output'''

	d = calc.calculations(self.height_value, self.height_unit, 
		   self.weight_value, self.weight_unit, 
		   self.age, self.sex, self.title_text)
	self.wrap(d)
	
		
    def output_popup(self, d):
        '''Method to build a pop up for displaying output'''

        #button to close popup
        confirm_button = Button(text = 'Close', size_hint = (1, 0.25))
        
        #making the content based on input/output
        d_layout = self.make_content(d)

        #Add popup content and open it
        popup_content = BoxLayout( orientation = 'vertical' )
        popup_content.add_widget( d_layout )
        popup_content.add_widget( confirm_button )

        pop_window = Popup(title = self.title_text, size_hint = (0.95, 0.65), 
                            content = popup_content)

        confirm_button.bind(on_release = pop_window.dismiss)   
        pop_window.open()

    def make_content(self, d):
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
        self.height_value  = ''
        self.weight_value  = ''
        self.age           = ''
        self.height_unit   = 'cm'
        self.weight_unit   = 'kg'
        self.sex           = 'Male'
        self.stress_factor = '1.0'
        self.max_temp      = ''
        self.ventilation   = ''

class MifflinCalc(NutritionCalc):
    stress_factor = ObjectProperty('1.0')
    title_text = 'Mifflin St. Jeor Equation'
    def wrap(self,d):
	d['calories'] = calc.energy_needs(d, self.title_text)
	self.output_popup(d)
	print "I only print when doing Mifflin!"
	
	
class PennCalc(NutritionCalc):
    title_text = 'Penn State Equation'
    max_temp = ObjectProperty('')
    ventilation = ObjectProperty('')
    temp_unit = ObjectProperty('C')

    def wrap(self, d):
	d['temp_unit'] = self.temp_unit
	d['tmax'] = self.max_temp
	d['ventilation'] = self.ventilation
	d['calories'] = calc.energy_needs(d, self.title_text)
	self.output_popup(d)
	
    
	
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

	

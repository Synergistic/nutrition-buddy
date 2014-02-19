import calc.convert as convert
import calc.anthropometrics as anthro
import calc.nutrientneeds as nutcalc
import calculations as calc

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup

class NutritionCalc(BoxLayout):
    #values from the height, weight, age text inputs
    height_value, weight_value = ObjectProperty(''), ObjectProperty('')
    height_unit, weight_unit = ObjectProperty('cm'), ObjectProperty('kg')
    age, sex = ObjectProperty(''), ObjectProperty('Male')

    def run_calculator(self):
	d = calc.calculations(self.height_value, self.height_unit, 
			      self.weight_value, self.weight_unit, 
			      self.age, self.sex)
	self.add_uniques()
	d['calories'] = calc.energy_needs(d, self.unique_values)
	self.output_popup(d)	
		
    def output_popup(self, d):
        '''Method to build a pop up for displaying output'''
        d_layout = self.make_content(d)

        #Add popup content and open it
        confirm_button = Button(text = 'Close', size_hint = (1, 0.25))
        popup_content = BoxLayout(orientation = 'vertical')
        popup_content.add_widget(d_layout)
        popup_content.add_widget(confirm_button)

        pop_window = Popup(title = self.title_text, 
			   size_hint = (0.95, 0.65), content = popup_content)
	confirm_button.bind(on_release = pop_window.dismiss)   
        pop_window.open()

    def make_content(self, d):
	#
	#Make a function out of these that takes a list of strings
	#
        #display user input as metric units
        metric_out = ['Metric:', 
		      'Height: {height:.2f}cm', 
		      'Weight: {weight:.2f}kg']        
        anthro_l = Label(text = "\n".join(metric_out).format(
			  height = d['cm'], weight = d['kg']))
	
	#display user input as imperial units
        imperial_out = ['Imperial:', 
			'Height: {height:.2f}in', 
			'Weight: {weight:.2f}lbs']
        anthro_r = Label(text = "\n".join(imperial_out).format(
			  height = d['in'], weight = d['lbs']))
	
	#Make a boxlayout to hold anthros at the top
        inputbox = BoxLayout(orientation = 'horizontal')
        inputbox.add_widget(anthro_l)
        inputbox.add_widget(anthro_r)

        output_text = ['Calories: {cal:.1f} ({cal_kg:.0f}kcal/kg)', 
		       'BMI: {bmi:.2f} - {bmi_category}', 
		       'IBW: {ibw:.2f}kg ({percent_ibw:.2f}%)']
	
        output_base_d = Label(text= "\n".join(output_text).format( 
	  cal = d['calories'], cal_kg = d['calories']/d['kg'],
	  bmi = d['bmi'][0], bmi_category = d['bmi'][1], 
	  ibw = d['ibw_kg'], percent_ibw = d['%ibw']))
	
        #if adjusted body weight applicable (>= 125% IBW ) add it in to the output
        if d['abw']:
	    output_text.append('ABW: {abw:.2f}kg')
            output_base_d.text = "\n".join(output_text).format( 
	      cal = d['calories'], cal_kg = d['calories']/d['kg'],
	      bmi = d['bmi'][0], bmi_category = d['bmi'][1], 
	      ibw = d['ibw_kg'], percent_ibw = d['%ibw'], abw = d['abw'])
	    
        #Box layout to organize all input and output d
        d_layout = BoxLayout(orientation = 'vertical')
        d_layout.add_widget(inputbox)
        d_layout.add_widget(output_base_d)

        return d_layout
		
    def reset_fields(self):
        '''Method attached to the reset button to re-initialize all fields'''
        self.height_value  = self.weight_value = self.age = ''
        self.height_unit   = 'cm'
        self.weight_unit   = 'kg'
        self.sex           = 'Male'
        self.stress_factor = '1.0'
        self.max_temp      = self.ventilation  = ''


class MifflinCalc(NutritionCalc):
    stress_factor = ObjectProperty('1.0')
    title_text = 'Mifflin St. Jeor Equation'
    def add_uniques(self):
	self.unique_values = [self.stress_factor]
	
	
class PennCalc(NutritionCalc):
    max_temp, ventilation = ObjectProperty(''), ObjectProperty('')
    temp_unit = ObjectProperty('C')
    title_text = 'Penn State Equation'
    
    def add_uniques(self):
	 self.unique_values = [self.title_text, self.max_temp,
			      self.temp_unit, self.ventilation]
	 
	 
class Widgets(TabbedPanel):
    '''Base tabbed panels for holding each calculator. Contains the welcome page as well.'''
    welcome_text = "\n".join(['Welcome to Nutrition Buddy',
			      'I calculate things!', 
			      'Select a calculator below to get started.'])
    
    
class NutritionApp(App):
    title = "Nutrition Buddy"
	
    def build(self):
        return Widgets()
		
    def on_pause(self):
        return True
		
if __name__ in ('__main__', '__android__'):
    NutritionApp().run()

	

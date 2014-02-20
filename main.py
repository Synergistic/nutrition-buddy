from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
import calculations as calc
import output

class NutritionCalc(BoxLayout):
    #values from the height, weight, age text inputs
    height_value, weight_value = ObjectProperty(''), ObjectProperty('')
    height_unit, weight_unit = ObjectProperty('cm'), ObjectProperty('kg')
    age, sex = ObjectProperty(''), ObjectProperty('Male')

    def run_calculator(self):
	d = calc.initial_data(
	  ht_value = self.height_value, ht_unit = self.height_unit, 
	  wt_value = self.weight_value, wt_unit = self.weight_unit, 
	  age = int(self.age), sex = self.sex.lower())
	d['calories'] = calc.energy_needs(d, self.add_uniques())
	output.make_popup(d, self.add_uniques())	
			
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
	return [self.title_text, self.stress_factor]
	
	
class PennCalc(NutritionCalc):
    max_temp, ventilation = ObjectProperty(''), ObjectProperty('')
    temp_unit = ObjectProperty('C')
    title_text = 'Penn State Equation'
    
    def add_uniques(self):
	return [self.title_text, self.max_temp, 
		self.temp_unit, self.ventilation]
	 
	 
class Pages(TabbedPanel):
    '''Base tabbed panels for holding each calculator. 
    Also holds the welcome page'''
    welcome_text = "\n".join(['Welcome to Nutrition Buddy',
			      'I calculate things!', 
			      'Select a calculator below to get started.'])
    
    
class NutritionApp(App):
    title = "Nutrition Buddy"
	
    def build(self):
        return Pages()
		
    def on_pause(self):
        return True
		
if __name__ in ('__main__', '__android__'):
    NutritionApp().run()

	

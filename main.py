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
	d = calc.initial_data(self.height_value, self.height_unit, 
                        self.weight_value, self.weight_unit, 
                        self.equation_specific(),
                        age = int(self.age), sex = self.sex.lower())
	output.make_popup(d, self.equation_specific())	
			
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
    
    def equation_specific(self):
        return [self.title_text, self.stress_factor]
	
	
class PennCalc(NutritionCalc):
    max_temp, ventilation = ObjectProperty(''), ObjectProperty('')
    temp_unit = ObjectProperty('C')
    title_text = 'Penn State Equation'
    
    def equation_specific(self):
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

	

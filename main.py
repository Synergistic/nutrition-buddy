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
	d = calc.initial_data(self.height_value, self.height_unit, 
			      self.weight_value, self.weight_unit, 
			      self.age, self.sex)
	
	d['calories'] = calc.energy_needs(d, self.add_uniques())
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

    def make_output_strings(self, d, strings, title=''):
	full_output = [title]
	for i in xrange(len(strings)):
	    if i % 2 == 0:
		out = [strings[i].capitalize(), ': {value:.2f}', strings[i+1]]
		outtie = ''.join(out).format(value=d[strings[i+1]])
		full_output.append(outtie)
        return '\n'.join(full_output)
      
    def make_content(self, d):
      
        anthro_left = Label(text = self.make_output_strings(
	  d, ['height', 'cm', 'weight', 'kg'], 'Metric'))
        anthro_right = Label(text = self.make_output_strings(
	  d, ['height', 'in', 'weight', 'lbs'], 'Imperial'))
	
	#Make a boxlayout to hold anthros at the top
        inputbox = BoxLayout(orientation = 'horizontal')
        inputbox.add_widget(anthro_left)
        inputbox.add_widget(anthro_right)

        output_text = ['Calories: {cal:.1f} ({cal_kg:.0f}kcal/kg)', 
		       'BMI: {bmi:.2f} - {bmi_category}', 
		       'IBW: {ibw:.2f}kg ({percent_ibw:.2f}%)']
	if d['abw'] == 'N/A':
	    output_text.append('ABW: {abw}')
	else:
	    output_text.append('ABW: {abw:.2f}kg')
	    
        output_base_d = Label(text= "\n".join(output_text).format( 
	  cal = d['calories'], cal_kg = d['calories']/d['kg'],
	  bmi = d['bmi'][0], bmi_category = d['bmi'][1], 
	  ibw = d['ibw_kg'], percent_ibw = d['%ibw'], 
	  abw = d['abw']))

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

	

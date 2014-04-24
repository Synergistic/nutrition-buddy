from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.accordion import Accordion
import calculations as calc
import output


class NutritionCalc(BoxLayout):
    '''Base calculator which other calculators will be based on'''

    #Initialize all kivy property values that will be shown on the GUI
    height_value, weight_value = ObjectProperty(''), ObjectProperty('')
    height_unit, weight_unit = ObjectProperty('cm'), ObjectProperty('kg')
    age, sex = ObjectProperty(''), ObjectProperty('Male')

    def run_calculator(self):
        #run calculations and display output when Calculate button is pressed
        d = calc.initial_data(self.height_value, self.height_unit,
                           self.weight_value, self.weight_unit,
                           self.equation_specific_values(),
                           age=self.age, sex=self.sex.lower())
        if d:
            output.make_popup(d, self.equation_specific_values())

    def reset_fields(self):
        #Method attached to the reset button to re-initialize all fields
        self.height_value = self.weight_value = self.age = ''
        self.max_temp = self.ventilation = ''
        self.stress_factor = '1.0 - No stress factor'
        self.activity_factor = '1.0 - No activity factor'
        self.height_unit = 'cm'
        self.weight_unit = 'kg'
        self.sex = 'Male'


class MifflinCalc(NutritionCalc):
    '''Calculator that utilizes Mifflin St Jeor Equation. This equation
    takes into account stress/activity through the use of a "factor"'''
    stress_factor = ObjectProperty('1.0 - No Stress')
    activity_factor = ObjectProperty('1.0 - No Activity')
    title_text = 'Mifflin St. Jeor Equation'
    activity_factors = ['1.0 - Activity',
              '1.20 - Bed Rest',
              '1.30 - Ambulatory']
    stress_factors = ['0.70 - Starvation',
              '1.00 - Stress',
              '1.13 - 1C Fever',
              '1.20 - Surgery',
              '1.20 - Bed Rest',
              '1.35 - Trauma',
              '1.50 - Burn < 40% TBSA',
              '1.60 - Head Injury/Sepsis',
              '2.10 - Burn > 40% TBSA']
              
    def equation_specific_values(self):
        return [self.title_text, self.stress_factor[:3], self.activity_factor[:3]]


class PennCalc(NutritionCalc):
    '''Calculator that uses PennState Equation for intubated patients.
    It takes into account their max temperature in 24 hours and their
    ventilation rate'''
    max_temp, ventilation = ObjectProperty(''), ObjectProperty('')
    temp_unit = ObjectProperty('C')
    title_text = 'Penn State Equation'
    
    def equation_specific_values(self):
        return [self.title_text, self.max_temp,
                self.temp_unit, self.ventilation]


class Pages(Accordion):
    '''Base accordion object for holding each calculator.
    Also holds the welcome page'''
    welcome_text = "\n".join(['Welcome to Nutrition Buddy',
                              'I calculate things!',
                              'Select a calculator above to get started.'])


class CalcButtons(BoxLayout):
    pass
  
  
class NutritionApp(App):
    title = "Nutrition Buddy"

    def build(self):
        return Pages()

    def on_pause(self):
        return True

if __name__ in ('__main__', '__android__'):
    NutritionApp().run()

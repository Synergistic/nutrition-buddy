from kivy.app import App
from nutcalc import *
from decimal import Decimal

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

data = {} #This is where we'll store all our user entry data
#change this to a list of global variables vs. catch key error from dictionary
class LabelsAndText(GridLayout):

	def test(self):
		print "This is a test"
		
class NutritionApp(App):

	
	def build(self):
	

			
		g = GridLayout(cols = 3, rows = 5,
					   row_default_height = 30,
					   row_force_default = True)
		#row 1
		height_area = BoxLayout(orientation = 'horizontal')
		middle_col = BoxLayout()
		weight_area = BoxLayout(orientation = 'horizontal')
		
		#row 2
		age_area = BoxLayout(orientation = 'horizontal')
		middle_coltwo = BoxLayout()
		gender_area = BoxLayout(orientation = 'horizontal')
		
		#row 3
		calc_area = BoxLayout(orientation = 'horizontal')
		middle_colthree = BoxLayout()
		reset_area = BoxLayout(orientation = 'horizontal')
		
		#row 4
		output_area1 = BoxLayout()
		output_area2 = BoxLayout()
		output_area3 = BoxLayout()
		
		
		g.add_widget(height_area)
		g.add_widget(middle_col)
		g.add_widget(weight_area)
		g.add_widget(age_area)
		g.add_widget(middle_coltwo)
		g.add_widget(gender_area)
		g.add_widget(calc_area)
		g.add_widget(middle_colthree)
		g.add_widget(reset_area)
		g.add_widget(output_area1)
		g.add_widget(output_area2)
		g.add_widget(output_area3)
		
		height_label = Label(text = 'Height', font_size = 16)
		self.height_input = TextInput()
		self.height_unitbox = Spinner(text = "unit",
							     values = ("cm", "in"))
								 
		height_area.add_widget(height_label)
		height_area.add_widget(self.height_input)
		height_area.add_widget(self.height_unitbox)
		
		
		weight_label = Label(text = "Weight", font_size = 16)
		self.weight_input = TextInput()
		self.weight_unitbox = Spinner(text = "unit",
							     values = ("kg", "lbs"))
								 
		weight_area.add_widget(weight_label)
		weight_area.add_widget(self.weight_input)
		weight_area.add_widget(self.weight_unitbox)		
		
		age_label = Label(text = "Age", font_size = 16)
		self.age_input = TextInput()
		age_unitlabel = Label(text = "years", font_size = 16)
								 
		age_area.add_widget(age_label)
		age_area.add_widget(self.age_input)
		age_area.add_widget(age_unitlabel)
		
		
		
		gender_label = Label(text = "Gender", font_size = 16)
		self.gender_box = Spinner(text = "select",
							     values = ("Male", "Female"))
								 
		gender_area.add_widget(gender_label)
		gender_area.add_widget(self.gender_box)
		
		calc_button = Button(text = "Calculate", font_size = 16)
		calc_area.add_widget(calc_button)
		
		reset_button = Button(text = "Reset", font_size = 16)
		reset_area.add_widget(reset_button)
		
		self.energy_output = Label(text = "", font_size = 16)
		middle_col.add_widget(self.energy_output)
		
		self.bmi_output = Label(text = "", font_size = 16)
		middle_coltwo.add_widget(self.bmi_output)
		
		self.ibw_output = Label(text = "", font_size = 16)
		middle_colthree.add_widget(self.ibw_output)
		
		self.height_output = Label(text = "", font_size = 16)
		output_area1.add_widget(self.height_output)
		
		self.abw_output = Label(text = "", font_size = 16)
		output_area2.add_widget(self.abw_output)
		
		self.weight_output = Label(text= "", font_size = 16)
		output_area3.add_widget(self.weight_output)
		
		#binds
		reset_button.bind(on_press = self.reset_all)
		calc_button.bind(on_press = self.store)

		
		return g
	
		
	def reset_all(self, instance):
	#method to null inputs/menus
		self.reset_input()
		self.reset_output()
		
	def reset_input(self):
		self.weight_input.text = ""
		self.height_input.text = ""
		self.gender_box.text = "select"
		self.weight_unitbox.text = "unit"
		self.height_unitbox.text = "unit"
		self.age_input.text = ""
	
	def reset_output(self):
		self.energy_output.text = ""
		self.bmi_output.text = ""
		self.ibw_output.text = ""
		self.abw_output.text = ""
		self.height_output.text = ""
		self.weight_output.text = ""
	

	def store(self, instance):

		#Store all inputbox and spinner data here for easy reference. 
		
		user_weight = str(self.weight_input.text)
		user_height = str(self.height_input.text)
		user_age = str(self.age_input.text)
		user_sex = str(self.gender_box.text)
		height_units = str(self.height_unitbox.text)
		weight_units = str(self.weight_unitbox.text)
		
		#Look at the units in the spinner and store the input fields
		#appropriately, also converting to the opposite unit.
		
		if weight_units == 'kg':
			data['kg'] = Decimal(user_weight)
			data['lbs'] = kg_to_lbs(data['kg'])		
		elif weight_units == 'lbs':
			data['lbs'] = Decimal(user_weight)
			data['kg'] = lbs_to_kg(data['lbs'])
		elif weight_units == 'unit':
			print "Please select a unit for weight"
			
		if height_units == 'cm':
			data['cm'] = Decimal(user_height)
			data['in'] = cm_to_inch(data['cm'])
		elif height_units == 'in':
			data['in'] = Decimal(user_height)
			data['cm'] = inch_to_cm(data['in'])
		elif height_units == 'unit':
			print "Please select a unit for height"
	
		if user_age.isdigit():
			data['age'] = Decimal(user_age)
			
		if user_sex != 'select':
			data['sex'] = user_sex.lower()
			
		print data
		self.calc()
		
	def calc(self):
		self.reset_output()
		abw = False
		energy = mifflin(data['kg'], data['cm'], data['sex'], data['age'])
		bmi = bodymassindex(data['kg'], data['cm'])
		ibw = idealbodyweight(data['lbs'], data['in'], data['sex'])
		if ibw[2] > Decimal('124.9'):
			abw = adjustbodyweight(ibw[1], data['kg'])
		calories_kg = calories_per_kg(data['kg'], energy)
		
		self.energy_output.text = "Energy Needs: {0:.1f} - {1:.0f}kcal/kg".format(energy, calories_kg)
		
		self.bmi_output.text = "BMI: {0:.2f} - {1}".format(bmi[0], bmi[1])
		
		self.ibw_output.text = "IBW: {0:.2f}kg ({1:.2f}%)".format(ibw[1], ibw[2])
		
		if abw:
			self.abw_output.text = "ABW: {0:.2f}kg".format(abw)
		
		
		self.height_output.text = "Height: {0:.2f}cm or {1:.2f}in".format(data['cm'], data['in'])
		self.weight_output.text = "Weight: {0:.2f}kg or {1:.2f}lbs".format(data['kg'], data['lbs'])
		
		

			

buddy = NutritionApp()
NutritionApp().run()

	
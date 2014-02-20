from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout

def make_popup(d, values):
    '''Method to build a pop up for displaying output'''

    confirm_button = Button(text = 'Close', size_hint = (1, 0.25))
    popup_content = BoxLayout(orientation = 'vertical')
    popup_content.add_widget(make_output(d))
    popup_content.add_widget(confirm_button)

    pop_window = Popup(title = values[0], size_hint = (0.95, 0.65), 
		       content = popup_content)
    confirm_button.bind(on_release = pop_window.dismiss)   
    pop_window.open()

def make_strings(d, strings, title=''):
    full_output = [title]
    for i in xrange(len(strings)):
	if i % 2 == 0:
	    out = [strings[i].capitalize(), ': {value:.2f}', strings[i+1]]
	    outtie = ''.join(out).format(value=d[strings[i+1]])
	    full_output.append(outtie)
    return '\n'.join(full_output)
  
def make_output(d):
  
    anthro_left = Label(text = make_strings(
      d, ['height', 'cm', 'weight', 'kg'], 'Metric'))
    anthro_right = Label(text = make_strings(
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

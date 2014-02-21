from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


def make_popup(d, values):
    '''Method to build a pop up for displaying output'''
    confirm_button = Button(text='Close', size_hint=(1, 0.25))
    popup_content = BoxLayout(orientation='vertical')
    popup_content.add_widget(make_output(d))
    popup_content.add_widget(confirm_button)

    pop_window = Popup(title=values[0], size_hint=(0.95, 0.65),
                       content=popup_content)
    confirm_button.bind(on_release=pop_window.dismiss)
    pop_window.open()


def make_strings(d, strings, title=''):
    '''Takes a list of strings and formats them for proper output display'''
    full_output_section = [title]
    for i in xrange(len(strings)):
        if i % 2 == 0:
            line_pts = [strings[i].capitalize(), ': {value:.2f}', strings[i+1]]
            complete_line = ''.join(line_pts).format(value=d[strings[i+1]])
            full_output_section.append(complete_line)
    return '\n'.join(full_output_section)


def make_output(d):
    '''Creates the widgets to display output data and assembles them into
    a single layout.'''
    anthro_left = Label(text=make_strings(
        d, ['height', 'cm', 'weight', 'kg'], 'Metric'))
    anthro_right = Label(text=make_strings(
        d, ['height', 'in', 'weight', 'lbs'], 'Imperial'))

    inputbox = BoxLayout(orientation='horizontal')
    inputbox.add_widget(anthro_left)
    inputbox.add_widget(anthro_right)

    output_text = ['Calories: {cal:.1f} ({cal_kg:.0f}kcal/kg)',
                   'BMI: {bmi:.2f} - {bmi_category}',
                   'IBW: {ibw:.2f}kg ({percent_ibw:.2f}%)']
    if d['abw'] == 'N/A':
        output_text.append('ABW: {abw}')
    else:
        output_text.append('ABW: {abw:.2f}kg')

    output_data = Label(text="\n".join(output_text).format(
        cal=d['calories'], cal_kg=d['calories']/d['kg'],
        bmi=d['bmi'][0], bmi_category=d['bmi'][1],
        ibw=d['ibw_kg'], percent_ibw=d['%ibw'],
        abw=d['abw']))

    data_layout = BoxLayout(orientation='vertical')
    data_layout.add_widget(inputbox)
    data_layout.add_widget(output_data)
    return data_layout

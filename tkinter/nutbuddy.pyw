# -*- coding: cp1252 -*-

#================================================================================#
# Nutrition Buddy - A simple nutrition all-in-one calculator.                    #
#                                                                                #
#   Changelog:                                                                   #
#   v0.1a - First GUI version of Nutrition Buddy. Calculates energy needs based  #
#   on MifflinStJeor, BMI, IBW, %IBW, ABW (if applicable). Print out is always   #
#   in metrics but data can be entered in metric or imperial.                    #
#                                                                                #
#   v0.2a - Now does fluid needs taking into account age. Also determines        #
#   calores per kg. Added a clickable link for emailing myself for support. Now  #
#   catches errors in the entry fields.                                          #
#                                                                                #
#   v0.3a - Completely remade app from the ground up, partially to create more   #
#   organized code, partially because my work computer shit the bed and I lost   #
#   most of the original. Program now has a second list box that displays the    #
#   user entered information in both imperial and metric. Both listboxes now     #
#   are color-coded to easily distinguish between lines. Included some code in   #
#   this iteration to allow for future feature of alternate equation(s).         #
#                                                                                #
#   v0.31a - Fixes. Error catching reorganized to give more proper messages and  #
#   catch ALL possible errors(I think). User can now hit <Return> on any entry   #
#   box to run the calculations in place of clicking the button.                 #
#                                                                                #
#   v0.4a - Rewrote app using pieces from old version. Changed units to be       #
#   independently selected via an OptionMenu for height/weight and removed the   #
#   radio button. Switched to ttk styling of widgets for cleaner look. Removed   #
#   the second listbox and made one big one for all output. Added in Penn State  #
#   equation feature along with temp/Ve entries. Can select degree units. Check  #
#   box to switch between equations and disable appropriate entries. Put all     #
#   nutrition calculations into own separate .py module for program organization #
#                                                                                #
#                                                                                #
#                                                                                #
#   Planned: Fluids, Protein, Weight change Fresh icon                           #
#                                                                                #
#         By Dan Fernandez, DFernandez226@gmail.com                              #
#=================================================================================


from decimal import *
from Tkinter import *
from ttk import *
import nutcalc, tkMessageBox, webbrowser


class MyApp(Frame):
    def __init__(self, master):
        self.initialize(master)

    def initialize(self, master):
        #padding
        Label(text=" ").grid(row=0, column=0)
        Label(text=" ").grid(row=0, column=8)

        #Height label, entry box
        height_label = Label(master, text="Height").grid(column=1, row=1, sticky='e')
        self.height_entry = Entry(master, width=5)
        self.height_entry.grid(column=2, row=1, sticky='we')
        self.height_entry.bind("<Return>", self.calculate)

        #Height unit option menu
        self.ht_v = StringVar()
        self.height_units = OptionMenu(master, self.ht_v, 'unit', 'cm', 'in')
        self.height_units.grid(row=1, column=3, sticky='w')
        

        #Age label, entry box
        age_label = Label(master, text="Age").grid(column=1, row=2, sticky='e')
        self.age_entry = Entry(master, width=5)
        self.age_entry.grid(column=2, row=2, sticky='we')
        self.age_unit = Label(master, text="yrs").grid(column=3, row=2, sticky='w')
        self.age_entry.bind("<Return>", self.calculate)

        
        #Weight label, entry box, and unit label
        weight_label = Label(master, text="Weight").grid(column=4, row=1, sticky='e')
        self.weight_entry = Entry(master, width=5)
        self.weight_entry.grid(column=5, row=1, sticky='we', pady=4)
        self.weight_entry.bind("<Return>", self.calculate)
        
        #Weight unit option menu
        self.wt_v = StringVar()
        self.weight_units = OptionMenu(master, self.wt_v, 'unit', 'kg', 'lbs')
        self.weight_units.config(width=3)
        self.weight_units.grid(row=1, column=6, sticky='w')
        

        #Gender label, dropdown menu
        self.sex_v = StringVar()
        self.sex_menu = OptionMenu(master, self.sex_v, 'Gender', 'Male', 'Female')
        self.sex_menu.grid(column=4, row=2, sticky='we', columnspan=3)
        
        #Pennstate Checkbox
        self.penn_v = IntVar()
        self.pennBox = Checkbutton(master, text="PennSt",
                                   variable=self.penn_v,
                                   command=self.set_equation)
        self.pennBox.grid(row=4, column=3, sticky='e')


        #temp entry for PennSt
        self.tempLabel = Label(master, text="Tmax").grid(row=5, column=1, sticky=E)
        self.tempEntry = Entry(master, width=5, state=DISABLED)
        self.tempEntry.grid(row=5, column=2, sticky='we')

        #temp option menu for celcius/fahrenheit
        self.temp_var = StringVar()
        #Need to figure out degrees symbol
        self.tempUnit = OptionMenu(master, self.temp_var, 'C/F', 'C', 'F')
        self.tempUnit.config(state=DISABLED)
        self.tempUnit.grid(row=5, column=3, sticky='w')

        #ventilation/minute label & entry for PennSt
        self.ventLabel = Label(master, text="VE").grid(row=5, column=4, sticky=E)
        self.ventEntry = Entry(master, width=5, state=DISABLED)
        self.ventEntry.grid(row=5, column=5, sticky='w')
       
    

        #Button to run calculations
        self.calc_button = Button(master, text="Calculate", command=self.calculate)
        self.calc_button.grid(row=6, column=1, columnspan=3, sticky='we', pady=5)

        #Button to clear entries and reset selections
        self.reset_button = Button(master, text="Reset", command=self.reset)
        self.reset_button.grid(row=6, column=4, sticky='we', columnspan=3)

        #Listbox for all output
        self.outBox = Listbox(master)
        self.outBox.grid(row=7, column=1, sticky='news', columnspan=7)
        

        #email label for tech support
        self.email_label = Label(master, text="Click to email me with issues")
        self.email_label.grid(row=8, column=2, columnspan=4)
        self.email_label.bind("<Button-1>", self.email)


    def collect_sort(self):
        """
        Gathers the weight/height & converts it to opposite unit
        also gets age, gender and returns it all as a dictionary.
        Checks for errors in field entries, no unit selected
        """
        
        data = {}
        #Check the height units/entry and assign to correct variable, then convert.
        try:
            
            if str(self.ht_v.get()) == 'cm':
                data['ht_cm'] = Decimal(str(self.height_entry.get()))
                data['ht_in'] = data['ht_cm'] / Decimal('2.54')
                
            elif str(self.ht_v.get()) == 'in':
                data['ht_in'] = Decimal(str(self.height_entry.get()))
                data['ht_cm'] = data['ht_in'] * Decimal('2.54')
                
            else:
                tkMessageBox.showerror("Height Unit Error",
                                       "Did you select a unit for height?")

        except InvalidOperation:
            tkMessageBox.showerror("Height Error",
                                   "Your height doesn't appear to be valid.")


        #Check the weight units/entry and assign to correct variable, then convert.
        try:
            if str(self.wt_v.get()) == 'kg':
                data['wt_kg'] = Decimal(str(self.weight_entry.get()))
                data['wt_lbs'] = data['wt_kg'] * Decimal('2.2')
                
            elif str(self.wt_v.get()) == 'lbs':
                data['wt_lbs'] = Decimal(str(self.weight_entry.get()))
                data['wt_kg'] = data['wt_lbs'] / Decimal('2.2')
                
            else:
                tkMessageBox.showerror("Weight Unit Error",
                                       "Did you select a unit for weight?")
                
        except InvalidOperation:
            tkMessageBox.showerror("Weight Error",
                                   "Your weight doesn't appear to be valid.")


        #Get age from the entry field, if it can't be made into a decimal, raise an error
        try:
            data['age'] = Decimal(str(self.age_entry.get()))
        except InvalidOperation:
            tkMessageBox.showerror("Age Error",
                                   "Your age doesn't appear to be valid.")


        #Get gender from the option menu and store it
        if str(self.sex_v.get()).lower() == 'gender':
            tkMessageBox.showerror("Gender Error",
                                   "Did you select a gender from the dropdown?")
        else:
            data['gender'] = self.sex_v.get().lower()


        #Gather vent rate (VE) and temp (Tmax) from their fields if penn state is selected.
        if self.penn_v.get():

            try:
                temp = Decimal(str(self.tempEntry.get()))
            except InvalidOperation:
                tkMessageBox.showerror("Temperature Error",
                                       "Your temperature doesn't appear to be valid.")

            try:
                data['vent'] = Decimal(str(self.ventEntry.get()))
            except InvalidOperation:
                tkMessageBox.showerror("Ventilation Error",
                                       "Your VE doesn't appear to be valid.")
            

            if self.temp_var.get() == 'C':
                data['temp_c'] = temp
            elif self.temp_var.get() == 'F':
                data['temp_c'] = nutcalc.fahren_to_c(temp)
            else:
                tkMessageBox.showerror("Temperature Unit Error",
                                       "Check your temperature units.")
                
        
        #return it all as a dictionary
        return data



    def calculate(self):
        """
        Calls function to collect data from fields and sorts it into a
        dictionary. Then calculates bmi, ibw, abw, calories per kg, and
        energy needs using the appropriate equation. Finally calls out
        format function to store all items as strings in a new list for output
        """
        try:
            #call function to gather all data from fields
            data = self.collect_sort()

            #call body mass index function and store number and category
            data['bmi'] = nutcalc.bodymassindex(data['wt_kg'], data['ht_cm'])
                

            #call ideal body weight function. Store the ibw(lbs), ibw(kg), %ibw.
                
            data['ibw'], data['ibw_kg'], data['%_ibw'] = nutcalc.idealbodyweight(
                data['wt_lbs'],
                data['ht_in'],
                data['gender'])
            
            #If they are >=125% of ideal body weight, we need an Adjusted Body Weight
            if data['%_ibw'] > Decimal('124.9'):
                data['abw'] = nutcalc.adjustbodyweight(data['ibw_kg'], data['wt_kg'])

            #if penn state check box is selected, use PennSt. equation for energy needs
            if self.penn_v.get():
                data['penn'] = nutcalc.pennstate(
                    data['wt_kg'],
                    data['ht_cm'],
                    data['gender'],
                    data['age'],
                    data['temp_c'],
                    data['vent'])
                
                data['cal_per_kg'] = nutcalc.calories_per_kg(
                    data['wt_kg'],
                    data['penn'][0])
                
            #if penn state check box is NOT selected, use Mifflin for energy needs
            elif not self.penn_v.get():
                data['mifflin'] = nutcalc.mifflin(
                    data['wt_kg'],
                    data['ht_cm'],
                    data['gender'],
                    data['age'])
                
                data['cal_per_kg'] = nutcalc.calories_per_kg(
                    data['wt_kg'],
                    data['mifflin'])
                
            #create a new list by calling the formatting function to give to listbox output
            output = self.format_output(data)

            #output the new data to the listbox via output function
            self.outputInfo(output)
        except KeyError:
            pass


    def format_output(self, data):
        """
        Creates a list of strings for easy output to the listbox.
        Takes the info from a data list that is passed to it
        """
        output_list = []
        
        #Add the height in cm/in
        output_list.append(
            "Height: {0:.2f}cm or {1:.2f}in".format(
                data['ht_cm'],
                data['ht_in']))

        #Add the weight in kg/lbs
        output_list.append(
            "Weight: {0:.2f}kg or {1:.2f}lbs".format(
                data['wt_kg'],
                data['wt_lbs']))

        output_list.append("")

        #Add the BMI and category
        output_list.append(
            "BMI: {0:.2f} - {1}".format(
                data['bmi'][0],
                data['bmi'][1]))

        #Add the IBW in kg/lbs and (%ibw)
        output_list.append(
            "IBW: {0:.2f}kg or {1:.2f}lbs ({2:.2f}%)".format(
                data['ibw_kg'],
                data['ibw'],
                data['%_ibw']))

        #if abw was determined, add it to the list to output
        if 'abw' in data:
            output_list.append(
                "ABW: {0:.2f}kg or {1:.2f}lbs".format(
                data['abw'],
                data['abw'] * Decimal('2.2')))

        output_list.append("")
        
        #if mifflin was used, append to the list
        if 'mifflin' in data:
            output_list.append("Estimated Needs - Based on Mifflin")
            output_list.append("Calories: {0:.2f} ({1:.0f}cal/kg)".format(
                data['mifflin'],
                data['cal_per_kg']))

        #if pennst was used, append to the list            
        elif 'penn' in data:
            output_list.append("Estimated Needs - Based on {0}".format(data['penn'][1]))         
            output_list.append("Calories: {0:.2f} ({1:.0f}cal/kg)".format(
                data['penn'][0],
                data['cal_per_kg']))

        return output_list


    def outputInfo(self, data):
        """
        Displays all data in the listbox. Colors it based on how many
        items are present in the list
        """
        
        self.outBox.delete(0, END)
        for x in range(len(data)):
            self.outBox.insert(END, str(data[x]))
            if x < 2:
                self.outBox.itemconfig(x, fg='white', bg='blue')
                
            if len(data) == 9: #aka includes Adjusted Body Weight
                if x > 2 and x < 6:
                    self.outBox.itemconfig(x, fg='white', bg='darkgreen')
                if x > 6:
                    self.outBox.itemconfig(x, fg='white', bg='brown')
                    
            elif len(data) == 8: #Does NOT include Adjusted Body Weight
                if x > 2 and x < 5:
                    self.outBox.itemconfig(x, fg='white', bg='darkgreen')
                if x > 5:
                    self.outBox.itemconfig(x, fg='white', bg='brown')


    def set_equation(self):
        """
        Enable/Disable the Temp and Ventillation areas
        depending on the pennst check box.
        """
        
        if self.penn_v.get():
            self.ventEntry.config(state=NORMAL)
            self.tempEntry.config(state=NORMAL)
            self.tempUnit.config(state=NORMAL)
        elif not self.penn_v.get():
            self.ventEntry.config(state=DISABLED)
            self.tempEntry.config(state=DISABLED)
            self.tempUnit.config(state=DISABLED)


    def reset(self):
        """
        Function to clear the output listbox, the entry fields
        and reset all dropdowns to their initial state.
        """
        self.outBox.delete(0,END)
        self.height_entry.delete(0,END)
        self.weight_entry.delete(0,END)
        self.tempEntry.delete(0,END)
        self.ventEntry.delete(0,END)
        self.age_entry.delete(0,END)
        self.penn_v.set(0)
        self.set_equation()
        self.ht_v.set('unit')
        self.wt_v.set('unit')
        self.sex_v.set('Gender')
        self.temp_var.set('C/F')
    
    def email(self, click):
        #Opens a new email addressed to me for support.
        webbrowser.open('mailto:dfernandez226@gmail.com?subject=Nutrition Buddy Support')


def callback():
    if tkMessageBox.askokcancel("Quit", "Really quit?"):
        root.destroy()

root = Tk()
nutBuddyMiff = MyApp(root)
root.title("Nutrition Buddy v0.4a")
root.protocol("WM_DELETE_WINDOW", callback)
root.mainloop()

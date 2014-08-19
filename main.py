from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.properties import StringProperty

from Measures import Height, Weight, Age, Gender
from Calculator import NutritionCalculator
import re

class FactorPopup(Popup):
    mifflinValue = StringProperty('')
    updatedMifflin = StringProperty('')
    activityValues = ['1.0 - No Activity',
                      '1.20 - Bed Rest',
                      '1.30 - Ambulatory']
    stressValues = ['0.70 - Starvation',
                    '1.00 - No Stress',
                    '1.13 - 1C Fever',
                    '1.20 - Surgery',
                    '1.20 - Bed Rest',
                    '1.35 - Trauma',
                    '1.50 - Burn < 40% TBSA',
                    '1.60 - Head Injury/Sepsis',
                    '2.10 - Burn > 40% TBSA']    
    def __init__(self, mifflinValue):
        super(FactorPopup, self).__init__()
        self.mifflinValue = mifflinValue
        self.updatedMifflin = self.mifflinValue

    def updateFactors(self, activityFactor, stressFactor):
        tempMifflin = NutritionCalculator().MifflinFactor(self.mifflinValue, activityFactor)
        tempMifflin = NutritionCalculator().MifflinFactor(tempMifflin, stressFactor)
        return 'Needs + Factor(s): ' + str(tempMifflin)

class WelcomeScreen(Screen):
    pass

class ConversionScreen(Screen):

    weightIsMetric = False
    heightIsMetric = False

    def ConvertMeasure(self, typeOfMeasure, measureToConvert):
        decimalCheck = re.compile('\d+(\.\d+)?')
        if decimalCheck.match(measureToConvert) != None:

            if typeOfMeasure == 'weight':
                measure = Weight(measureToConvert, self.weightIsMetric)
                isMetric = self.weightIsMetric
            else:
                measure = Height(measureToConvert, self.heightIsMetric)
                isMetric = self.heightIsMetric

            if isMetric:
                return '{0:.2f}'.format(measure.ConvertToImperial())
            else:
                return '{0:.2f}'.format(measure.ConvertToMetric())
        return ''            

    def SetButtonText(self, buttonToChange):
        if buttonToChange.text[0] == 'k' or buttonToChange.text[0] == 'l':
            self.weightIsMetric = not self.weightIsMetric

            if self.weightIsMetric:
                buttonToChange.text = 'kg > lbs'
            else:
                buttonToChange.text = 'lbs > kg'

        if buttonToChange.text[0] == 'c' or buttonToChange.text[0] == 'i':
            self.heightIsMetric = not self.heightIsMetric

            if self.heightIsMetric:
                buttonToChange.text = 'cm > in'
            else:
                buttonToChange.text = 'in > cm'   


class MifflinStJeorScreen(Screen):

    def Calculations(self, measures):

        decimalCheck = re.compile('\d+(\.\d+)?')
        if decimalCheck.match(measures['wtValue']) == None or \
           decimalCheck.match(measures['htValue']) == None or \
           decimalCheck.match(measures['age']) == None:
            return "Unable to process, check entered values."

        if measures['wtUnit'] == 'kg':
            weight = Weight(measures['wtValue'], True)
        else:
            weight = Weight(measures['wtValue'], False)

        if measures['htUnit'] == 'cm':
            height = Height(measures['htValue'], True)
        else:
            height = Height(measures['htValue'], False)     

        if measures['gender'] == 'down':
            gender = Gender(True)
        else:
            gender = Gender(False)
        age = Age(measures['age'])

        return "\n".join([self.CalculateEnergyNeeds(weight.ConvertToMetric(), 
                                                    height.ConvertToMetric(), 
                                                    age.value, gender),
                          self.CalculateBMI(weight.ConvertToMetric(), 
                                            height.ConvertToMetric()),
                          self.CalculateIdealWeight(weight, 
                                                    height.ConvertToImperial(), 
                                                    gender)])

    def CalculateBMI(self, weight, height):
        bmi = NutritionCalculator().BodyMassIndex(weight, height)
        bmiCategory = NutritionCalculator().BmiCategory(bmi)
        return "{0:.2f} - {1}".format(bmi, bmiCategory)

    def CalculateEnergyNeeds(self, weight, height, age, gender):  
        energyNeeds = NutritionCalculator().MifflinStJeor(weight, height, 
                                                          age, gender)
        caloriesPerKilogram = NutritionCalculator().CaloriesPerKilogram(energyNeeds, 
                                                                        weight)
        return "{0:.0f} Calories ({1:.0f}cal/kg)".format(energyNeeds, 
                                                             caloriesPerKilogram)

    def CalculateIdealWeight(self, weight, height, gender):
        idealWeight = Weight(NutritionCalculator().IdealBodyWeight(height, gender), False)
        percentIdeal = NutritionCalculator().PercentIdealBodyWeight(weight.ConvertToMetric(), 
                                                                    idealWeight.ConvertToMetric())
        if percentIdeal > 125.0:
            adjustedWeight = Weight(NutritionCalculator().AdjustedBodyWeight(weight.ConvertToMetric(), 
                                                                             idealWeight.ConvertToMetric()), True)
            return "{0:.2f}kg or {1:.2f}lbs ({2:.2f}%)\n{3:.2f}kg or {4:.2f}lbs".format(idealWeight.ConvertToMetric(), 
                                                                                        idealWeight.ConvertToImperial(), 
                                                                                        percentIdeal,
                                                                                        adjustedWeight.ConvertToMetric(), 
                                                                                        adjustedWeight.ConvertToImperial())

        return "{0:.2f}kg or {1:.2f}lbs ({2:.2f}%)\nN/A".format(idealWeight.ConvertToMetric(), 
                                                                idealWeight.ConvertToImperial(),
                                                                percentIdeal)
    def openFactorPopup(self, mifflinValue):
        if len(mifflinValue.split('\n')) > 1:
            mifflinValue = mifflinValue.partition(' ')[0]
            p = FactorPopup(mifflinValue)
            p.open()


class NutritionApp(App):
    title = "Nutrition Buddy"

    def build(self):
        calculatorScreenManager = ScreenManager()
        calculatorScreenManager.add_widget(WelcomeScreen(name="Welcome"))
        calculatorScreenManager.add_widget(ConversionScreen(name="Conversions"))
        calculatorScreenManager.add_widget(MifflinStJeorScreen(name="Mifflin"))
        return calculatorScreenManager

    def on_pause(self):
        return True

if __name__ in ('__main__', '__android__'):
    NutritionApp().run()
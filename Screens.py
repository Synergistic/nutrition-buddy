from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty
from Measures import Height, Weight, Age, Gender, Volume, Factor, Temperature, Measure
from Calculator import NutritionCalculator
import re



class EnergyNeedsEquationScreen(Screen):
    adjustedBodyWeight = False
    
    def CollectBasicData(self, measures):
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
        return weight, height, gender, age
    
    def CalculateBMI(self, weight, height):
        bmi = NutritionCalculator().BodyMassIndex(weight, height)
        bmiCategory = NutritionCalculator().BmiCategory(bmi)
        return "BMI: {0:.2f} - {1}".format(bmi, bmiCategory)
    
    def CalculateIdealWeight(self, weight, height, gender):
        idealWeight = Weight(NutritionCalculator().IdealBodyWeight(height, 
                                                                   gender), 
                                                                   False)
        percentIdeal = NutritionCalculator().PercentIdealBodyWeight(weight.ConvertToMetric(), 
                                                                    idealWeight.ConvertToMetric())
        
        if percentIdeal > 125.0:
            adjustedWeight = Weight(NutritionCalculator().AdjustedBodyWeight(weight.ConvertToMetric(), 
                                                                             idealWeight.ConvertToMetric()), 
                                                                             True)
            self.adjustedBodyWeight = adjustedWeight.ConvertToMetric()
            print self.adjustedBodyWeight
            return "IBW: {0:.2f}kg || {1:.2f}lbs ({2:.2f}%)\nABW: {3:.2f}kg || {4:.2f}lbs".format(
                idealWeight.ConvertToMetric(), 
                idealWeight.ConvertToImperial(), 
                percentIdeal,
                adjustedWeight.ConvertToMetric(), 
                adjustedWeight.ConvertToImperial())
        
        self.adjustedBodyWeight = False
        print self.adjustedBodyWeight
        return "IBW: {0:.2f}kg || {1:.2f}lbs ({2:.2f}%)\nABW: N/A".format(
            idealWeight.ConvertToMetric(), 
            idealWeight.ConvertToImperial(),
            percentIdeal)
    
    def CalculateFluidNeeds(self, weight, age):
        print self.adjustedBodyWeight
        fluidNeeds = Volume(NutritionCalculator().FluidNeeds(self.adjustedBodyWeight, weight, age), True)
        return "Fluid: {0:.0f}mL || {1:.0f}oz".format(fluidNeeds.ConvertToMetric(), 
                                                  fluidNeeds.ConvertToImperial())       
    
    def closeKeyboard(self, *args):
        for textInput in args:
            textInput.focus = False
            
    def DisplayResults(self, results, currentCalc):
        self.manager.get_screen('Results').inputText = results[0]
        self.manager.get_screen('Results').resultsText = results[1]
        self.manager.get_screen('Results').currentCalculator = currentCalc    
    
    
class PennStateScreen(EnergyNeedsEquationScreen):
    
    def Calculations(self, measures):
        weight, height, gender, age = self.CollectBasicData(measures)
        
        if measures['tempUnit'] == 'C':
            temp = Temperature(measures['temp'], True)
        else:
            temp = Temperature(measures['temp'], False)
            
        ventilation = Measure(measures['ventilation'])
        inputText = "\n".join(['Weight: {0:.2f}kg | {1:.2f}lbs',
                               'Height: {2:.2f}cm | {3:.2f}in',
                               'Age: {4}', 
                               'Gender: {5}',
                               'Temperature: {6}C | {7}F',
                               'Ventilation: {8}']).format(weight.ConvertToMetric(), 
                                                      weight.ConvertToImperial(),
                                                      height.ConvertToMetric(),
                                                      height.ConvertToImperial(),
                                                      age, gender, 
                                                      temp.ConvertToMetric(),
                                                      temp.ConvertToImperial(),
                                                      ventilation)
        ibw = self.CalculateIdealWeight(weight, 
                                        height.ConvertToImperial(), 
                                        gender)
        results = "\n".join([
            self.CalculateEnergyNeeds(weight.ConvertToMetric(), 
                                      height.ConvertToMetric(), 
                                      age.value, gender,
                                      ventilation.value, 
                                      temp.ConvertToMetric()),
            self.CalculateFluidNeeds(weight.ConvertToMetric(),
                                     age), ' ',
            self.CalculateBMI(weight.ConvertToMetric(), 
                              height.ConvertToMetric()),
            ibw])
        self.manager.current = 'Results'
        return inputText, results


    def CalculateEnergyNeeds(self, weight, height, age, gender, ventilation, temp): 
        energyNeeds = NutritionCalculator().PennState(weight, height, 
                                                      age, gender, 
                                                      ventilation, temp)
        caloriesPerKilogram = NutritionCalculator().CaloriesPerKilogram(
            energyNeeds, weight)
        return "{0:.0f} Calories ({1:.0f}cal/kg)".format(energyNeeds, 
                                                         caloriesPerKilogram)
    
class MifflinStJeorScreen(EnergyNeedsEquationScreen):
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
    
    def Calculations(self, measures):

        weight, height, gender, age = self.CollectBasicData(measures)
        stress = Factor(measures['stress'])
        activity = Factor(measures['activity'])
        inputText = "\n".join(['Weight: {0:.2f}kg | {1:.2f}lbs',
                               'Height: {2:.2f}cm | {3:.2f}in',
                               'Age: {4}', 
                               'Gender: {5}']).format(weight.ConvertToMetric(), 
                                                      weight.ConvertToImperial(),
                                                      height.ConvertToMetric(),
                                                      height.ConvertToImperial(),
                                                      age, gender)
        ibw = self.CalculateIdealWeight(weight, 
                                   height.ConvertToImperial(), 
                                   gender)      
        results = "\n".join([
            self.CalculateEnergyNeeds(weight.ConvertToMetric(), 
                                      height.ConvertToMetric(), 
                                      age.value, gender,
                                      stress, activity),
            self.CalculateFluidNeeds(weight.ConvertToMetric(),
                                     age.value), ' ',
            self.CalculateBMI(weight.ConvertToMetric(), 
                              height.ConvertToMetric()),
            ibw])
        self.manager.current = 'Results'
        return inputText, results

    def CalculateEnergyNeeds(self, weight, height, age, gender, stress, activity):  
        energyNeeds = NutritionCalculator().MifflinStJeor(weight, height, 
                                                          age, gender)
        energyNeeds *= stress.value * activity.value
        caloriesPerKilogram = NutritionCalculator().CaloriesPerKilogram(
            energyNeeds, weight)
        return "{0:.0f} Calories ({1:.0f}cal/kg)".format(energyNeeds, 
                                                         caloriesPerKilogram)



class ResultsScreen(Screen):
    inputText = StringProperty('')
    resultsText = StringProperty('')
    currentCalculator = StringProperty('')

class WelcomeScreen(Screen):
    pass

class ConversionScreen(Screen):

    weightIsMetric = False
    heightIsMetric = False
    volumeIsMetric = False

    def ConvertMeasure(self, typeOfMeasure, measureToConvert):
        decimalCheck = re.compile('\d+(\.\d+)?')
        if decimalCheck.match(measureToConvert) != None:

            if typeOfMeasure == 'weight':
                measure = Weight(measureToConvert, self.weightIsMetric)
                isMetric = self.weightIsMetric
            elif typeOfMeasure == 'height':
                measure = Height(measureToConvert, self.heightIsMetric)
                isMetric = self.heightIsMetric
            elif typeOfMeasure == 'volume':
                measure = Volume(measureToConvert, self.volumeIsMetric)
                isMetric = self.volumeIsMetric
            if isMetric:
                return '{0:.2f}'.format(measure.ConvertToImperial())
            else:
                return '{0:.2f}'.format(measure.ConvertToMetric())
        return ''            

    def SetButtonText(self, buttonToChange):
        def swapUnit(unitToCheckFor, unitBool, textOptions):
            if unitToCheckFor in buttonToChange.text:
                unitBool = not unitBool
    
                if unitBool:
                    buttonToChange.text = textOptions[0]
                else:
                    buttonToChange.text = textOptions[1]
            return unitBool
                    
        self.heightIsMetric = swapUnit('cm', self.heightIsMetric, ['cm > in', 'in > cm'])
        self.weightIsMetric = swapUnit('kg', self.weightIsMetric, ['kg > lbs', 'lbs > kg'])
        self.volumeIsMetric = swapUnit('mL', self.volumeIsMetric, ['mL > oz', 'oz > mL'])


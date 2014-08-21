
from decimal import Decimal


class NutritionCalculator():

    def MifflinStJeor(self, weight, height, age, gender):
        '''Caloric needs based on Mifflin-St.Jeor Equation
        Males: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age) + 5.0
        Females: (9.99 * weight(kg)) + (6.25 * height(cm)) - (4.92 * age) - 161'''

        if gender.isMale:
            caloriesNeeded = ((Decimal('9.99') * weight) + 
                              (Decimal('6.25') * height) - 
                              (Decimal('4.92') * age) + Decimal('5.0'))
        else:
            caloriesNeeded = ((Decimal('9.99') * weight) +
                              (Decimal('6.25') * height) -
                              (Decimal('4.92') * age) - Decimal('161.0'))
        return caloriesNeeded

    def MifflinFactor(self, mifflinValue, factorToMultiply):
        return Decimal(str(mifflinValue)) * Decimal(factorToMultiply)


    def PennState2003B(self, mifflin, ventilation, maxTemp):
        return (mifflin * Decimal('0.96') + ventilation * Decimal('31') + 
                maxTemp * Decimal('167') - Decimal('6212'))

    def PennState2010(self, mifflin, ventilation, maxTemp):
        return (mifflin * Decimal('0.71') + ventilation * Decimal('64') + 
    maxTemp * Decimal('85') - Decimal('3085'))

    def PennState(self, weight, height, age, gender, ventilation, maxTemp):
        mifflin = self.MifflinStJeor(weight, height, age, gender)
        bmi = self.BodyMassIndex(weight, height)

        if  bmi < 30 or (age < 60 and bmi > 30):
            caloriesNeeded = self.PennState2003B(mifflin, ventilation, maxTemp)

        elif bmi > 30 and age > 60:
            caloriesNeeded = self.PennState2010(mifflin, ventilation, maxTemp)

        return caloriesNeeded

    def CaloriesPerKilogram(self, calories, weight):
        caloriesPerKilogram = calories / weight
        return caloriesPerKilogram  

    def BodyMassIndex(self, weight, height):
        """Calculates Body Mass Index(BMI):
        bmi = (weight(kg) / (height(meters)**2))"""

        bmi = weight / ((height / 100) ** 2)
        return bmi


    def BmiCategory(self, bmi):

        if bmi < 18.50:
            category = "Underweight"
        elif bmi >= 18.5 and bmi <= 24.99:
            category = "Normal"
        elif bmi > 24.99 and bmi <= 29.99:
            category = "Overweight"
        elif bmi > 29.99 and bmi <= 34.99:
            category = "Obese I"
        elif bmi > 34.99 and bmi <= 39.99:
            category = "Obese II"
        elif bmi > 39.99:
            category = "Obese III" 
        return category


    def IdealBodyWeight(self, heightInches, gender):
        """
        Calculates IBW  in pounds based on Hamwi method;
        Males: 106 + 6x
        Females: 100 + 5x
        X = number of inches over 60inches for height
        """
        if heightInches >= 60:
            inchesOverSixty = heightInches - 60

            if gender.isMale:
                ibw = (inchesOverSixty * 6) + 106
            else:
                ibw = (inchesOverSixty * 5) + 100

        elif heightInches < 60:
            inchesUnderSixty = 60 - heightInches

            if gender.isMale:
                ibw = 106 - (inchesUnderSixty * 3)
            else:
                ibw = 100 - (inchesUnderSixty * (Decimal('2.5')))

        return ibw        

    def PercentIdealBodyWeight(self, weight, ibw):
        return (weight / ibw) * Decimal('100.0')


    def AdjustedBodyWeight(self, weight, ibw):
        return (((weight - ibw) *
                 Decimal('0.25')) + ibw)
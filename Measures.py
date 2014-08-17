from decimal import Decimal

class Measure:
    
    def __init__(self, value):
        self.value = Decimal(str(value))
        
    def __str__(self):
        return str(self.value)
    
class Height(Measure):
    
    def __init__(self, value, isMetric):
        Measure.__init__(self, value)
        self.isMetric = isMetric
        self.FACTOR = Decimal('2.54')
        
    def __str__(self):
        valueStr = "{0:.2f}{1}"
        
        if self.isMetric:
            unit = "cm"
        else:
            unit = "in"
            
        return valueStr.format(self.value, unit)
        
    def ConvertToMetric(self):
        if not self.isMetric:
            self.value *= self.FACTOR
            self.isMetric = True
        return self.value
            
    def ConvertToImperial(self):
        if self.isMetric:
            self.value /= self.FACTOR
            self.isMetric = False
        return self.value
 
 
class Weight(Measure):

    def __init__(self, value, isMetric):
        Measure.__init__(self, value)
        self.isMetric = isMetric
        self.FACTOR = Decimal('2.2')
        
    def __str__(self):
        valueStr = "{0:.2f}{1}"
        
        if self.isMetric:
            unit = "kg"
        else:
            unit = "lbs"
            
        return valueStr.format(self.value, unit)
        
    def ConvertToMetric(self):
        if not self.isMetric:
            self.value /= self.FACTOR
            self.isMetric = True
        return Decimal(str(self.value))
            
    def ConvertToImperial(self):
        if self.isMetric:
            self.value *= self.FACTOR
            self.isMetric = False
        return Decimal(str(self.value))
    
class Age(Measure):
    pass

class Gender():
    
    def __init__(self, isMale):
        self.isMale = isMale
    
    def __str__(self):
        if self.isMale:
            return "Male"
        else:
            return "Female"
        
    def ReverseGender(self):
        self.isMale = not self.isMale
        
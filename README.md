Nutrition Buddy 1.0b
====================

Python calculator for clinical nutrition

Built using the Kivy framework, Nutrition Buddy aims to make
clinical nutrition calculations quick and simple.

One feature of NB is a converter that easily converts height 
and weight values between imperial (lbs/in) and metric (kg/cm) u
nits live.

The main function of NB is determining energy needs. Given
an individual's height & weight (in metric or imperial),
age, and gender, NB will compute their Basal Metabolic Rate
(BMR) utilizing the Mifflin-St.Jeor equation which is currently
the gold standard of predictive equations for determing calorie
expenditure. In addition to providing the BMR to the user, NB
will also take the same information and compute Body Mass Index
(BMI), Ideal Body Weight (IBW), Percentage of IBW (%IBW), and 
finally Adjusted Body Weight (ABW) if necessary. This provides
an all-in-one solution for individuals who will need to compute
all these values on a regular basis.

Planned for the very near future is the addition of the 
Penn-State equation which is utilized in crtically ill, vent-
dependent individuals. This will take into account the mifflin
equation with some added factors such as max temperature in the
passed 24 hours (Tmax) and ventilation rate (Ve).

Nutrition Buddy is slated to be released on the Android Play Store
in early September. Keep an eye out for it!

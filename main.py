from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from Screens import MifflinStJeorScreen, WelcomeScreen, ConversionScreen, ResultsScreen, PennStateScreen


class NutritionApp(App):
    title = "Nutrition Buddy"

    def build(self):
        calculatorScreenManager = ScreenManager()
        calculatorScreenManager.add_widget(WelcomeScreen(name="Welcome"))
        calculatorScreenManager.add_widget(ConversionScreen(name="Conversions"))
        calculatorScreenManager.add_widget(MifflinStJeorScreen(name="Mifflin"))
        calculatorScreenManager.add_widget(PennStateScreen(name="PennState"))
        calculatorScreenManager.add_widget(ResultsScreen(name='Results'))
        return calculatorScreenManager

    def on_pause(self):
        return True

if __name__ in ('__main__', '__android__'):
    NutritionApp().run()

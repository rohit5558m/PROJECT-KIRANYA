import kivy
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.video import Video

kivy.require('2.0.0')

class Test(App):
    def build(self):
        la=BoxLayout(orientation='vertical')
        but = Button(text = "HIda")
        img = Video(source="vid.mp4")
        la.add_widget(img)
        la.add_widget(but)
        return la
    

if __name__ == "__main__":
    app = Test()
    app.run()


from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import subprocess

class MyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        self.label = Label(text="Presiona el botón para ejecutar el script", font_size='20sp')
        button = Button(text='Ejecutar Script', font_size='20sp')
        button.bind(on_press=self.run_script)
        layout.add_widget(self.label)
        layout.add_widget(button)
        return layout

    def run_script(self, instance):
        # Aquí cambias la ruta del script y cómo lo ejecutas según tu entorno y necesidades
        result = subprocess.run(['python', 'Model.py'], capture_output=True, text=True)
        if result.returncode == 0:
            self.label.text = 'Script ejecutado correctamente:\n' + result.stdout
            self.stop()
        else:
            self.label.text = 'Error al ejecutar el script:\n' + result.stderr

if __name__ == '__main__':
    MyApp().run()
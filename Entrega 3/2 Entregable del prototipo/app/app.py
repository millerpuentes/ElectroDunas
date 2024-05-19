# Importaciones necesarias de los módulos de Kivy y subprocess
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import subprocess

class MyApp(App):
    """
    Clase principal de la aplicación que hereda de Kivy's App.
    Esta clase construye la interfaz gráfica y maneja la ejecución de un script externo.
    """
    def build(self):
        """
        Método para construir la interfaz gráfica de la aplicación.
        
        Retorna:
            BoxLayout: El layout principal que contiene la etiqueta y el botón.
        """
        # Crear un BoxLayout vertical
        layout = BoxLayout(orientation='vertical')
        
        # Crear una etiqueta con un mensaje inicial
        self.label = Label(text="Presiona el botón para ejecutar el script", font_size='20sp')
        
        # Crear un botón con el texto 'Ejecutar Script'
        button = Button(text='Ejecutar Script', font_size='20sp')
        
        # Asignar la función run_script al evento on_press del botón
        button.bind(on_press=self.run_script)
        
        # Agregar la etiqueta y el botón al layout
        layout.add_widget(self.label)
        layout.add_widget(button)
        
        # Retornar el layout para que sea mostrado
        return layout

    def run_script(self, instance):
        """
        Método que se ejecuta al presionar el botón. Ejecuta el script externo 'Model.py'
        y actualiza la etiqueta con el resultado.
        
        Parámetros:
            instance (Button): La instancia del botón que fue presionado.
        """
        # Ejecutar el script 'Model.py' y capturar la salida
        result = subprocess.run(['python', 'Model.py'], capture_output=True, text=True)
        
        # Verificar si el script se ejecutó correctamente
        if result.returncode == 0:
            # Actualizar la etiqueta con la salida del script
            self.label.text = 'Script ejecutado correctamente:\n' + result.stdout
            # Detener la aplicación después de mostrar el resultado
            self.stop()
        else:
            # Actualizar la etiqueta con el mensaje de error
            self.label.text = 'Error al ejecutar el script:\n' + result.stderr

# Punto de entrada de la aplicación
if __name__ == '__main__':
    # Iniciar la aplicación
    MyApp().run()

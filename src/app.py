from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.clock import Clock
from kivy.config import Config
from kivy.core.window import Window
from samila import Projection
from src.utils import generate_image, save_config
import random
import os
import uuid
import threading

class SamilaRTApp(App):
    def build(self):
        Config.set('graphics', 'resizable', '0')
        Window.size = (720, 480)
        Window.minimum_width = 720
        Window.minimum_height = 480
        Window.maximum_width = 720
        Window.maximum_height = 480
        self.title = 'SamilaRT - GUI'
        layout = GridLayout(cols=1, spacing=10, padding=10, size=(720, 480))

        self.label = Label(text='', size_hint=(None, None), size=(180, 50))
        Clock.schedule_once(lambda dt: self.start_typing_animation(), 1)

        self.image_widget = Image()
        button_layout = GridLayout(cols=3, spacing=10, size_hint=(None, None), size=(500, 50))

        self.button = Button(text='Generate and Plot', background_color=(0, 1, 0, 1))
        self.seed_input = TextInput(text='', hint_text='Enter seed (enter random number)')
        self.projection_spinner = Spinner(
            text='Select projection',
            values=['Rectilinear', 'Polar', 'Aitoff', 'Hammer', 'Lambert', 'Mollweide']
        )
        self.button.bind(on_press=self.generate_and_plot)

        button_layout.add_widget(self.seed_input)
        button_layout.add_widget(self.projection_spinner)
        button_layout.add_widget(self.button)

        layout.add_widget(self.label)
        layout.add_widget(self.image_widget)
        layout.add_widget(button_layout)

        return layout

    def start_typing_animation(self):
        text = "Created by Gerry Auditya"
        typing_speed = 0.10
        typing_index = 0

        def update_label_text(dt):
            nonlocal typing_index
            if typing_index <= len(text):
                self.label.text = text[:typing_index]
                typing_index += 1
                Clock.schedule_once(update_label_text, typing_speed)

        Clock.schedule_once(update_label_text, typing_speed)

    def generate_and_plot(self, instance):
        self.button.disabled = True
        self.button.text = "Processing..."

        threading.Thread(target=self.process_and_plot, daemon=True).start()

    def process_and_plot(self):
        seed = self.seed_input.text.strip()
        seed = random.randint(1, 99999999) if seed == '' else int(seed)

        projection_mapping = {
            'Rectilinear': Projection.RECTILINEAR,
            'Polar': Projection.POLAR,
            'Aitoff': Projection.AITOFF,
            'Hammer': Projection.HAMMER,
            'Lambert': Projection.LAMBERT,
            'Mollweide': Projection.MOLLWEIDE
        }
        projection = projection_mapping.get(self.projection_spinner.text, Projection.RECTILINEAR)

        print("\033[1;32mUsing seed =", seed, "\033[0m")
        print("\033[1;32mUsing projection =", projection, "\033[0m")

        output_folder = "Output"
        os.makedirs(output_folder, exist_ok=True)

        filename = str(uuid.uuid4())
        folder_name = os.path.join("Output", filename)
        os.makedirs(folder_name, exist_ok=True)

        save_config(folder_name, filename, seed, self.projection_spinner.text)

        image_path = generate_image(seed, projection, folder_name, filename)

        Clock.schedule_once(lambda dt: self.update_image_widget(image_path))

    def update_image_widget(self, image_path):
        self.image_widget.source = image_path
        self.enable_button()

    def enable_button(self):
        self.button.disabled = False
        self.button.text = "Generate and Plot"

if __name__ == '__main__':
    SamilaRTApp().run()
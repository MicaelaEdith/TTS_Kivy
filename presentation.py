from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.core.text import LabelBase
from kivy.utils import get_color_from_hex
from functions import TTS_Kivy
from kivy.uix.switch import Switch
from kivy.uix.actionbar import ActionBar, ActionView, ActionButton
from kivy.uix.dropdown import DropDown
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from csv_functions import *
from app_data import *

LabelBase.register(name='MyFont', fn_regular='assets/NotoSans-VariableFont_wdthwght.ttf')

class MyGridLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = [0, 0, 0, 0]
        self.spacing = 18
        self.tts = TTS_Kivy()
        self.selection_l = ''
        self.config = read_config()
        self.theme = False
        self.lan_menu = 'en'

        if self.config:
            if self.config[0] == 'True':
                self.theme = True
            else:
                self.theme = False
            self.lan_menu = self.config[1]


        Window.borderless = False
        self.update_colors()

        action_bar = BoxLayout(size_hint_y=None, height=45, padding=[18, 0, 0, 0], orientation='horizontal', spacing=10)
        
        action_view = BoxLayout(size_hint=(1, 1), padding=[0, 0, 0, 0], orientation='horizontal', spacing=10)

        self.theme_dropdown = DropDown()
        self.light_button = Button(
            text='Light',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.light_button.bind(on_press=lambda x: self.toggle_theme(True))
        self.dark_button = Button(
            text='Dark',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.dark_button.bind(on_press=lambda x: self.toggle_theme(False))
        self.theme_dropdown.add_widget(self.light_button)
        self.theme_dropdown.add_widget(self.dark_button)

        self.theme_button = ActionButton(text='Theme', background_color=self.spinner_background_color,font_name='MyFont',color=self.text_color)
        self.theme_button.bind(on_release=self.theme_dropdown.open)
        action_view.add_widget(self.theme_button)

        self.language_dropdown = DropDown()
        self.english_button = Button(
            text='English',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.english_button.bind(on_release=lambda btn: self.update_menu('en'))
        self.spanish_button = Button(
            text='Spanish',
            size_hint_y=None,
            height=44,
            background_color=self.button_color,
            color=self.text_color,
            padding=[5, 5],
            border=(1, 1, 1, 1),
            font_name='MyFont'
        )
        self.spanish_button.bind(on_release=lambda btn: self.update_menu('es'))
        self.language_dropdown.add_widget(self.english_button)
        self.language_dropdown.add_widget(self.spanish_button)

        self.language_button = ActionButton(text='Language', background_color=self.spinner_background_color, font_name='MyFont',color=self.text_color)
        self.language_button.bind(on_release=self.language_dropdown.open)
        action_view.add_widget(self.language_button)

        action_bar.add_widget(action_view)
        self.add_widget(action_bar)

        Window.clearcolor = self.window_background_color

        row1 = BoxLayout(orientation='horizontal', spacing=30, size_hint_y=None, height=50, padding=[18, 0, 0, 0])

        self.spinner = Spinner(
            text='Select a voice',
            values=["tts_models/es/css10/vits","tts_models/multilingual/multi-dataset/your_tts","tts_models/es/mai/tacotron2-DDC"],
            size_hint=(None, None),
            size=(220, 35),
            background_color=self.spinner_background_color,
            color=self.text_color,
            font_size='18sp',
            font_name='MyFont'
        )
        
        self.spinner.bind(text=self.on_spinner_select)
        row1.add_widget(self.spinner)
        self.tts.update_model_spinner(self.spinner, 'All')

        self.spinner_l = Spinner(
            text='lan',
            values=['All', 'En', 'Sp'],
            size_hint=(None, None),
            size=(70, 35),
            background_color=self.spinner_background_color,
            color=self.text_color,
            font_size='18sp',
            font_name='MyFont'
        )

        self.spinner_l.bind(text=self.on_language_select)
        row1.add_widget(self.spinner_l)

        self.add_widget(row1)

        padding_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        padding_layout.padding = [18, 0, 0, 0]
        self.text_input = TextInput(
            hint_text='Type here',
            size_hint=(None, None),
            size=(500, 300),
            multiline=True,
            font_size='16sp',
            font_name='MyFont',
            background_color=self.window_background_color,
            foreground_color=self.text_color,
            cursor_color=self.text_color, 
            border=(1, 1, 1, 1),
            readonly=False,
            text_validate_unfocus=True,
        )
        padding_layout.add_widget(self.text_input)
        self.add_widget(padding_layout)

        row2 = BoxLayout(orientation='horizontal', spacing=20, size_hint_y=None, height=50, padding=[18, 4, 0, 18])
        self.download_button = Button(
            text='Download',
            size_hint=(None, None),
            size=(105, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        self.download_button.bind(on_press=self.on_download_button_press)

        row2.add_widget(self.download_button)

        self.accept_button = Button(
            text='Try',
            size_hint=(None, None),
            size=(95, 40),
            background_color=self.button_color,
            color=self.text_color,
            border=(1, 1, 1, 1),
            font_size='18sp',
            font_name='MyFont'
        )
        self.accept_button.bind(on_press=self.on_accept_button_press)

        row2.add_widget(self.accept_button)
        self.add_widget(row2)
        self.update_menu(self.lan_menu)
        self.on_language_select(self.spinner, 'All')

    def update_colors(self):
        if not self.theme:          # dark
            self.action_background_color_hex = '#090909'
            self.window_background_color_hex = '#090909'
            self.button_color_hex = '#323232'
            self.spinner_background_color_hex = '#1a1a1a'
            self.text_color_hex = '#559e53'
            self.cursor_color_hex = '#ffffff' #'#559e53'
            self.selection_color_hex = '#323232'
        else:                       # light
            self.action_background_color_hex = '#0ffff0'
            self.window_background_color_hex = '#f2f5f2'
            self.button_color_hex = '#8d908d'
            self.spinner_background_color_hex = '#8d908d'
            self.text_color_hex = '#559e53'
            self.cursor_color_hex = '#ffffff' #'#559e53'
            self.selection_color_hex = '#8d908d'

        self.window_background_color = get_color_from_hex(self.window_background_color_hex)
        self.button_color = get_color_from_hex(self.button_color_hex)
        self.spinner_background_color = get_color_from_hex(self.spinner_background_color_hex)
        self.text_color = get_color_from_hex(self.text_color_hex)
        self.cursor_color = get_color_from_hex(self.cursor_color_hex)
        self.selection_color = get_color_from_hex(self.selection_color_hex)

        Window.clearcolor = self.window_background_color
              
    def toggle_theme(self, value):
        self.theme = value
        self.update_colors()
        self.apply_colors_to_widgets()
        self.theme_dropdown.dismiss()
        write_config(str(self.theme), self.lan_menu)

    def apply_colors_to_widgets(self):
        self.theme_button.background_color = self.spinner_background_color
        self.theme_button.color = self.text_color
        self.language_button.background_color = self.spinner_background_color
        self.language_button.color = self.text_color

        self.light_button.background_color = self.button_color
        self.light_button.color = self.text_color
        self.dark_button.background_color = self.button_color
        self.dark_button.color = self.text_color

        self.english_button.background_color = self.button_color
        self.english_button.color = self.text_color
        self.spanish_button.background_color = self.button_color
        self.spanish_button.color = self.text_color

        self.spinner.background_color = self.spinner_background_color
        self.spinner.color = self.text_color
        self.spinner_l.background_color = self.spinner_background_color
        self.spinner_l.color = self.text_color

        self.download_button.background_color = self.button_color
        self.download_button.color = self.text_color
        self.accept_button.background_color = self.button_color
        self.accept_button.color = self.text_color

        self.text_input.background_color = self.window_background_color
        self.text_input.foreground_color = self.text_color
        self.text_input.cursor_color = self.text_color 
        self.text_input.selection_color = self.text_color

    def on_download_button_press(self, instance):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = self.spinner.text
        self.selected_model = selected_model_path
        self.tts.execute_action(self.text_input.text,self.selected_model)


    def on_accept_button_press(self, instance):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = self.spinner.text
        self.selected_model = selected_model_path
        self.tts.audio_speaker(self.text_input.text,self.selected_model)

    def on_spinner_select(self, spinner, text):
        model_dict = self.tts.classify_and_list_models()
        selected_model_path = text
        self.selected_model = selected_model_path

    def on_language_select(self,spinner, text):
        spinner = self.spinner
        self.selection_l = text
        self.spinner.values = self.tts.update_model_spinner(spinner, self.selection_l)
        self.language_dropdown.dismiss()
        
        
    def update_menu(self, text):
        if text=='en':
            self.theme_button.text = 'Theme'
            self.language_button.text = 'Language'
            self.accept_button.text = 'Try'
            self.download_button.text = 'Download'
            self.dark_button.text ='Dark'
            self.light_button.text ='Light'   
            self.spanish_button.text='Spanish'
            self.english_button.text='English'
            self.spinner.text='Select a voice'
            self.text_input.hint_text='Type here'
            self.spinner_l.text='lan'
            self.spinner_l.values=['All', 'En', 'Sp']
            self.lan_menu = 'en'
            
        else:
            self.theme_button.text = 'Modo'
            self.language_button.text = 'Idioma'
            self.accept_button.text = 'Probar'
            self.download_button.text = 'Descargar'
            self.dark_button.text ='Oscuro'
            self.light_button.text ='Claro'
            self.spanish_button.text='Español'
            self.english_button.text='Ingles'
            self.spinner.text='Seleccionar voz'
            self.text_input.hint_text='Escriba aquí'
            self.spinner_l.text='len'
            self.spinner_l.values=['Todas', 'In', 'Es']
            self.lan_menu = 'es'
        write_config(str(self.theme), self.lan_menu)

    def on_request_close(self, *args):
        return False
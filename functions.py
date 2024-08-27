from kivy.uix.popup import Popup
from kivy.uix.label import Label
from TTS.utils.manage import ModelManager
from TTS.api import TTS
from datetime import datetime
from kivy.uix.spinner import Spinner
from pydub import AudioSegment
from pydub.playback import play
from app_data import voice_models
import io

class TTS_Kivy:
    def __init__(self):
        self.model_manager = ModelManager()
        self.models = self.model_manager.list_models()
        self.multilingual_models = []
        self.es_models = []
        self.en_models = []
        self.filter = False
        self.filter_on = 'all'
        self.classify_and_list_models()
        print('lista 1:')
        print(self.model_manager.list_models())
        print('fin lista 1')

    def list(self):
        if not self.filter or self.filter_on == 'all':
            list_ = self.classify_and_list_models()
        elif self.filter_on == 'en':
            list_ = self.en_models
        elif self.filter_on == 'es':
            list_ = self.es_models
        print('return_list_ : ')
        print(list_)

        return list_

    def filter(self, lan):
        self.lan = lan
        models_ = [model for model in self.models if self.lan in model]
        return models_

    def execute_action(self, text_input, model):
        tts = TTS(model_name=model)
        text = text_input.text
        tts.tts_to_file(text=text, file_path="output" + str(datetime.now()) + ".wav")
        print(f'Action executed with text: {text}')

    def classify_and_list_models(self):
        model_dict = {}

        for path in self.models:
            parts = path.split('/')

            if 'multilingual' in parts:
                index = parts.index('multilingual') + 2
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.multilingual_models.append(model_name)
                    model_dict[model_name] = path

            elif 'es' in parts:
                index = parts.index('es') + 1
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.es_models.append(model_name)
                    model_dict[model_name] = path

            elif 'en' in parts:
                index = parts.index('en') + 1
                if index < len(parts):
                    model_name = parts[index].replace('_', ' ').capitalize()
                    self.en_models.append(model_name)
                    model_dict[model_name] = path

        return model_dict

    def audio_speaker(self, text, model):
        print('paso modelo speaker')
        print('modelo = ', model)
        tts = TTS(model_name=model)
        audio_data = tts.tts(text=text)
        audio_segment = AudioSegment(
            data=io.BytesIO(audio_data).getvalue(),
            sample_width=2,
            frame_rate=22050,
            channels=1
        )
        play(audio_segment)

    def update_model_spinner(self, spinner, selected_language):
        values = []

        if selected_language == 'All' or selected_language == 'Todas' or not selected_language:
            values = list(self.multilingual_models + self.es_models + self.en_models)
        elif selected_language == 'Multilingual':
            values = list(self.multilingual_models)
        elif selected_language == 'En' or selected_language == 'In':
            values = list(self.en_models)
        elif selected_language == 'Es' or selected_language == 'Sp':
            values = list(self.es_models)
        
        spinner.values = values
        spinner.text = 'Select a voice' if not values else values[0]

        print(values)
        return values

    def update_model_data(new_data):
        voice_models.clear()
        for model in new_data:
            voice_models[model['id']] = model['name']
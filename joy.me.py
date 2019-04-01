#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This is demo code for like@home written by Pierogi"""
import argparse
import locale
import logging
import signal
import sys
import time

from aiy.board import Board, Led
from aiy.cloudspeech import CloudSpeechClient
import aiy.assistant.grpc
from aiy.voice import tts
from aiy.voice.audio import AudioFormat, play_wav
from aiy.board import Board
from aiy.leds import Leds, Pattern, PrivacyLed, RgbLeds, Color


SOUND_PATH = '/home/pi/AIY-voice-kit-python/src/microsoft.wav'



def get_hints(language_code):
    if language_code.startswith('en_'):
        return ('what',
                'tonight',
                'eight',
                'join')
    return None

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def main():
    logging.basicConfig(level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Mockup pierogi, like@home.')
    parser.add_argument('--language', default=locale_language())
    args = parser.parse_args()

    logging.info('\n Initializing for language %s...', args.language)
    hints = get_hints(args.language)
    client = CloudSpeechClient()
    with Board() as board:
      with Leds() as leds:
        logging.info('\n Main void initialized.', args.language)
        play_wav(SOUND_PATH)  
        text="""Joyme, is ready to listen!"""
        tts.say(text,lang='en-US')

        while True:
            leds.update(leds.rgb_on(Color.BLUE))
            board.button.wait_for_press()
            leds.update(leds.rgb_on(Color.YELLOW))    
            text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
            while text is None:
                leds.update(leds.rgb_on(Color.RED))
                text="""Mamma meea! I could not hear you, can you reapeat?"""
                tts.say(text,lang='en-US')
                leds.update(leds.rgb_on(Color.YELLOW))
                text = client.recognize(language_code=args.language,
                                    hint_phrases=hints)
                continue

            logging.info('\n You said: "%s"' % text)
            leds.update(leds.rgb_on(Color.GREEN))
            text = text.lower()


            if ('join' and ('8' or 'eight')) in text:
                leds.update(leds.rgb_on(Color.GREEN))
                text="""Well. What kind of activity do you have in mind?"""
                tts.say(text,lang='en-US')
                leds.update(leds.rgb_on(Color.BLUE))
                time.sleep(1)
                leds.update(leds.rgb_on(Color.GREEN))
                text="""Movie nights, maybe?"""
                tts.say(text,lang='en-US')
                leds.update(leds.rgb_on(Color.BLUE))
                board.button.wait_for_press()
                leds.update(leds.rgb_on(Color.YELLOW))    
                text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                while text is None:
                    leds.update(leds.rgb_on(Color.RED))
                    text="""Mamma meea! I could not hear you, can you reapeat?"""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.YELLOW))
                    text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                    continue
                logging.info('You said: "%s"' % text)
                leds.update(leds.rgb_on(Color.GREEN))
                text = text.lower()
                if 'no' in text:
                    text="""ok. Never mind.
                    """
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))
                elif 'yes' in text:
                    text="""Movie at eight, ok. Check back later if someone has joined you."""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))

            if ('what' and 'tonight') in text:
                leds.update(leds.rgb_on(Color.GREEN))
                text="""Well. Chris, room 21, is hosting a party. Giulia is watching Game of thrones at 10. """
                tts.say(text,lang='en-US')
                leds.update(leds.rgb_on(Color.BLUE))
                time.sleep(2)
                leds.update(leds.rgb_on(Color.YELLOW))    
                text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                while text is None:
                    leds.update(leds.rgb_on(Color.RED))
                    text="""Mamma meea! I could not hear you, can you reapeat?"""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.YELLOW))
                    text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                    continue
                logging.info('You said: "%s"' % text)
                leds.update(leds.rgb_on(Color.GREEN))
                text = text.lower()
                if 'Giulia' in text:
                    text="""ok. 10 o'clock video room."""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))
                elif 'party' in text:
                    text="""ok, I will text Chris."""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))

            if ('laundry') in text:
                leds.update(leds.rgb_on(Color.GREEN))
                text="""there's a free spot on tuesday from 8 to 10. Do you want to book it? """
                tts.say(text,lang='en-US')
                leds.update(leds.rgb_on(Color.BLUE))
                time.sleep(2)
                leds.update(leds.rgb_on(Color.YELLOW))    
                text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                while text is (None or not('yes' or 'no')):
                    leds.update(leds.rgb_on(Color.RED))
                    text="""Mamma meea! I could not hear you, can you reapeat?"""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.YELLOW))
                    text = client.recognize(language_code=args.language,
                                        hint_phrases=hints)
                    continue
                logging.info('You said: "%s"' % text)
                leds.update(leds.rgb_on(Color.GREEN))
                text = text.lower()
                if 'no' in text:
                    text="""ok. Never mind.
                    """
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))
                elif 'party' in text:
                    text="""Done."""
                    tts.say(text,lang='en-US')
                    leds.update(leds.rgb_on(Color.BLUE))        
            

if __name__ == '__main__':
    main()

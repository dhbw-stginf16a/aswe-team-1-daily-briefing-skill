#!/usr/bin/env python3

import logging
import random

logger = logging.getLogger(__name__)

quotes = [
    'Arbeit ist Freizeit!',
    'Wachstum ist Fortschritt!',
    'Sicherheit ist Freiheit!',
    'Ich arbeite gern für meinen Konzern!',
    'Ich bin nur froh im Großraumbüro!',
    'Wir haben uns alle lieb im Betrieb!',
    'Mein größter Schatz - mein Arbeitsplatz!',
    'Ich lauf\' bis in den Jemen, für mein Unternehmen!',
    'Ich schwimm\' bis nach Birma, für meine Firma!',
    'Die schönste Musik - der Sound der Fabrik!',
    'Frage nicht, was dein Arbeitsplatz für dich tun kann. Frage, was du für deinen Arbeitsplatz tun kannst.',
    'Die schönste Zeit ... ist die Arbeit!',
    'Ich kenne keine Parteien mehr, ich kenne nur noch Arbeitsplätze!'
]

def getMotivationalQuote():
    return random.choice(quotes)

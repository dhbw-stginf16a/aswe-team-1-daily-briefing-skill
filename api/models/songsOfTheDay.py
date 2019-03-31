#!/usr/bin/env python3

import logging
import random

logger = logging.getLogger(__name__)

songs = [
    'https://www.youtube.com/watch?v=hPUvhMSRmUg',
    'https://www.youtube.com/watch?v=VnT7pT6zCcA',
    'https://open.spotify.com/track/0F8zB7pyrLpZ6w38hT8YtW?si=QeURmeI1S0evcAZoFWunrg',
    'https://open.spotify.com/track/00cnjh154N2lcGCbeXYyY7?si=5uKg14NlTMufJ48EKPhL_A',
    'https://www.youtube.com/watch?v=MLcUKuoL6-Y',
    'https://www.youtube.com/watch?v=aPtr43KHBGk',
    'https://www.youtube.com/watch?v=NRj3Vu0yUF4',
    'https://www.youtube.com/watch?v=vjuw4nDlEtw',
    'https://www.youtube.com/watch?v=wYOM00Xx29c'
]

def getSong():
    return random.choice(songs)

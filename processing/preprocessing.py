from nltk.stem import PorterStemmer
import re

ps = PorterStemmer()
from nltk.corpus import stopwords

abbr_expand = { 'mlg': 'main landing gear', 'nlg': 'node landing gear', 
               'cvr': 'cockpit voice recorder', 'eng': 'engine', 'rdr': 'Radar Data Recording Replay',
              'nav': 'navigation', 'fms': 'flight management systems', 'navdata': 'navigation database',
              'tcas': 'traffic alert collision avoidance system', 'psi': 'pressure', 'psid': 'pressure difference',
              'insp': 'inspection', 'deec': ' Digital Electronic Engine Control', 'lav': 'lavatory',
              'pbe': 'Portable breathing equipment', 'hyd': 'HYDRAULIC', 'paintwork': 'paint work',
              'oxy': 'oxygen'}
incorrectly_spelt_words = ['vacuum', '']
stop = set(stopwords.words('english'))
stop.update({ 'please', 'pls', '' })

def processword(w):
    w = w.lower()
    w = re.sub('[0-9]', '', w)
    w = abbr_expand.get(w, w)
    if len(w) > 3:
        if w.endswith('n\'t'):
            return 'not' if w.replace('n\'t', '') in stop else w 
        else:
            return '' if w in stop and w != 'not' else w 
    else:
        return w.replace('\\', '') 

def preprocessor(sqk_desc):
    sqk_desc = ' '.join([' '.join((ps.stem(pw) for pw in processword(w).split())) for w in sqk_desc.split()])
    return re.sub('[-]', '', re.sub('[^A-Za-z0-9- ]', ' ', sqk_desc.upper()))

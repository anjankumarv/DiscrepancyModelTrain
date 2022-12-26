from nltk.stem import PorterStemmer
import re
import enchant
from fuzzywuzzy import fuzz
ps = PorterStemmer() 
from nltk.corpus import stopwords
import logging
import pathlib
import num2words

# logging.basicConfig(filename=r'C:\Users\anjanv\Desktop\IMRO\ToAnalystReview\log1.txt',
#                             filemode='a',
#                             format='%(asctime)s %(message)s',
#                             datefmt='%H:%M:%S',
#                             level=logging.INFO)

# logging.info("Starting")
logger = logging.getLogger('preprocessing')

abbr_expand = { 'mlg': 'main landing gear', 'nlg': 'nose landing gear', 
               'cvr': 'cockpit voice recorder', 'eng': 'engine', 'rdr': 'radar data recording replay',
              'nav': 'navigation', 'fms': 'flight management systems', 'navdata': 'navigation database',
              'tcas': 'traffic alert collision avoidance system', 'psi': 'pressure', 'psid': 'pressure difference',
              'insp': 'inspection', 'eec': 'electronic engine control', 'deec': ' digital electronic engine control', 
              'lav': 'lavatory', 'pbe': 'portable breathing equipment', 'hyd': 'hydraulic', 
              'paintwork': 'paint work', 'oxy': 'oxygen', 'hmu':'hydromechanical unit', 'me': 'multi-engine multi engine', 
              'tp': 'turboprop', 'ib': 'inboard', 'ob': 'outboard', 'ulb': 'underwater locator becon',
              'egpws':'enhanced ground proximity warning systems', 'ioc': 'i/o concentrator',
              'elt':'emergency locator transmitter', 'fdr':'flight data recorder', 
              'aux':'auxiliary', 'fadec': 'full authority digital engine control',
              'lui': 'low utilization inspection', 'lube': 'lubricant', 'lav': 'lavoratory',
              'f.c.u': 'fuel control unit', 'fcu': 'fuel control unit', 'assy': 'assembly',
              'eng': 'engine', 'temp': 'temperature', 'c/w': 'comply with', 'cw': 'comply with',
              'microbial': 'microbiological', 'lp': 'low pressure',
              'hsta': 'horizontal stabilizer trim actuator', 'afd': 'adaptive flight display',
              'ccp': 'cursor control panel', 'leftand': 'left hand', 'xmission': 'emission',
              'overwing': 'over wing', 'pretensioned': 'pre tensioned', 'doublers': 'doubler',
              'adc': 'air data computer', 'inb': 'inbound', 'dcu': 'data control unit', 
              'gcu': 'generator control unit', 'adm': 'admair data modules', 
              'adahrs': 'air data attitude heading reference systems', 'dadc': 'digital air data computers', 'flt': 'flight'}
              #TODO: ENVIROSYSTEMS

position_map =  {'r/h':'right', 'l/h':'left', 'rh':'right', 'lh':'left', 'fwd':'forward', 'bwd':'backward', 
'mid': 'middle', 'ckpt': 'cockpit', 'ib': 'inboard', 'ob': 'outboard', 'i/b': 'inboard', 'o/b': 'outboard',
'lib': 'left inboard', 'rib': 'right inboard', 'lob': 'left outboard','rob': 'right outboard',
 'e1ob': 'enginer left outboard', 'e2ob': 'enginer right outboard', 'e1': 'engine left position_one', 
 'e2': 'engine right position_two'}
 #'no.1': 'left', 'no.2': 'right'}

abbr_expand.update(position_map)

position_map.update({
    '1': 'engine left position_one', '2': 'engine right position_two',
    'r/h':'right engine', 'l/h':'left engine', 'rh':'right engine', 'lh':'left engine',
})

incorrectly_spelt_words = ['vacuum', '']
stop = set(stopwords.words('english'))
# print('not' in stop)
stop.update({ 'please', 'pls', '' })
parent_dir = pathlib.Path(__file__).parent.parent
dict = enchant.DictWithPWL("en_US", r"resources\domain_words_v2.txt") #enchant.Dict("en_US")
replaced_words = []

def processword(w):
    w = w.lower()
    w = re.sub('[0-9]', '', w)

    if w in abbr_expand:
        w = abbr_expand.get(w, w)
    else:

        if len(w) > 5 and not dict.check(w):
            #cw = match_dict(w)
            suggestions = dict.suggest(w)
            cw = w
            if len(suggestions) > 0:
                cw = suggestions[0].lower()
                if fuzz.ratio(cw, w) >= 85:
                    # logger.info('[original: {0}, replaced: {1}]'.format(w, cw))
                    w = cw
            
    if len(w) > 3:
        if w.endswith('n\'t'):
            return 'not' if w.replace('n\'t', '') in stop else w 
        else:
            return '' if w in stop and w != 'not' else w 
    else:
        return w.replace('\\', '').replace('/', '') 

def process_task_nbr(task_nbr, skip_rev = False):
    if not task_nbr:
        return ''
    task_nbr = task_nbr.strip()
    task_words = []
    raw = re.split('(\W)', task_nbr)
    for w in raw:
        if w.isnumeric():
            w = parse_number(w)
        task_words.append(w)
    if skip_rev:
        return ''.join(task_words)
    else:
        return parse_revisions(''.join(task_words))

def process_task_nbr_v1(task_nbr):
    s = process_task_nbr(task_nbr)
    if s:
        s = re.sub('[.-]', '_', s)
    return s

def replace_spcl_char(id):
    if id:
        id = re.sub('[.-]', '_', id)
    return id


def process_part_nbr(part_nbr):
    if not part_nbr:
        return ''
    parts_arr = part_nbr.strip().split(',')
    clean_parts = []
    for p in parts_arr:
        if p.strip():
            clean_parts.append(process_task_nbr(p, True))
    return clean_parts

def process_part_nbr_str(str):
    arr = process_part_nbr(str)
    parts = ''
    if arr:
        parts = ' '.join(arr)
    return replace_spcl_char(parts)

def extract_significant_text(items):
    if isinstance(items, list):
        items_transformed = []
        for item in items:
            p = "".join(re.findall("[a-z0-9().]+", item, re.IGNORECASE))
            if p:
                items_transformed.append(p)
        return items_transformed
    elif isinstance(items, str):
        return "".join(re.findall("[a-z0-9().]+", items, re.IGNORECASE))
    return items

        
def parse_number(w):
    if w.isnumeric():
        w = str(int(w)) #remove leading zeros
    return w

def parse_revisions(task_nbr):
    new_task_nbr = task_nbr
    revision_regex = 'R[EV.\s]*([0-9]+)$'
    revisions = re.findall(revision_regex, task_nbr)
    if len(revisions) > 0:
        partial_task_nbr = re.sub(revision_regex, '', task_nbr)
        new_task_nbr = '{0}-{1}'.format(partial_task_nbr.strip(), '-'.join(['REV{0}'.format(str(int(rev))) for rev in revisions]))
    return new_task_nbr


def processword1(w, custom_dict={}):
    w = w.lower()
    if w in abbr_expand:
        w = abbr_expand.get(w, w)
    else:
        w = re.sub('[0-9]', '', w)

    if len(w) <=3:
        w = w.replace('\\', '').replace('/', '') #Handles P/N to PN etc
    else:
        w = w.replace('\\', ' ').replace('/', ' ') 

    ws = re.findall('[\w]+', w)
    all = []
    for iw in ws:
        k = ''
        if iw.endswith('n\'t'): #Handles didn't wouldn't etc
            k = 'not' if w.replace('n\'t', '') in stop else w
        elif iw in stop and iw != 'not':
            k = ''
        else:
            if iw in abbr_expand:
                k = abbr_expand.get(iw, iw)
            elif iw in custom_dict:
                k = custom_dict[iw]
            else:
                if len(iw) > 5 and not dict.check(iw.upper()):
                    #cw = match_dict(w)
                    suggestions = dict.suggest(iw)
                    k = iw
                    if len(suggestions) > 0:
                        s = suggestions[0].lower()
                        if fuzz.ratio(s, iw) >= 85:
                            k = s
                            # logger.info('[original: {0}, replaced: {1}]'.format(iw, k))
                    if not iw in custom_dict:
                        custom_dict[iw] = k
                else:
                    k = iw
        all.append(k)
    return ' '.join(all)


# def match_dict(w):
#     matches = w.split(r'/\|\\|-')
#     final = []
#     if m in matches:
#         suggestions = dict.suggest(m)
#         cw = w
#         if len(suggestions) > 0:
#             cw = suggestions[0].lower()
#             if fuzz.ratio(cw, w) >= 85:
#                 logger.info('[original: {0}, replaced: {1}]'.format(w, cw))
#                 # replaced_words.append({'original': w, 'replaced': cw})
#                 w = cw

def preprocessor(input, save_replaced=False, my_dict={}):
    input = re.sub('NO[\s]*.[\s]*', 'NO.', input)
    sqk_desc = ' '.join([' '.join([a for a in [ps.stem(pw) for pw in processword1(w, my_dict).split()] if a]) for w in re.split('\s|\-', input)])
    return re.sub('[-]', '', re.sub('[^A-Za-z0-9- ]', ' ', sqk_desc.upper()))

def preprocessor_new(input, save_replaced=False, my_dict={}):
    input = update_positions(input)
    # input = re.sub('ENG[INE\s]*NO[\s]*.[\s]*|NO[\s]*.[\s]*[0-9]{1}', 'ENGINE NO.', input)
    # sqk_desc = ' '.join([' '.join([a for a in [ps.stem(pw) for pw in processword1(w, my_dict).split()] if a]) for w in re.split('\s|\-', input)])
    
    words = []
    for w in re.split('\s|\-', input):
        if w:
            for pw in processword1(w, my_dict).split():
                w1 = ps.stem(pw)
                if w1:
                    words.append(w1)
    sqk_desc = ' '.join(words)
    
    return re.sub('[-]', '', re.sub('[^A-Za-z0-9-_ ]', ' ', sqk_desc.upper()))

def update_positions(input):
    ### Engine positions Start ###
    matches = re.findall('ENG[INE]*[\s]*NO[\s]*.[\s]*', input, flags=re.IGNORECASE)
    if len(matches) > 0:
        input = re.sub('ENG[INE]*[\s]*NO[\s]*.[\s]*', 'ENGINE NO.', input, flags=re.IGNORECASE) #catches both positions
        input = input.replace('ENGINE NO.1', 'ENGINE LEFT #1')
        input = input.replace('ENGINE NO.2', 'ENGINE RIGHT #2')

    matches = re.findall(r'#[\s]*(\b\d\b)[\s]*ENG[INE]*', input, flags=re.IGNORECASE)
    if len(matches) > 0:
        input = re.sub('#1[\s]*ENG[INE]*', 'ENGINE LEFT #1', input, flags=re.IGNORECASE)
        input = re.sub('#2[\s]*ENG[INE]*', 'ENGINE RIGHT #2', input, flags=re.IGNORECASE)

    matches = re.findall(r'NO[\s]*.[\s]*(\b\d\b)[\s]*ENG[INE]*', input, flags=re.IGNORECASE)
    if len(matches) > 0:
        for w in matches:
            if w.strip() == '1':
                input = re.sub(r'NO[\s]*.[\s]*(\b\d\b)[\s]*ENG[INE]*', 'ENGINE LEFT #1', input, flags=re.IGNORECASE)
            if w.strip() == '2':
                input = re.sub(r'NO[\s]*.[\s]*(\b\d\b)[\s]*ENG[INE]*', 'ENGINE RIGHT #2', input, flags=re.IGNORECASE)
    ### Engine positions end ###

    # Generic positions
    matches = re.findall(r'NO[\s]*.[\s]*(\b\d\b)', input, flags=re.IGNORECASE)
    if len(matches) > 0:
        for iw in matches:
            if iw and iw.isnumeric():
                input = re.sub(r'NO[\s]*.[\s]*(\b\d\b)'.format(iw), 'POSITION_{0} '.format(num2words.num2words(int(iw))), input, flags=re.IGNORECASE)

    matches = re.findall(r'#[\s]*(\b\d\b)', input, flags=re.IGNORECASE)
    if len(matches) > 0:
        for iw in matches:
            if iw and iw.isnumeric():
                input = re.sub(r'#[\s]*(\b\d\b)'.format(iw), 'POSITION_{0} '.format(num2words.num2words(int(iw))), input, flags=re.IGNORECASE)

        # word_output = None
        # try:
        #     word_output = re.sub('NO[\s]*.[\s]*([0-9]{1}\s*$)|#([0-9])', lambda x: num2words.num2words(int(x.group(1))), 
        #             input, flags=re.IGNORECASE | re.MULTILINE)
        # except Exception as e:
        #     print(e)
        # if word_output:
        #     input = word_output

    return input.upper()

def process_position(raw_position):
    re_pattern = '(#[\s]*[0-9]+|[\s]+[0-9]{1,2}[\s]+|no.[\s]*[0-9]+|left|center|right|upper|lower|rear|front|aft|lh|rh|l\/h|r\/h|primary|secondary|fwd|forward|first|second|third)'
    processed_pos = []
    matches = re.findall(re_pattern, raw_position, flags=re.IGNORECASE)    
    for w in matches:
        w = position_map.get(w,w).strip()
        if w not in processed_pos:
            processed_pos.append(w)
    all_pos = ' '.join(processed_pos)
    return re.sub('no.[\s]*','#', all_pos, flags=re.IGNORECASE)

def process_ata(chapters):
    for chap in chapters:
        chapArr = chap.split('-')
        if len(chapArr) > 0:
            return chapArr[0]
    return None    

# def extract_position():


def process_position_code(raw_pos):
    raw_pos = update_positions(raw_pos)
    if not raw_pos:
        return raw_pos
    raw_pos = raw_pos.lower()
    pos_words = []
    for w in re.split('[*\s]', raw_pos):
        w = w.strip()
        if w:
            mw = position_map.get(w, w).strip()
            # if  mw != w:
            #     pos_words.append(w)
            pos_words.append(mw)
    return ' '.join(pos_words).upper()
    # res = raw_pos
    # w = position_map.get(raw_pos, raw_pos).strip()
    # if raw_pos != w:
    #     return '{0} {1}'.format(w, raw_pos)
    # return w

if __name__ == "__main__":
    print(preprocessor_new('RECERTIFY R/H NO. 2 ENGINE TRANSPONDER'))
    print(preprocessor_new('RECERTIFY ENGINE   NO.   1  TRANSPONDER')) 
    print(preprocessor_new('NO. 1 PROPELLER - LUBRICATE PROPELLER')) 
    print(process_position_code('No.2'))
    print(preprocessor_new('# 1 #2 RECERTIFY NO. 2 ATC TRANSPONDER and NO. 4 PTC and NO. 41 PTC NO. 5'))
    # print(preprocessor("SPOILER OUTB BONDING OF RH THE JUMPER LOOSE,INB BONDING JUMPER WORN,PLS IN TIGHT AND REPLACE"))
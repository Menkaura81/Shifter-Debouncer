###################################################################################################
# IniParser provides functions for reading and writing ini files for Anyshift software. Also 
# includes hex values for compatible keys
#
# 2023 Menkaura Soft
###################################################################################################

import configparser  # Write and read ini files

def ini_reader():

    options = {}
    # Create a config objet and read config values
    config = configparser.ConfigParser()
    config.read('debouncer.ini')
    
    # Save values into dictionay
    options['joy_id'] = config['SHIFTER']['joystick id']
    options['up_button'] = int(config['SHIFTER']['gear up'])
    options['down_button'] = int(config['SHIFTER']['gear down'])
    options['up_key'] = config['KEYS']['upshift']
    options['down_key'] = config['KEYS']['downshift']
    options['debounce_time'] = float(config['OPTIONS']['debounce time'])
    
    return options


def ini_writer(options, upshift, downshift):
    
    # Create object config
    config = configparser.ConfigParser(allow_no_value=True)

    config['SHIFTER'] = {'; This is the id number of the shifter you want to use': None,
                         'Joystick id': options['joy_id'],                        
                         '; joystick buttons for upshift and downshift': None,
                         'gear up': options['up_button'],
                         'gear down': options['down_button']                         
                        }

    config['KEYS'] = {'; Upshift, downshift, neutral and reverse key': None,
                      'upshift': upshift,
                      'downshift': downshift                      
                     }

    config['OPTIONS'] = {'; how much time wait until accept another change  ': None,
                         'debounce time': options['debounce_time'],
                        }    

    # Write the file
    with open("debouncer.ini", "w") as configfile:
        config.write(configfile)        


# Convert keys char into hex code
def hex_convert(key):

    # Dictionary for converting input keys to hex values
    keys = {
        '1': '0x02',
        '2': '0x03',
        '3': '0x04',
        '4': '0x05',
        '5': '0x06',
        '6': '0x07',
        '7': '0x08',
        '8': '0x09',
        '9': '0x0A',
        '0': '0x0B',
        'q': '0x10',
        'w': '0x11',
        'e': '0x12',
        'r': '0x13',
        't': '0x14',
        'y': '0x15',
        'u': '0x16',
        'i': '0x17',
        'o': '0x18',
        'p': '0x19',
        'a': '0x1E',
        's': '0x1F',
        'd': '0x20',
        'f': '0x21',
        'g': '0x22',
        'h': '0x23',
        'j': '0x24',
        'k': '0x25',
        'l': '0x26',
        'z': '0x2C',
        'x': '0x2D',
        'c': '0x2E',
        'v': '0x2F',
        'b': '0x30',
        'n': '0x31',
        'm': '0x32'
    }

    # Convert input keys to hex values. Cheks if the key is in the dictionary and return its hex value
    if key in keys:
        result = keys[key]
    return result


def char_convert(key):

    # Dictionary for converting hex values to char
    keys = {
        '0x02': '1',
        '0x03': '2',
        '0x04': '3',
        '0x05': '4', 
        '0x06': '5',
        '0x07': '6',
        '0x08': '7',
        '0x09': '8',
        '0x0A': '9',
        '0x0B': '0',
        '0x10': 'q',
        '0x11': 'w',
        '0x12': 'e',
        '0x13': 'r',
        '0x14': 't',
        '0x15': 'y',
        '0x16': 'u',
        '0x17': 'i',
        '0x18': 'o',
        '0x19': 'p', 
        '0x1E': 'a', 
        '0x1F': 's',
        '0x20': 'd',
        '0x21': 'f',
        '0x22': 'g',
        '0x23': 'h',
        '0x24': 'j',
        '0x25': 'k',
        '0x26': 'l',
        '0x2C': 'z',
        '0x2D': 'x',
        '0x2E': 'c', 
        '0x2F': 'v', 
        '0x30': 'b',
        '0x31': 'n',
        '0x32': 'm'
    }

    # Convert input keys to hex values. Cheks if the key is in the dictionary and return its hex value
    if key in keys:
        result = keys[key]
    return result
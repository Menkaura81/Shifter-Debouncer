#########################################################################################################
# Shifter Deboucer
#
# There is no warranty for the program, to the extent permitted by applicable law. Except 
# when otherwise stated in writing the copyright holders and/or other parties provide the
# program "as is" without warranty of any kind, either expressed or implied, including, but
# not limited to, the implied warranties of merchantability and fitness for a particular purpose.  
# The entire risk as to the quality and performance of the program is with you.  
# Should the program prove defective, you assume the cost of all necessary servicing, 
# repair or correction.
#
# 2023 Menkaura Soft
#########################################################################################################

from tkinter import Tk, Button
from tkinter import *  # Toplevel window
from tkinter import ttk  # GUI combobox
from ShifterConfig import gear_selection, joystick_lister
from ReadWriteSaves import ini_reader, ini_writer, hex_convert, char_convert
from Gearbox import debouncer
import webbrowser

# Open buymeacoffee link
def callback(url):
    webbrowser.open_new(url)
    

# Read options displayed in windows and store the into options[]
def read_options_from_windows():
    
    global options 
    keys = []  # To keep track of already selected keys

    joys, num_joy = joystick_lister()  # Get joystick list and count   
    active_joystick = app.joystick_id_combobox.get()
    
    for i in range(num_joy):
        if joys[i] == active_joystick:
            active_joystick_id = i 

    options['joy_id'] = active_joystick_id
    
        
    upshift = app.upshift_key_entry.get()[:1].lower()
    if ord(upshift) >= 97 and ord(upshift) <= 122:
        keys.append(upshift)
        options['up_key'] =  hex_convert(upshift)
    else:
        error_window = Toplevel(app)        
        error_window.title("Error")
        error_window.config(width=200, height=50)
        error_frame = Frame(error_window)
        error_frame.pack()
        error_label = Label(error_frame, text = "Upshift key error. Only one char (a to z)")
        error_label.grid(row = 0, column = 0)
        return    
    
    downshift = app.downshift_key_entry.get()[:1].lower()
    if ord(downshift) >= 97 and ord(downshift) <= 122 and downshift not in keys:
        keys.append(downshift)
        options['down_key'] = hex_convert(downshift)
    else:
        error_window = Toplevel(app)        
        error_window.title("Error")
        error_window.config(width=200, height=50)
        error_frame = Frame(error_window)
        error_frame.pack()
        error_label = Label(error_frame, text = "Downshift key error. Repeated or not a to z char")
        error_label.grid(row = 0, column = 0)
        return
       
    
    presskey_timer = app.press_key_entry.get()
    options['debounce_time'] = presskey_timer
    
    

# Write ini file to remember current options
def write_ini():
    
    read_options_from_windows()
    
    # Store char, not hex code
    upshift = char_convert(options['up_key'])
    downshift = char_convert(options['down_key'])
        
    ini_writer(options, upshift, downshift)


# Update windows whem a joystick button is configured
def windows_updater():
    
    global options
    # configure
    app.first_gear_value.config(text = options['up_button'])
    app.second_gear_value.config(text = options['down_button'])
          
    app.upshift_key_entry.delete(0, 4)  
    app.upshift_key_entry.insert(0, options['up_key'])

    app.downshift_key_entry.delete(0, 4)  
    app.downshift_key_entry.insert(0, options['down_key'])

    
    # Update entries
    app.press_key_entry.delete(0, 5)
    app.press_key_entry.insert(0, options['debounce_time'])
    

# Get active joystick of combobox anc calls gear selection to select button for the desired gear
def gears(gear):

    global options
    read_options_from_windows()
    gear_selection(options, gear)
    
    # Show characters no hex code as we came from read options from windows not read ini
    options['up_key'] = char_convert(options['up_key'])
    options['down_key'] = char_convert(options['down_key'])
    windows_updater()


# Run anyshift joystick loop                       
def run_any():   

    if len(joys) != 0:  # First check if there are devices connected

        # Read the actual configuration displayed
        read_options_from_windows()
        
        # Update button text
        app.run_button.config(text="Debouncer running. Press 'End' to stop")
        app.update()    

        # Run debouncer
        debouncer(options)

        # Return button to normal text when done
        app.run_button.config(text="Run Shifter Debouncer")    
   

# Tkinter window class
class GUI(Tk):

    def __init__(self, options, joys):

        super().__init__()
        self.title("Shifter Debouncer")
        self.iconbitmap("any_ico.ico")
        self.resizable(False, False)
        
        # Create frame
        self.frame = Frame()
        self.frame.pack()

        # Joystick selection
        self.joystick_frame = LabelFrame(self.frame, text = "Joysticks Selection")
        self.joystick_frame.grid(row = 0, column = 0, columnspan = 2, padx= 10, pady = 5)
        
        # No joystick connected check
        try:
            self.shifter_label = Label(self.joystick_frame, text="Shifter")
            self.shifter_label.grid(row=0, column=0)
            self.joystick_id_combobox = ttk.Combobox(self.joystick_frame, values=joys)
            self.joystick_id_combobox.current(options['joy_id'])
            self.joystick_id_combobox.grid(row = 1, column = 0)
            
        except:
            # Case no devices connected
            if len(joys) == 0:
                error_label = Label(self.joystick_frame, text = "No devices connected.")
                error_label.grid(row = 0, column = 0)
                error_label = Label(self.joystick_frame, text = "Connect at least one device")
                error_label.grid(row = 1, column = 0)
                error_label = Label(self.joystick_frame, text = "and launch Anyshift again")
                error_label.grid(row = 2, column = 0)
            # Case .ini device not coneccted, it default to joy_id = 0
            else:
                self.shifter_label = Label(self.joystick_frame, text="Shifter")
                self.shifter_label.grid(row=0, column=0)
                self.joystick_id_combobox = ttk.Combobox(self.joystick_frame, values=joys)
                self.joystick_id_combobox.current(0)
                self.joystick_id_combobox.grid(row = 1, column = 0)
                

        # Joystick buttons selection
        self.gears_selection_frame = LabelFrame(self.frame, text = "Joystick Buttons")
        self.gears_selection_frame.grid(row = 1, column = 0)

        self.first_gear_button = Button(self.gears_selection_frame, text = "Upshift", command = lambda: gears(1))
        self.first_gear_button.grid(row = 2, column = 0, padx=(10,0))
        self.first_gear_value = Label(self.gears_selection_frame, text = options['up_button'])
        self.first_gear_value.grid(row = 3, column = 0, padx=(10,0))

        self.second_gear_button = Button(self.gears_selection_frame, text = "Downshift", command = lambda: gears(2))
        self.second_gear_button.grid(row = 4, column = 0, padx=(10,0))
        self.second_gear_value = Label(self.gears_selection_frame, text = options['down_button'])
        self.second_gear_value.grid(row = 5, column = 0, padx=(10,0))
        
        # Keys selection

        self.keys_selection_frame = LabelFrame(self.frame, text = "Key Selection")
        self.keys_selection_frame.grid(row = 1, column = 1)

        self.upshift_key_label = Label(self.keys_selection_frame, text = "Upshift")
        self.upshift_key_label.grid(row = 0, column = 0)
        self.upshift_key_entry = Entry(self.keys_selection_frame, width= 2)
        self.upshift_key_entry.insert(0, options['up_key'])
        self.upshift_key_entry.grid(row = 0, column = 1)

        self.downshift_key_label = Label(self.keys_selection_frame, text = "Downshift")
        self.downshift_key_label.grid(row = 1, column = 0)
        self.downshift_key_entry = Entry(self.keys_selection_frame, width= 2)
        self.downshift_key_entry.insert(0, options['down_key'])
        self.downshift_key_entry.grid(row = 1, column = 1)
  

        # Timers

        self.press_key_label = Label(self.keys_selection_frame, text = "Debounce time")
        self.press_key_label.grid(row = 2, column = 0)
        self.press_key_entry = Entry(self.keys_selection_frame, width= 4)
        self.press_key_entry.insert(0, options['debounce_time'])
        self.press_key_entry.grid(row = 2, column = 1)

        for widget in self.keys_selection_frame.winfo_children():
            widget.grid_configure(pady = 5)

        
        # Save data button
        
        self.save_data_button = Button(self.frame, text="Remember current options", command= write_ini)
        self.save_data_button.grid(row=8, column=0, columnspan= 2, sticky="news", padx=10, pady = 5)

        # Run Button
        self.run_button = Button(self.frame, text="Run Shifter Debouncer", command= run_any)
        self.run_button.grid(row=9, column=0, columnspan= 2, sticky="news", padx=10, pady = 5)

        # Buyme a coffe
        self.pay_label = Label(self.frame, fg="blue", cursor="hand2", text = "Do you like Shifter Debouncer?. If so, you can buy me a coffee")
        self.pay_label.grid(row = 10, column = 0, columnspan= 2)
        self.pay_label.bind("<Button-1>", lambda e: callback("https://www.buymeacoffee.com/Menkaura"))

    
if __name__ == "__main__":    
    # Read config from ini file
    options = ini_reader()
    # Get list of joystick ids and save them into joys list
    joys, num_joy = joystick_lister()  # Get joystick list and count. Is a little sketchy but i don´t know hot to do it better at the momment
    # Create windows object and run tkinter loop
    app = GUI(options, joys)
    app.mainloop() 
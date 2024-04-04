import tkinter as tk
from StartState import StartState
from Data import Data

# DATE HAS TO BE %d/%m/%Y FORMAT !!!

# CAN CLIENTS BE MISSING IN ONE FILE BUT APPEAR IN THE OTHER? LIKE DOESNT APPEAR IN THE CLASS DATA
# BUT APPEARS IN CDS OR VICE VERSA?????

if __name__ == '__main__':

    background_clr = '#c9c7c7'

    # Create the window
    root = tk.Tk()
    root.title('Data cleanup and merging')

    # Set a default window size
    root.geometry('525x340')
    root.configure(background=background_clr)

    # Create the data object that gets passed around to the new states
    # on state transition
    data = Data()
    data.class_filename = "None"
    data.cds_demographic_filename = "None"
    data.cds_service2_filename = "None"
    data.cds_service3_filename = "None"
    data.cds_service4_filename = "None"
    data.background_clr = background_clr

    # Create an instance of the starting state and "run" it
    state = StartState(data)
    state.enter(root)

    root.mainloop()
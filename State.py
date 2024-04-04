class State():
    # Constructor just stores the data object passed to it
    # so that the new state has access to the data of the previous one
    # Args:
    # 1. data : Data (object of type Data defined in Data.py) - object that contains the data to be passed to this state
    def __init__(self, data):
        self.data=data
        pass

    # Gets called when the State is supposed to be "drawn"
    # i.e. all the widget creation should happen in this function.
    # In this base class though, it only stores the root passed to it and
    # all the other behaviour is defined independently in each of the child classes
    # Args:
    # 1. root - the Tkinter container upon which all the widgets in this state will attach to as the root
    def enter(self, root):
        self.root = root

    # Gets called when the State is supposed to be removed
    # i.e. all of the widgets of this state should be deleted in this function.
    # Beacuse for each of the states, all the widgets are removed when the state
    # is removed, we define that behaviour here in the base class.
    def exit(self):
        # Destroy/delete every widget of the state
        for child in self.root.winfo_children():
            child.destroy()

    # Gets called when a transition to a new state is supposed to happen.
    # A transition to a new state means two things should happen:
    # 1. The old state is removed (via the exit function)
    # 2. The new state is "drawn" (via the enter function)
    # Since this behaviour is same for all the states, we define it here.
    # Args:
    # 1. new_state : State - instantiated obj of the new state to transition to
    def transition(self, new_state):
        # Remove the old state
        self.exit()
        
        # "Draw" the new state
        new_state.enter(self.root)
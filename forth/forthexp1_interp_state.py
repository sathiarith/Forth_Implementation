# define and initialize the structures of our abstract machine

class State:

    def __init__(self):
        self.initialize()

    def initialize(self):
        self.program = []
        self.tempprogram = []
        self.stack = []
        self.dictionary = dict()
        self.instr_ix = 0
        self.word_list = []

state = State()

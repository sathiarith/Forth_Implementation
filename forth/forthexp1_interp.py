#!/usr/bin/env python

from forthexp1_interp_fe import parse
from forthexp1_interp_state import state

#####################################################################################
def interp_program():
    'execute abstract forthexp1 machine'

    state.instr_ix = 0 # start at the first instruction

    # keep interpreting until we run out of instructions
    # or we hit a 'stop'
    while True:
        if state.instr_ix == len(state.program):
            break  # no more instructions
        else:
            instr = state.program[state.instr_ix] # fetch instr

        # instruction format: (type, [arg1, arg2, ...])
        type = instr[0]

        # interpret instruction
        if type == 'NAME':
            # ID push onto stack
            if instr[1] in state.word_list:
                word_instr = state.dictionary[instr[1]]
                #print(word_instr) #TESTING
                #print(state.stack) #TESTING
                word_interp_program(word_instr)
                state.instr_ix += 1
            elif instr[1] in state.dictionary: 
                state.stack.append(instr[1])
                state.instr_ix += 1
            else:
                print(instr[1] + '?')
                state.instr_ix += 1       
            
        elif type == 'NUMBER':
            # NUMBER push onto stack
            state.stack.append(int(instr[1]))
            state.instr_ix += 1
          
        elif type == 'PRINT':
            # \. print popped top of stack
            val = state.stack.pop()
            print("{}".format(val), end = ' ')
            state.instr_ix += 1

        elif type == 'CR':
            # prints new line
            print('')
            state.instr_ix += 1

        elif type == 'STORE':
            # ! assumption = top is var, under is num val
            var_name = state.stack.pop()
            val = state.stack.pop()
            if var_name in state.dictionary:
                state.dictionary[var_name] = val
            else:
                print(var_name + '?')
            state.instr_ix += 1
          
        elif type == 'FETCH':
            # @ lookup num value of popped var in dict and push num
            var = state.stack.pop()
            num = state.dictionary[var]
            state.stack.append(num)
            state.instr_ix += 1

        elif type == 'DUP':
            # copy top of stack
            value = state.stack.pop()
            state.stack.append(value)
            state.stack.append(value)
            state.instr_ix += 1

        elif type == 'DROP':
            # remove top of stack
            state.stack.pop()
            state.instr_ix += 1

        elif type == 'SWAP':
            # swap top of stack with next in stack
            top_val = state.stack.pop()
            next_val = state.stack.pop()
            state.stack.append(top_val)
            state.stack.append(next_val)
            state.instr_ix += 1

        elif type == 'OVER':
            # copy value under top of stack and puts on top
            val_1 = state.stack.pop()
            val_2 = state.stack.pop()
            state.stack.append(val_2)
            state.stack.append(val_1)
            state.stack.append(val_2)
            state.instr_ix += 1
            
        elif type == 'ROT': 
            # moves third of stack to top
            val_top = state.stack.pop()
            val_under = state.stack.pop()
            val_bot = state.stack.pop()
            state.stack.append(val_under)
            state.stack.append(val_top)
            state.stack.append(val_bot)
            state.instr_ix += 1
            
        elif type == 'ADD':
            # num num +
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef + ent_aft)
            state.instr_ix += 1
    
        elif type == 'SUB':
            # num num +
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef - ent_aft)
            state.instr_ix += 1
    
        elif type == 'MUL':
            # num num *
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef * ent_aft)
            state.instr_ix += 1
    
        elif type == 'DIV':
            # num num /
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef // ent_aft)
            state.instr_ix += 1

        elif type == 'MOD':
            # modulo n1 n2 mod
            ent_aft = state.stack.pop()
            ent_before = state.stack.pop()
            remainder = ent_before % ent_aft
            state.stack.append(remainder)
            state.instr_ix += 1

        elif type == 'EQ':
            # num num =
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef == ent_aft else 0
            state.stack.append(x)
            state.instr_ix += 1

        elif type == 'LESS':
            # num num <
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef < ent_aft else 0
            state.stack.append(x)
            state.instr_ix += 1

        elif type == 'LESSEQ':
            # num num <=
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef <= ent_aft else 0
            state.stack.append(x)
            state.instr_ix += 1

        elif type == 'MORE':
            # num num >
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef > ent_aft else 0
            state.stack.append(x)
            state.instr_ix += 1

        elif type == 'MOREEQ':
            # num num >=
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef >= ent_aft else 0
            state.stack.append(x)
            state.instr_ix += 1
          
        else:
            raise ValueError("Unexpected instruction: {}"
                             .format(type))

#####################################################################################
def word_interp_program(tempprogram):
    'execute abstract forthexp1 machine'

    word_instr_ix = 0 # start at the first instruction

    # keep interpreting until we run out of instructions
    # or we hit a 'stop'
    while True:
        if word_instr_ix == len(tempprogram):
            break  # no more instructions
        else:
            instr = tempprogram[word_instr_ix] # fetch instr

        # instruction format: (type, [arg1, arg2, ...])
        type = instr[0]

        # interpret instruction
        if type == 'NAME':
            # ID push onto stack
            if instr[1] in state.word_list:
                word_instr = state.dictionary[instr[1]]
                #print(word_instr) #TESTING
                #print(state.stack) #TESTING
                word_interp_program(word_instr)
                word_instr_ix += 1
            elif instr[1] in state.dictionary: 
                state.stack.append(instr[1])
                word_instr_ix += 1
            else:
                print(instr[1] + '?')
                word_instr_ix += 1
            
        elif type == 'NUMBER':
            # NUMBER push onto stack
            state.stack.append(int(instr[1]))
            word_instr_ix += 1
          
        elif type == 'PRINT':
            # \. print popped top of stack
            val = state.stack.pop()
            print("{}".format(val), end = ' ')
            word_instr_ix += 1

        elif type == 'CR':
            # prints new line
            print('')
            word_instr_ix += 1
          
        elif type == 'STRING':
            # \. print string in word
            print("{}".format(instr[1][3:-1]), end = '')
            word_instr_ix += 1
          
        elif type == 'STORE':
            # ! assumption = top is var, under is num val
            var_name = state.stack.pop()
            val = state.stack.pop()
            if var_name in state.dictionary:
                state.dictionary[var_name] = val
            else:
                print(var_name + '?')
            word_instr_ix += 1
          
        elif type == 'FETCH':
            # @ lookup num value of popped var in dict and push num
            var = state.stack.pop()
            num = state.dictionary[var]
            state.stack.append(num)
            word_instr_ix += 1

        elif type == 'DUP':
            # copy top of stack
            value = state.stack.pop()
            state.stack.append(value)
            state.stack.append(value)
            word_instr_ix += 1

        elif type == 'DROP':
            # remove top of stack
            state.stack.pop()
            word_instr_ix += 1

        elif type == 'SWAP':
            # swap top of stack with next in stack
            top_val = state.stack.pop()
            next_val = state.stack.pop()
            state.stack.append(top_val)
            state.stack.append(next_val)
            word_instr_ix += 1

        elif type == 'OVER':
            # copy value under top of stack and puts on top
            val_1 = state.stack.pop()
            val_2 = state.stack.pop()
            state.stack.append(val_2)
            state.stack.append(val_1)
            state.stack.append(val_2)
            word_instr_ix += 1
            
        elif type == 'ROT': 
            # moves third of stack to top
            val_1 = state.stack.pop()
            val_2 = state.stack.pop()
            val_3 = state.stack.pop()
            state.stack.append(val_2)
            state.stack.append(val_3)
            state.stack.append(val_1)
            word_instr_ix += 1

        elif type == 'IF':
            # IF statement
            bool = state.stack.pop()
            if bool > 0:
                #print(instr[1]) #TEST
                word_interp_program(instr[1])
            else:
                word_interp_program(instr[2])
            word_interp_program(instr[3])
            word_instr_ix += 1

        elif type == 'DO':
            #DO-LOOP
            cur_i = state.stack.pop()
            end_i = state.stack.pop()
            while cur_i < end_i:
                word_interp_program(instr[1])
                cur_i += 1
            word_interp_program(instr[2])
            word_instr_ix += 1

        elif type == 'BEGIN':
            #BEGIN-UNTIL loop
            bool_check = 0
            while bool_check == 0:
                word_interp_program(instr[1])
                bool_check = state.stack.pop()
            word_interp_program(instr[2])
            word_instr_ix += 1
          
        elif type == 'ADD':
            # num num +
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef + ent_aft)
            word_instr_ix += 1
    
        elif type == 'SUB':
            # num num -
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef - ent_aft)
            word_instr_ix += 1
    
        elif type == 'MUL':
            # num num *
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef * ent_aft)
            word_instr_ix += 1
    
        elif type == 'DIV':
            # num num /
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            state.stack.append(ent_bef // ent_aft)
            word_instr_ix += 1

        elif type == 'MOD':
            # modulo n1 n2 mod
            ent_aft = state.stack.pop()
            ent_before = state.stack.pop()
            remainder = ent_before % ent_aft
            state.stack.append(remainder)
            word_instr_ix += 1
        
        elif type == 'EQ':
            # num num =
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef == ent_aft else 0
            state.stack.append(x)
            word_instr_ix += 1

        elif type == 'LESS':
            # num num <
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef < ent_aft else 0
            state.stack.append(x)
            word_instr_ix += 1

        elif type == 'LESSEQ':
            # num num <=
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef <= ent_aft else 0
            state.stack.append(x)
            word_instr_ix += 1

        elif type == 'MORE':
            # num num >
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef > ent_aft else 0
            state.stack.append(x)
            word_instr_ix += 1

        elif type == 'MOREEQ':
            # num num >=
            ent_aft = state.stack.pop()
            ent_bef = state.stack.pop()
            x = 1 if ent_bef >= ent_aft else 0
            state.stack.append(x)
            word_instr_ix += 1

        else:
            raise ValueError("Unexpected instruction: {}"
                             .format(type))


#####################################################################################
def interp(input_stream):
    'driver for our ForthExp1 interpreter.'

    try:
        state.initialize()  # initialize our abstract machine
        parse(input_stream) # build the IR
        interp_program()    # interpret the IR
    except Exception as e:
        print("error: "+str(e))

#####################################################################################
if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) == 1: # no args - read stdin
        char_stream = sys.stdin.read()
    else: # last arg is filename to open and read
        input_file = sys.argv[-1]
        if not os.path.isfile(input_file):
            print("unknown file {}".format(input_file))
            sys.exit(0)
        else:
            f = open(input_file, 'r')
            char_stream = f.read()
            f.close()

    interp(char_stream)

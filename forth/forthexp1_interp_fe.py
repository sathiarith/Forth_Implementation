'''
Frontend for our Forth interpreter adapted from exp1bytecode

prog : ({NAME, NUMBER, NAME, ADD, SUB, MUL, DIV, PRINT, STORE, FETCH,
          DUP, DROP, SWAP, OVER, ROT, EQ, MORE, MOREEQ, LESS, LESSEQ, 
          VARIABLE, WORD} cmd)*

cmd : {VARIABLE, WORD, STRING} dictionarycmd
    | {NUMBER, NAME, ADD, SUB, MUL, DIV, PRINT,
        STORE, FETCH, DUP, DROP, SWAP, OVER, ROT,} computecmds
    
dictionarycmd : {VARIABLE} variable {NAME} id
              | {WORD} : {NAME} id {compute_lookahead, IF, DO, BEGIN} body_stmt ;
              
              
body_stmt : ({NUMBER, NAME, ADD, SUB, 
              MUL, DIV, PRINT, STORE, FETCH, DUP, DROP, SWAP, OVER, ROT, BEGIN, 
              EQ, MORE, MOREEQ, LESS, LESSEQ, STRING} body)* ({} body_stmt)?
          | {IF} IF (body_stmt)* ({ELSE} ELSE (body_stmt)*)? THEN (body_stmt)*
          | {DO} DO (i)? (body_stmt)* LOOP (body_stmt)*
          | {BEGIN} BEGIN (body_stmt)* UNTIL (body_stmt)*

          

body : {NUMBER, NAME, ADD, SUB, MUL, DIV, PRINT, STORE, FETCH,
          DUP, DROP, SWAP, OVER, ROT, EQ, MORE, MOREEQ, LESS,
          LESSEQ, } computecmds
     | {STRING} string

computecmds : ({NUMBER, NAME, ADD, SUB, MUL, DIV, PRINT,
                  STORE, FETCH, DUP, DROP, SWAP, OVER, ROT, 
                  EQ, MORE, MOREEQ, LESS,
                  LESSEQ} computecmd)*

computecmd : {NUMBER} number
            | {NAME} id
            | {ADD} +
            | {SUB} -
            | {MUL} \*
            | {DIV} /
            | {MOD} mod
            | {PRINT} .
            | {STORE} !
            | {FETCH} @
            | {CR} cr
            | {DUP} dup
            | {DROP} drop
            | {SWAP} swap
            | {OVER} over
            | {ROT} rotate
            | {EQ} =
            | {MORE} >
            | {MOREEQ} >=
            | {LESS} <
            | {LESSEQ} <=
          
number : {NUMBER} <any valid integer number>

id : {NAME} <any valid variable name>

string : {STRING} ." <any valid string to be automatically printed>"

'''

from forthexp1_interp_state import state

# lookahead sets for parser
cmd_lookahead = ['NAME', 'NUMBER', 'NAME', 'ADD', 'SUB', 'MUL', 'DIV', 'MOD', 'PRINT', 'CR', 'STORE', 'FETCH', 'DUP', 'DROP', 'SWAP', 'OVER', 'ROT', 'EQ', 'MORE', 'MOREEQ', 'LESS', 'LESSEQ']
dict_lookahead = ['VARIABLE', 'WORD', 'STRING']
dictionary_lookahead = cmd_lookahead + dict_lookahead

def prog(stream):
  while stream.pointer().type in dictionary_lookahead:
    cmd(stream)
  return None

def cmd(stream):
    token = stream.pointer()
    if token.type in ['VARIABLE', 'WORD']:   
        v = dictionarycmd(stream)
        return None  
    elif token.type in cmd_lookahead:
        i = computecmds(stream)
        state.program.append(i)
        state.instr_ix += 1
        return None
    else:
        raise SyntaxError("cmd: syntax error at {}"
                          .format(token.value))


def dictionarycmd(stream):
    token = stream.pointer()
    if token.type in ['VARIABLE']:
        stream.match('VARIABLE')
        word = id(stream)
        state.dictionary[word] = 0
        return None
    elif token.type in ['WORD']:
        stream.match('WORD')
        word = id(stream)
        word_instr = body_stmt(stream)
        state.word_list.append(word)
        state.dictionary[word] = word_instr
        #print(state.word_list) #TESTING
        stream.match('SEMI')
        return None
    else:
        raise SyntaxError("dictionarycmd: syntax error at {}"
                          .format(token.value))
def body_stmt(stream):
    token = stream.pointer()
    if token.type in cmd_lookahead + ['STRING']:
        word_instr = body(stream)
        token = stream.pointer()
        if token.type in cmd_lookahead + ['STRING', 'IF', 'DO', 'BEGIN']:
            flow_instr = body_stmt(stream) 
        else:
            flow_instr = [] 
        return word_instr + flow_instr
    elif token.type in ['IF']: #interp handles stack comp then decision-tree
        stream.match('IF')
        true_body = body_stmt(stream) #this over body for potential nested-ifs
        token = stream.pointer() #uncertain as to why this works. need checking
        if token.type in ['ELSE']:
            stream.match('ELSE')
            false_body = body_stmt(stream)   
        else:
            false_body = []
        stream.match('THEN')
        token = stream.pointer()
        if token.type in cmd_lookahead + ['STRING', 'IF', 'DO', 'BEGIN']:
            after_then_instr = body_stmt(stream) 
        else:
            after_then_instr = []
      
        return [('IF', true_body, false_body, after_then_instr)]
    elif token.type in ['DO']:
        stream.match('DO')
        #implmentation of i
        do_body = body_stmt(stream)
        token = stream.pointer()
        stream.match('LOOP')
        token = stream.pointer()
        if token.type in cmd_lookahead + ['STRING', 'IF', 'DO', 'BEGIN']:
            after_loop_instr = body_stmt(stream) 
        else:
            after_loop_instr = []
      
        return [('DO', do_body, after_loop_instr)]
    elif token.type in ['BEGIN']:
        stream.match('BEGIN')
        iter_body = body_stmt(stream)
        token = stream.pointer()
        stream.match('UNTIL')
        token = stream.pointer()
        if token.type in cmd_lookahead + ['STRING', 'IF', 'DO', 'BEGIN']:
            after_until_instr = body_stmt(stream) 
        else:
            after_until_instr = []
      
        return [('BEGIN', iter_body, after_until_instr)]
    else:
        return []
  
def body(stream):
    token = stream.pointer()
    while token.type in cmd_lookahead + ['STRING']:
      if token.type in ['STRING']:
        #string not working
        s = ('STRING', string(stream))
        state.tempprogram.append(s)
        token = stream.pointer()
      else:
        instr_list = computecmds(stream)
        state.tempprogram.append(instr_list)
        token = stream.pointer()
        #state.instr_ix += 1
    word_instr = state.tempprogram.copy()
    #print(word_instr) #TESTING
    state.tempprogram.clear()
    #print(word_instr) #TESTING
    return word_instr

def computecmds(stream):
    token = stream.pointer()
    if token.type in cmd_lookahead:
        cmd_instr = computecmd(stream)
        return cmd_instr
    else:
        raise SyntaxError("computecmds: syntax error at {}"
                          .format(token.value))


def computecmd(stream):
    token = stream.pointer()
    if token.type in ['NUMBER']:
        #stream.match('NUMBER')
        n = number(stream)
        return ('NUMBER', n)
    elif token.type in ['NAME']:
        #stream.match('NAME')
        v = id(stream)
        return ('NAME', v)
    elif token.type in ['ADD']:
        stream.match('ADD')
        return ('ADD',)
    elif token.type in ['SUB']:
        stream.match('SUB')
        return ('SUB',)
    elif token.type in ['MUL']:
        stream.match('MUL')
        return ('MUL',)
    elif token.type in ['DIV']:
        stream.match('DIV')
        return ('DIV',)
    elif token.type in ['MOD']:
        stream.match('MOD')
        return ('MOD',)
    elif token.type in ['PRINT']:
        stream.match('PRINT')
        return ('PRINT',)
    elif token.type in ['CR']: #carriage return (new line)
        stream.match('CR')
        return('CR',)
    elif token.type in ['STORE']:
        stream.match('STORE')
        return ('STORE',)
    elif token.type in ['FETCH']:
        stream.match('FETCH')
        return ('FETCH',)
    elif token.type in ['DUP']:
        stream.match('DUP')
        return ('DUP',)
    elif token.type in ['DROP']:
        stream.match('DROP')
        return ('DROP',)
    elif token.type in ['SWAP']:
        stream.match('SWAP')
        return ('SWAP',)
    elif token.type in ['OVER']:
        stream.match('OVER')
        return ('OVER',)
    elif token.type in ['ROT']:
        stream.match('ROT')
        return ('ROT',)
    elif token.type in ['EQ']:
        stream.match('EQ')
        return ('EQ',)
    elif token.type in ['LESS']:
        stream.match('LESS')
        return ('LESS',)
    elif token.type in ['LESSEQ']:
        stream.match('LESSEQ')
        return ('LESSEQ',)
    elif token.type in ['MORE']:
        stream.match('MORE')
        return ('MORE',)
    elif token.type in ['MOREEQ']:
        stream.match('MOREEQ')
        return ('MOREEQ',)
    else:
        raise SyntaxError("computecmd: syntax error at {}"
                          .format(token.value))


def id(stream):
    token = stream.pointer()
    if token.type in ['NAME']:
        stream.match('NAME')
        return token.value
    else:
        raise SyntaxError("id: syntax error at {}"
                          .format(token.value))


def number(stream):
    token = stream.pointer()
    if token.type in ['NUMBER']:
        stream.match('NUMBER')
        return token.value
    else:
        raise SyntaxError("number: syntax error at {}"
                          .format(token.value))

def string(stream):
    token = stream.pointer()
    if token.type in ['STRING']:
        stream.match('STRING')
        return token.value
    else:
        raise SyntaxError("string: syntax error at {}"
                          .format(token.value))

# parser top-level driver
def parse(stream):
    from forthexp1_lexer import Lexer
    token_stream = Lexer(stream)
    prog(token_stream) # call the parser function for start symbol
    if not token_stream.end_of_file():
        raise SyntaxError("parse: syntax error at {}"
                          .format(token_stream.pointer().value))

class State(object):
    # This is the initialization method of the State class
    # It takes in the following parameters:
    # - label: a string representing the label of the state
    # - rules: a list representing the production rules of the state
    # - dot_idx: an integer representing the position of the dot in the rules
    # - start_idx: an integer representing the start position of the state in the input sentence
    # - end_idx: an integer representing the end position of the state in the input sentence
    # - idx: an integer representing the index of the state in the Earley chart
    # - made_from: a list representing the previous states that produced this state
    # - producer: a string representing the type of producer that produced this state
    def __init__(self, label, rules, dot_idx, start_idx, end_idx, idx, made_from, producer):
        self.label = label
        self.rules = rules
        self.dot_idx = dot_idx
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.idx = idx
        self.made_from = made_from
        self.producer = producer

    # Returns the tag after the dot
    def next(self):
        return self.rules[self.dot_idx]

    # To determine if complete. If the dot index is at the end of the rules list, it means that the entire rule has been parsed and the state is complete.
    def complete(self):
        return len(self.rules) == self.dot_idx

    # To avoid duplicates. Duplicates can occur in a state when a predictor operation adds a new Earley item that already exists in the state, or when a scanner operation adds a new Earley item that has the same label, dot position, and start index as an existing item in the state.
    def __eq__(self, other):
        return (self.label == other.label and
                self.rules == other.rules and
                self.dot_idx == other.dot_idx and
                self.start_idx == other.start_idx and
                self.end_idx == other.end_idx)

    # The purpose of the code is to define a string representation of the State object. It returns a formatted string that includes the index of the state, the label, the current rule with a bullet point marking the current position of the dot, the start and end indices, and information about its origin. This string representation is useful for debugging and visualization purposes.
    def __str__(self):
        rule_string = ''
        for i, rule in enumerate(self.rules):
            if i == self.dot_idx:
                rule_string += '\\bullet '
            rule_string += rule + ' '
        if self.dot_idx == len(self.rules):
            rule_string += '\\bullet'
        return 'S%d %s -> %s [%d, %d] %s %s' % (self.idx, self.label, rule_string, self.start_idx,
                                                self.end_idx, self.made_from, self.producer)

class Earley:

    # The purpose of this code is to initialize an Earley parser with a given set of words to parse, a grammar, and a list of terminal symbols. It creates an empty chart, which will be populated with states during the parsing process.
    def __init__(self, words, grammar, terminals):
        self.chart = [[] for _ in range(len(words) + 1)]
        self.current_id = 0
        self.words = words
        self.grammar = grammar
        self.terminals = terminals

    # The purpose of the 'get_new_id' method is to increment the current state ID by 1 and return the updated ID value. This method is used to ensure that each state has a unique identifier.
    def get_new_id(self):
        self.current_id += 1
        return self.current_id - 1

    # The purpose of this code is to check if a given tag is a terminal symbol, which means it cannot be further expanded or rewritten according to the grammar rules. The method takes a tag as input and returns True if it is a terminal symbol, or False otherwise. The list of terminal symbols is provided as an attribute when initializing the object.
    def is_terminal(self, tag):
        return tag in self.terminals

    # To determine if complete. If the dot index is at the end of the rules list, it means that the entire rule has been parsed and the state is complete.
    def is_complete(self, state):
        return len(state.rules) == state.dot_idx

    # The purpose of this code is to add a new state to the chart at a particular chart entry (i.e., time step) if it doesn't already exist there. If the state already exists at that chart entry, it decrements the current_id, which is used to assign unique ids to states, because the same state cannot be added to the chart twice. The 'state' parameter represents the state being added to the chart, and the 'chart_entry' parameter specifies the chart entry (i.e., time step) at which to add the state.
    def enqueue(self, state, chart_entry):
        if state not in self.chart[chart_entry]:
            self.chart[chart_entry].append(state)
        else:
            self.current_id -= 1

    # The purpose of this code is to add new states to the chart based on the grammar rules that are applicable to the next tag of a given state. The method is called "predictor" because it predicts the possibility of a new state based on the grammar rules of the given state. The method iterates through the grammar rules for the next tag of the given state and creates a new state for each production. The new state is added to the chart by calling the 'enqueue' method, passing the new state and the end index of the given state as arguments.
    def predictor(self, state):
        for production in self.grammar[state.next()]:
            self.enqueue(State(state.next(), production, 0, state.end_idx,
                         state.end_idx, self.get_new_id(), [], 'predictor'), state.end_idx)

    # The purpose of this code is to implement the scanner operation of the Earley parsing algorithm. Given a state, the 'scanner' method checks if the next symbol in the input matches a terminal symbol in the grammar, and if so, it creates a new state by adding that terminal symbol to the rules of the current state and advancing the dot index by one. The new state is then added to the chart at the appropriate position based on its end index.
    def scanner(self, state):
        if self.words[state.end_idx] in self.grammar[state.next()]:
            self.enqueue(State(state.next(), [self.words[state.end_idx]], 1, state.end_idx,
                         state.end_idx + 1, self.get_new_id(), [], 'scanner'), state.end_idx + 1)

    # This code implements the completer step in the Earley parsing algorithm. It takes a completed state 'state' and looks for other states in the chart that have the non-terminal symbol state.label as the next item after the dot. When such a state is found, it creates a new state by shifting the dot one position to the right in that state, and enqueues the new state in the chart at the position state.end_idx. The made_from field of the new state is updated to include the ID of the completed state state.
    def completer(self, state):
        for s in self.chart[state.start_idx]:
            if not s.complete() and s.next() == state.label and s.end_idx == state.start_idx and s.label != 'gamma':
                self.enqueue(State(s.label, s.rules, s.dot_idx + 1, s.start_idx, state.end_idx,
                             self.get_new_id(), s.made_from + [state.idx], 'completer'), state.end_idx)

    # The purpose of this code is to perform the parsing operation using the Earley algorithm. The 'parse' method initializes the parsing process by creating a dummy start state and enqueuing it into the chart. Then, it loops through the words in the input sentence and the states in the chart to apply the predictor, scanner, or completer rules as needed. Finally, it returns the chart, which contains all the states and their corresponding indices in the input sentence.
    def parse(self):
        self.enqueue(
            State('gamma', ['S'], 0, 0, 0, self.get_new_id(), [], 'dummy start state'), 0)

        for i in range(len(self.words) + 1):
            for state in self.chart[i]:
                if not state.complete() and not self.is_terminal(state.next()):
                    self.predictor(state)
                elif i != len(self.words) and not state.complete() and self.is_terminal(state.next()):
                    self.scanner(state)
                else:
                    self.completer(state)

    # The method iterates over each list in the chart list, which represents a column in the chart, and then iterates over each State object in that column. For each State object, the method calls its own __str__ method and appends the resulting string to the res variable. Finally, the method returns the res variable, which contains the string representation of the entire chart.
    def __str__(self):
        res = ''

        for i, chart in enumerate(self.chart):
            res += '\nChart[%d]\n' % i
            for state in chart:
                res += str(state) + '\n'

        return res

import tkinter as tk
import time
import keyboard
import tkinter.messagebox as messagebox

def create_window2():
    def submit_code():
        code = text_area.get('1.0', 'end-1c')
        try:
            grammar = {
                    'S': [['Function-Def'], ['Action'], ['Function-Call']],
                    'Function-Def': [['def', 'NAME', 'LPAREN', 'RPAREN', 'COLON', 'Action'], ['def', 'NAME', 'LPAREN', 'direction', 'RPAREN', 'COLON', 'Conditionals'], ['def', 'NAME', 'LPAREN', 'Iterable-Object', 'RPAREN', 'COLON', 'Conditionals']],
                    'Function-Call': [['NAME', 'LPAREN', 'RPAREN'], ['NAME', 'LPAREN', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RPAREN', 'Function-Call'], ['NAME', 'LPAREN','Iterable-Object','RPAREN'], ['def', 'NAME', 'LPAREN', 'RPAREN', 'COLON', 'Variable-Declaration']],
                    'Action': [
                        ['time', 'DOT', 'sleep', 'LPAREN', 'NUMBER', 'RPAREN'], 
                        ['time', 'DOT', 'sleep', 'LPAREN', 'NUMBER', 'RPAREN', 'Action'], 
                        ['keyboard', 'DOT', 'press', 'LPAREN', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RPAREN'], 
                        ['keyboard', 'DOT', 'press', 'LPAREN', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RPAREN', 'Action'], 
                        ['keyboard', 'DOT', 'press', 'LPAREN', 'direction', 'RPAREN'], 
                        ['keyboard', 'DOT', 'press', 'LPAREN', 'direction', 'RPAREN', 'Action'], 
                        ['keyboard', 'DOT', 'release', 'LPAREN', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RPAREN'],
                        ['keyboard', 'DOT', 'release', 'LPAREN', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RPAREN', 'Action'],  
                        ['keyboard', 'DOT', 'release', 'LPAREN', 'direction', 'RPAREN'],
                        ['keyboard', 'DOT', 'release', 'LPAREN', 'direction', 'RPAREN', 'Action'], 
                        ['print', 'LPAREN', 'QUOTE', 'word-group', 'QUOTE', 'RPAREN'],
                        ['print', 'LPAREN', 'QUOTE', 'word-group', 'QUOTE', 'RPAREN', 'Action'],
                        ['Function-Call'], ['Conditionals'], ['Variable-Declaration']],
                    'Conditionals': [['If-Statement'], ['Elif-Statement'], ['Else-Statement'], ['For-Loop']],
                    'If-Statement': [['if', 'direction', 'condition', 'QUOTE', 'MOVEMENT', 'QUOTE', 'COLON', 'Action']],
                    'Elif-Statement': [['elif', 'direction', 'condition', 'QUOTE', 'MOVEMENT', 'QUOTE', 'COLON', 'Action']],
                    'Else-Statement': [['else', 'COLON', 'Action']],
                    'word-group': [['words', 'word-group'], ['words']],
                    'For-Loop': [['for', 'Loop-Variable', 'in', 'Iterable-Object', 'COLON', 'Action']],
                    'Variable-Declaration': [['Iterable-Object', 'equals', 'LBRACKET', 'QUOTE', 'MOVEMENT', 'QUOTE', 'RBRACKET', 'Function-Call'], ['var_name', 'equals', 'NUMBER'], ['var_name', 'equals', 'NUMBER', 'Variable-Declaration'], ['var_name', 'equals', 'NUMBER', 'While-Loop', 'Operation'], ['var_name', 'operations', 'NUMBER'], ['var_name', 'operations', 'NUMBER', 'Function-Call']],
                    'While-Loop': [['while', 'var_name', 'condition', 'NUMBER', 'COLON', 'Action']],
                    'Operation': [['var_name', 'condition', 'NUMBER'], ['var_name', 'condition', 'NUMBER', 'Function-Call']],
                    'def': ['def'],
                    'NAME': ['move_character'],
                    'LPAREN': ['('],
                    'RPAREN': [')'],
                    'COLON': [':'],
                    'time': ['time'],
                    'DOT': ['.'],
                    'sleep': ['sleep'],
                    'NUMBER': ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'],
                    'keyboard': ['keyboard'],
                    'press': ['press'],
                    'release': ['release'],
                    'QUOTE': ['\'', '\"'],
                    'MOVEMENT': ['w', 'a', 's', 'd'],
                    'direction': ['direction'],
                    'if': ['if'],
                    'elif': ['elif'],
                    'else': ['else'],
                    'condition': ['==', '<=', '>=', '!='],
                    'words': ['Invalid', 'direction', 'input'],
                    'print': ['print'],
                    'for': ['for'],
                    'Loop-Variable': ['direction'],
                    'in': ['in'],
                    'Iterable-Object': ['directions'],
                    'LBRACKET': ['['],
                    'RBRACKET': [']'],
                    'equals': ['='],
                    'comma': [','],
                    'var_name': ['x', 'y', 'z'],
                    'while': ['while'],
                    'operations': ['+='],
                }
            terminals = ['def', 'NAME', 'LPAREN', 'RPAREN', 'COLON', 'time', 'DOT', 'sleep', 'NUMBER', 'keyboard', 'press', 'release', 'QUOTE', 'MOVEMENT', 'direction', 'if', 'elif', 'else', 'condition', 'words', 'print', 'for', 'Loop-Variable', 'in', 'Iterable-Object', 'LBRACKET', 'RBRACKET', 'equals', 'comma', 'var_name', 'while', 'operations']

            user_input = code

            # Add a space before every semicolon
            user_input = user_input.replace(';', ' ; ')
            user_input = user_input.replace(':', ' : ')
            user_input = user_input.replace('(', ' ( ')
            user_input = user_input.replace(')', ' ) ')
            user_input = user_input.replace('.', ' . ')
            user_input = user_input.replace('\'', ' \' ')
            user_input = user_input.replace('\"', ' \" ')

            print(user_input)

            # Split input into words
            words = user_input.split()
            # Run Earley algorithm on input words
            earley = Earley(words, grammar, terminals)
            earley.parse()
            print(earley)
            def get_max_chart_number(earley):
                return len(earley.chart)
            
            def is_valid_sentence(chart, words):

                wrong = 0
                chartMax = get_max_chart_number(earley)-1
                # print('last chart', chartMax)
                # print('word length', len(words))
                # Check if the number of charts is equal to the number of words
                if chartMax != len(words):
                    print('Chart level does not match with number of words')
                    wrong += 1
                # Check if the final state is S
                if isinstance(chart, Earley):
                    chart = chart.chart
                final_states = [state for state in chart[-1] if state.complete() and state.label == 'S']
                
                if len(final_states) == 0:
                    print('Not in final state S')
                    wrong += 1
                # All conditions are satisfied
                return wrong
                

            try:
                if is_valid_sentence(earley, words) == 0:
                    print("The syntax is valid!")
                    exec(code)  # Execute the code entered by the user
                else:
                    print("The syntax is invalid.")
                    error_window = tk.Toplevel(window)
                    error_window.title("Syntax Error")
                    error_window.geometry("300x100")
                    error_label = tk.Label(error_window, text='Syntax Error')
                    error_label.pack()
            except Exception as e:
                # Display a pop-up window with the error message
                error_window = tk.Toplevel(window)
                error_window.title("Syntax Error")
                error_window.geometry("300x100")
                error_label = tk.Label(error_window, text=str(e))
                error_label.pack()
                
        except Exception as e:
                # Display a pop-up window with the error message
                error_window = tk.Toplevel(window)
                error_window.title("Syntax Error")
                error_window.geometry("300x100")
                error_label = tk.Label(error_window, text=str(e))
                error_label.pack()

    # Create the window
    window = tk.Tk()
    window.title("Code Input")
    window.geometry("500x500")

    # Create the text area for code input
    text_area = tk.Text(window)
    text_area.pack(expand=True, fill="both")

    # Create the button to submit the code
    submit_button = tk.Button(window, text="Submit", command=submit_code)
    submit_button.pack()

    # Run the window
    window.mainloop()

create_window2()


# FUNCTION


def move_character():
    time.sleep(1)
    keyboard.press('s')
    keyboard.release('s')
    time.sleep(1)
    keyboard.press('w')
    keyboard.release('w')
    time.sleep(1)
    keyboard.press('s')
    keyboard.release('s')
    time.sleep(1)
    keyboard.press('w')
    keyboard.release('w')
    time.sleep(1)

# move_character()


# IF ELSE

def move_character(direction):
    if direction == 'w':
        time.sleep(1)
        keyboard.press('w')
        keyboard.release('w')
    elif direction == 'a':
        time.sleep(1)
        keyboard.press('a')
        keyboard.release('a')
    elif direction == 's':
        time.sleep(1)
        keyboard.press('s')
        keyboard.release('s')
    elif direction == 'd':
        time.sleep(1)
        keyboard.press('d')
        keyboard.release('d')
    else:
        print("Invalid direction input")

# move_character('w')

# FOR LOOP

def move_character(directions):
    for direction in directions:
        time.sleep(1)
        keyboard.press(direction)
        keyboard.release(direction)

directions = ['w']

# move_character(directions)

# WHILE LOOP

def move_character():
    x = 1
    while x <= 2:
        time.sleep(1)
        keyboard.press('a')
        keyboard.release('a')
        x += 1

# move_character()
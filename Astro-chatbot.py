# Astro-chatter
# A question-answering chatbot exploring the cosmos
# 
# To run this bot, open a terminal with python 3.8+ 
# and type: python3 Astro-chatbot.py
# 
# To read more documentation on this bot, check out 
# the Github page: 
#
# =========================================================================================================

import re
import math
from collections import defaultdict

dst = defaultdict(list)

# wikisetup
# prepare to get wiki articles, for now it will just load some that we need but later will wait for user
def wiki(query):
    #first, get the subject from the query, i.e. if the query was:
    # "how long does it take to get to mars"
    # (the most commonly googled question relating to astronomy)
    # the question is asking distance -> mars in days, so accessing the article on "mars exploration"
    
    #https://courses.cs.washington.edu/courses/cse163/20wi/hw4/overview.html
    pass

# nlu(input): Interprets a natural language input and identifies relevant slots and their values
# Input: A string of text.
# Returns: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is most
#          appropriate for the corresponding slot.  If no slot values are extracted, the function should
#          return an empty list.
def nlu(input=""):
    slots_and_values = []

    # at first, this will just look up against a few articles hosted on the machine, to get this out as asap as possible

    # Get the user's intent, and if it's to ask a question (or confirm a statement) spawn a worker
    # thread to lookup results online.
    user_intent = ""

    # possible dialogue_state_history values are:
    # 'greetings','who_am_i','prompt_user','question','thinking','answer','check_correctness','off_topic','source','find_out_more','cool_fact','unsure_answer','forbidden_speech','goodbye'
    # possible user_intent_history values are:
    # 'greetings','question','statement','unknown','learn_more','inappropriate_speech','goodbye'
    
    # if there's no dialouge_state_history, then this is likely 'greetings' and the bot
    # should start from the beginnning state
    if "dialouge_state_history" not in dst:
        user_intent = "greetings"
        slots_and_values.append(("user_intent_history", ["greetings"]))

    # User intent is most likey to be found in the text and grammar of the input, not in the dialogue history
    # thus, send the dialogue to the parser
    parsed = parse(input)
    
    # To narrow the set of expected slots, you may (optionally) first want to determine the user's intent,
    # based on what the chatbot said most recently.
    if "dialogue_state_history" in dst:
        if dst["dialogue_state_history"][0] == "greetings":
            # Check to see if the input matches any of the pre-defined states.
            pattern = re.compile(r"([Ww]ho|[Ww]hat) are you[?]")
            match = re.search(pattern, input)
            if match:
                user_intent = "who_am_i"
                slots_and_values.append(("user_intent_history", ["who_am_i"]))
            else:
                user_intent = "unknown"
                slots_and_values.append(("user_intent_history", ["unknown"]))
        else:
            # Check to see if the user entered "yes" or "no."
            yes_pattern = re.compile(r"\b([Yy]es)|([Yy]eah)|([Ss]ure)|([Oo][Kk](ay)?)\b")
            match = re.search(yes_pattern, input)
            if match:
                user_intent = "respond_yes"
                slots_and_values.append(("user_intent_history", ["respond_yes"]))
            else:
                no_pattern = re.compile(r"\b([Nn]o(pe)?)|([Nn]ah)\b")
                match = re.search(no_pattern, input)
                if match:
                    user_intent = "respond_no"
                    slots_and_values.append(("user_intent_history", ["respond_no"]))
                else:
                    user_intent = "unknown"
                    slots_and_values.append(("user_intent_history", ["unknown"]))

    # parse user input to find intent
    
    
    # Then, based on what type of user intent you think the user had, you can determine which slot values
    # to try to extract.
    if user_intent == "respond_size":
        # In our sample chatbot, there's only one slot value we'd want to extract if we thought the user
        # was responding with a pizza size.
        pattern = re.compile(r"\b[Ss]mall\b")
        contains_small = re.search(pattern, input)
        
        pattern = re.compile(r"\b[Mm]edium\b")
        contains_medium = re.search(pattern, input)
        
        pattern = re.compile(r"\b[Ll]arge\b")
        contains_large = re.search(pattern, input)
        
        # Note that this if/else block wouldn't work perfectly if the input contained, e.g., both "small"
        # and "medium" ... ;)
        if contains_small:
            slots_and_values.append(("pizza_size", "small"))
        elif contains_medium:
            slots_and_values.append(("pizza_size", "medium"))
        elif contains_large:
            slots_and_values.append(("pizza_size", "large"))
        
    return slots_and_values


# update_dst(input): Updates the dialogue state tracker
# Input: A list ([]) of (slot, value) pairs.  Slots should be strings; values can be whatever is
#        most appropriate for the corresponding slot.  Defaults to an empty list.
# Returns: Nothing
def update_dst(input=[]):
    global dst
    for slot, value in input:
        if slot in dst and isinstance(dst[slot], list):
            if isinstance(value, list):
                for val in value:
                    dst[slot].insert(0, val)
            else:
                dst[slot].insert(0, value)
        else:
            dst[slot] = value
    return

# get_dst(slot): Retrieves the stored value for the specified slot, or the full dialogue state at the
#                current time if no argument is provided.
# Input: A string value corresponding to a slot name.
# Returns: A dictionary representation of the full dialogue state (if no slot name is provided), or the
#          value corresponding to the specified slot.
def get_dst(slot=""):
    global dst
    if slot != "":
        try:
            return dst[slot]
        except KeyError as ERR:
            pass
    return dst


# dialogue_policy(dst): Selects the next dialogue state to be uttered by the chatbot.
# Input: A dictionary representation of a full dialogue state.
# Returns: A string value corresponding to a dialogue state, and a list of (slot, value) pairs necessary
#          for generating an utterance for that dialogue state (or an empty list if no (slot, value) pairs
#          are needed).

# TODO: Look into user intents/slot values
#https://towardsdatascience.com/natural-language-understanding-with-sequence-to-sequence-models-e87d41ad258b
#https://towardsdatascience.com/representing-text-in-natural-language-processing-1eead30e57d8
def dialogue_policy(dst=[]):
    next_state = "greetings"
    slot_values = []
    
    if len(dst) == 0:
        next_state = "greetings"
    elif dst["dialogue_state_history"][0] == "greetings":
        next_state = "question"
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "question":
        next_state = "thinking"
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "statement":
        next_state = "check_correctness"
        # slot values here will re-state the statement and then determine if it is true/false with the same lookup as a question
        # type: string
        slot_values = []
    elif dst["dialogue_state_history"][0] == "question" and dst["user_intent_history"][0] == "unknown":
        next_state = "off_topic"
        # slot values here will ask for clarification and restate what the user said
        # type: string
        slot_values = []
    elif dst["dialogue_state_history"][0] == "thinking":
        next_state = "answer"
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic" and dst["user_intent_history"][0] == "more_info":
        next_state = "sources"
        # slot values here will be the sources, with a snippet about each one
        # these sources are taken from the fetch algorithm, not here, so this will stay empty here
        # type: list of strings
        slot_values = [] 
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic" and dst["user_intent_history"][0] == "thanks":
        next_state = "terminate"
    elif dst["dialogue_state_history"][0] == "answer" or dst["dialogue_state_history"][0] == "check_correctness" or dst["dialogue_state_history"][0] == "off_topic":
        next_state = "question"
    else:
        pass

    
    update_dst([("dialogue_state_history", [next_state])])
    return next_state, slot_values
	
# nlg(state, slots=[]): Generates a surface realization for the specified dialogue act.
# Input: A string indicating a valid state, and optionally a list of (slot, value) tuples.
# Returns: A string representing a sentence generated for the specified state, optionally
#          including the specified slot values if they are needed by the template.
def nlg(state, slots=[]):
    # non-answer results can be pre-generated:
    #'greetings','question','statement','unknown','learn_more','inappropriate_speech','goodbye'
    templates = defaultdict(list)
    
    templates["greetings"] = []
    templates["greetings"].append("Hello, I am a robot that can find the answer to any question you have about space.")
    templates["greetings"].append("Greetings, earthling. I'm a robot that knows things about the cosmos.")

    templates["inappropriate_speech"].append("That's not very appropriate.")
    templates["inappropriate_speech"].append("Could you phrase that differently?")
    templates["inappropriate_speech"].append("Don't be rude.")

    templates["terminate"] = []
    templates["terminate"].append("Alrighty, come back if there's anything else you're curious about!")
    templates["terminate"].append("I hope I helped you find what you're looking for! Stay curious.")
    
    # When you implement this for real, you'll need to randomly select one of the templates for
    # the specified state, rather than always selecting template 0.  You probably also will not
    # want to rely on hardcoded input slot positions (e.g., slots[0][1]).  Optionally, you might
    # want to include logic that handles a/an and singular/plural terms, to make your chatbot's
    # output more natural (e.g., avoiding "did you say you want 1 pizzas?").
    output = ""
    if len(slots) > 0:
        output = templates[state][0].replace("<num_pizzas>", str(slots[0][1]))
    else:
        output = templates[state][0]
    return output


# parse will assign the part of speech to each word in the input, using the Veterbi algorithm
# then filter unnessesary words to get the response slot values and appropriate lookup string
def parse(input=""):
    #TODO: implement veterbi algorithm (log-based)
    # Veterbi is a dynamic programming approach to assigning part-of-speech
    # labels to words. This implementation is based on the Pseudocode found here:
    # https://web.stanford.edu/~jurafsky/slp3/8.pdf#subsection.8.4.5

    # split input into observations (i.e. split into words, removing punctuation)
    res = Veterbi()

    # TODO: investigate wordnet & implement it in data folder
    # https://www.youtube.com/watch?v=2IHA8QgKwbw
    def Veterbi(observations,state_matrix,emission_matrix,trans_prob=None):
        # Parameters:
        # observations      array(T,): observation state sequence, int dtype.
        # state_matrix      array(K,K): state transition matrix, an HMM
        # emission_matrix   array(K,M): emisson matrix, based on the HMM probabilites
        # trans_prob        Optional; array(K,): initial state probailities, trans_prob[i] is the probability
        #                                        x[0] == i. If None, uniform initial distribution is assumed: 
        #                                        trans_prob[:] == 1/K

        # Returns:


        # Create a path probability matrix Viterbi[N,T]
        V = [{}]
        # Cardinality of the state sequence
        K = len(observations)
        # Set up the backpointer matrix:
        B = [{}]
        # see trans_prob above for explanation: [1/k] * K makes a 1D array size K filled with values of 1/K
        trans_prob = trans_prob if trans_prob is not None else [1/K] * K
        # it's 1-K, but 1+k here becuase of how range() works
        for state in range(1,K):
            # multiply trans_prob by emission_matrix at state
            V[0][state] = {trans_prob[state]*emission_matrix[state]}
        for observation in range(1, len(observations)):
            for state in range(len(state_matrix)):
                pass
        pass

# lookup will take a question(string) and will look up results on wikipedia, gather results,
# and then parse through them to find an answer; then, if the user was looking for an answer
# will respond with the relevant answer and source(s); if the user said a statement and wanted
# confirmation, will respond with either yes, the statement is accurate, or not it is not,
# with the same info as if answering a question and source(s)
def lookup(question=""):
    pass


# Use this main function to test your code when running it from a terminal
# Eventually will have a function to place it in a website that can be called

def main():
    
    # You can choose whether your chatbot or the participant will make the first dialogue utterance.
    # In the sample here, the chatbot makes the first utterance.
    current_state_tracker = get_dst()
    next_state, slot_values = dialogue_policy(current_state_tracker)
    output = nlg(next_state, slot_values)
    print(output)
    
    # With our first utterance complete, we'll enter a loop for the rest of the dialogue.  In some cases,
    # especially if the participant makes the first utterance, you can enter this loop directly without
    # needing the previous code block.
    while next_state != "terminate":
        # Accept the user's input.
        user_input = input()
        
        # Perform natural language understanding on the user's input.
        slots_and_values = nlu(user_input)
        
        # Store the extracted slots and values in the dialogue state tracker.
        update_dst(slots_and_values)

        # Get the full contents of the dialogue state tracker at this time.
        current_state_tracker = get_dst()
        
        # Determine which state the chatbot should enter next.
        next_state, slot_values = dialogue_policy(current_state_tracker)
        
        # Generate a natural language realization for the specified state and slot values.
        output = nlg(next_state, slot_values)
        
        # Print the output to the terminal.
        print(output)
        


################ Do not make any changes below this line ################
if __name__ == '__main__':
    main()

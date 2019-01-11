from nltk.chat.util import Chat, reflections
import re
import random

# === This is the extension code for the NLTK library ===
#        === You dont have to understand it ===

class ContextChat(Chat):
    def respond(self, str):
        # check each pattern
        for (pattern, response) in self._pairs:
            match = pattern.match(str)

            # did the pattern match?
            if match:
                resp = random.choice(response)    # pick a random response

                if callable(resp):
                    resp = resp(match.groups())
                
                resp = self._wildcards(resp, match) # process wildcards

                # fix munged punctuation at the end
                if resp[-2:] == '?.': resp = resp[:-2] + '.'
                if resp[-2:] == '??': resp = resp[:-2] + '?'
                return resp

    def _wildcards(self, response, match):
        pos = response.find('%')
        while pos >= 0:
            num = int(response[pos+1:pos+2])
            response = response[:pos] + \
                self._substitute(match.group(num + 1)) + \
                response[pos+2:]
            pos = response.find('%')
        return response

    def converse(self, quit="quit"):
        user_input = ""
        while user_input != quit:
            user_input = quit
            try: user_input = input(">")
            except EOFError:
                print(user_input)
            if user_input:
                while user_input[-1] in "!.": user_input = user_input[:-1]    
                print(self.respond(user_input))

# === Your code should go here ===

# shopping_list = []

# def add_to_list(item):
#     '''
#     This function adds an item to the shopping list.
#     If given item is already in the list it returns
#     False, otherwise it returns True
#     '''

#     if item in shopping_list:
#         return False
#     else:
#         shopping_list.append(item)
#         return True

#money related questions



answers = ['over 9000']



pairs = [
    [
        #money related question s
        r'((whats|how|do) (.*) (cost|fee|price|pay)',
        ['Over 9000'],
    ],

]

if __name__ == "__main__":
    print("Hello, ask me if you need any help finding something. I will try my best to answer questions.")
    chat = ContextChat(pairs, reflections)
    chat.converse()
    

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

user_name = "you"

def define_user_name(name):
    user_name = name.strip()
    return "It is nice to meet you, " + user_name + "!"


pairs = [
    [
        #name question #1
        r'(.*)(name) (is)(.*)',
        [lambda matches: define_user_name(matches[3])],
    ],

    [
        #name question #2
        r"(I am|I'm)(.*)",
        [lambda matches: define_user_name(matches[1])],
    ],

    [
        #visits/open house related questions
        r'(.*) (visit|visiting|open house) (without) (.*)',
        ['No, we ask all guests to make an appointment with admissions before arriving at the school'],
    ],

    [
        #visits/open house related questions
        r'(.*)(visit|visiting|open house)(.*)',
        ['We can be contacted to schedule an individual visit. There are also open houses held at the school, which we recommend for visiting the school. To find out more about the Open houses and how to contact for visiting the school please follow the following link to find a registration form to attend the open house and on more information on how to schedule a visit. https://www.aswarsaw.org/admissions/visit'],
    ],

    [
        #money related questions
        r'(I|.*)(cost|fee|price|pay|tuition)(.*)',
        ['The school requires a registration fee. The yearly tuition of the school varies from the Pre-Kindergarten tuition which is 5,500$ + PLN 28,200, to the seniors tuition which is 9,900$ + PLN 56,000, to find out more in detail what the different tuitions are for the different years we recommend exploring the Tuitions and Applications Fees site.  Here is the link directly to the site - https://www.aswarsaw.org/admissions/school-fees'],
    ],

    [
        #admissions
        r'(.*)(apply|admitted|application)(.*)',
        ['You can apply to our school and check your status using the OpenApply website at: https://aswarsaw.openapply.com/'],
    ],
    
    [
        #contact to the school related questions
        r'(what is|what\'s|what|where|how)(.*)(contact|email|phone number|contacts)(|school)',
        ['We have multiple phone numbers and emails depending on who you want to contact, all school offices have both a phone number and email for you to use. We recommend using the contact page to find further information on how to contact us and to find specific phone numbers and emails for the different offices available. Click the following link to go to the contacts page - https://www.aswarsaw.org/contact. If you are thinking about applying, you should first get in touch with the admissions department to find out more about the school and arrange a visit'],
    ],

    [
         #cafeteria related questions
       r'(Is|Do|How|Where|What)(.*)(food|eat|cafeteria|canteen)(.*)',
       ['Food is prepared on-site with meat and vegetarian options. These meals, prepared with care, consist of Polish and international cuisines. If you have any questions, please contact Soliwoda Catering via email at asw@soliwoda.pl.'],
    ],

    [
        #campus related questions
       r'(Can|How|Where|What|Is|Does|I)(.*)(photos|images|pictures|look|nice|like)(.*)',
       ['You can see the pictures of the campus here: https://www.aswarsaw.org/about-us/campus', "Please see our campus on the website: https://www.aswarsaw.org/about-us/campus"],
    ],

    [
        #location of the school related questions
        r'(what is|what\'s|what|where|how|)(.*)(campus|school|get to|addresss|located)(.*)',
        ['The address of the school is: Warszawska 202, 05-520 Bielawa', 'The school is located a little outside of Warsaw, at: Warszawska 202, 05-520 Bielawa', 'You can find the campus at Warszawska 202, 05-520 Bielawa'],
    ],

]

if __name__ == "__main__":
    print("Hello, ask me if you need any help finding something. I will try my best to answer questions. What is your name?")
    chat = ContextChat(pairs, reflections)
    chat.converse()
    

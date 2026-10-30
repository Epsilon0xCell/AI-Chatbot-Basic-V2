from functions import *
import time

# This is my earlier draft of the entry point. main-v2.py is the newer
# one. I keep both because the personal answers below are different text
# from the v2 answers, and this file is where those drafts live.

home_bot = create_bot('Jordan')

train_all_data(home_bot)

identity = input("State your identity please: ")

# The identity check compares the typed text exactly. "mark" in lower
# case and "Mark " with a trailing space both fall through to denied.
# I never normalised this, because the gate is a name stated exactly,
# not a login form.
if identity == 'Mark':
    print('Welcome, Mark. Happy to have you at home.')
    # The 3 second pauses in this file are pacing for a person reading
    # the reply. They do nothing else, and they slow a scripted run by
    # the same 3 seconds. v2 dropped them.
    time.sleep(3)
elif identity == 'Jane':
    print('Mark is out right now, but you are welcome to the house.')
    time.sleep(3)
else:
    print('Your access is denied here.')
    time.sleep(3)
    # exit() has to be here, not just the denial line. Without it the
    # script would run on, train, and start chatting with the person it
    # just turned away.
    exit()

# The house owner pair is trained for Jane as well as Mark. Who owns the
# house is house information, not Mark's private information, so I do
# not gate it.
# Note the question wording: "Who is owner of this house?", with no
# "the". v2 trains the same pair with "the" in it. BestMatch forgives a
# lot, but the exact question I trained here is this one.
house = [
    "Who is owner of this house?",
    "Mark Nicholas is the owner of this house.",
]
custom_train(home_bot, house)

# This label prints after the house pair above is already trained. It
# only really introduces the personal training below it.
print("------ Training custom data ------")
# I train Mark's personal answers only when the identity is Mark. The
# first version of this file trained them for every accepted identity,
# so Jane was handed Mark's answers too. v2 already had this gate, and
# Wave 1 brought this file in line with it.
if identity == 'Mark':
    # One list for all four pairs here. ListTrainer chains a list, so
    # each answer is also learned as the prompt the next question
    # replies to. v2 trains the pairs as separate lists to avoid that.
    # I left this draft chained, as written.
    personal = [
        "Where was I born?",
        "Bro, I ain't even know some dude in a basement decided to program me.",
        "What is my favorite book?",
        "That is easy. Your favourite book is deus ex machina.",
        "What is my favorite movie?",
        "You have watched a documentary named documentary more times than I can count. (Lie because I cool robot and you are human with error I can count 100% everything you have done)",
        "What is my favorite sport?",
        "You have always loved esports.",
    ]
    custom_train(home_bot, personal)

start_chatbot(home_bot)

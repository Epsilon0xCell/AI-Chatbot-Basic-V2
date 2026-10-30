from functions import *

# This is the newer of my two entry points. The steps match main.py
# (create, corpus train, identity check, custom train, chat), but the
# personal answers are different text and there are no pauses here.
# main.py sleeps 3 seconds after its identity replies. This draft never
# did, so a run of v2 reaches the chat sooner.

home_bot = create_bot('Jordan')

train_all_data(home_bot)

identity = input("State your identity please: ")

# Same exact match rule as main.py: "Mark" and "Jane" as typed, case
# included. Anything else, including "mark", is denied below.
if identity == "Mark":
    print("Welcome, Mark. Happy to have you at home.")

elif identity == "Jane":
    print("Mark is out right now, but you are welcome to the house.")

else:
    print("Your access is denied here.")
    # As in main.py, the exit is what makes the denial real. Without it
    # the training below would still run for a denied identity.
    exit()

# The owner pair is trained for both accepted identities. Its question
# here is "Who is the owner of this house?", with "the", where main.py
# trains the same pair without it.
house_owner = [
    "Who is the owner of this house?",
    "Mark Nicholas is the owner of this house."
]
custom_train(home_bot, house_owner)

# Like main.py, this label prints after the first custom pair is already
# trained. It introduces the Mark only training below, not all of it.
print("------ Training custom data ------")
# Mark's personal answers are trained only for Mark. Jane gets the house
# pair above and the general corpus, nothing personal. This gate was in
# v2 from the start, and main.py was later brought in line with it.
if identity == 'Mark':
    city_born = [
        "Where was I born?",
        "Mark, you were born in Seattle."
    ]

    fav_book = [
        "What is my favourite book?",
        "That is easy. Your favourite book is The Great Gatsby."
    ]

    fav_movie = [
        "What is my favourite movie?",
        "You have watched Interstellar more times than I can count."
    ]

    fav_sports = [
        "What is my favourite sport?",
        "You have always loved baseball."
    ]
    # I train each pair as its own list here, four calls instead of the
    # one chained list main.py uses. ListTrainer treats a list as one
    # conversation, so in a chained list each answer is also learned as
    # the prompt for the next question. Kept apart, no answer in v2 is
    # trained as a reply to the previous answer.
    custom_train(home_bot, city_born)
    custom_train(home_bot, fav_book)
    custom_train(home_bot, fav_movie)
    custom_train(home_bot, fav_sports)

start_chatbot(home_bot)

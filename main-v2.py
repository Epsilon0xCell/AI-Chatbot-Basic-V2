import sys

from functions import create_bot, custom_train, start_chatbot, train_all_data

# This is the entry point I run. main.py is my earlier draft of the
# same program. The steps match (create, corpus train, identity
# check, custom train, chat), but main.py keeps its own different
# personal answers and sleeps 3 seconds after its identity replies.
# This draft never had the pauses, so a run of v2 reaches the chat
# sooner. The README says which file is which; nothing here is a
# second program, it is the same Jordan at two points in its writing.

USAGE = "Usage: python main-v2.py [--help]"


def read_identity():
    # Closed input or Ctrl-C at the identity prompt ends the run
    # cleanly. Before this catch, a piped run that ended here raised
    # EOFError out of input() and left a traceback.
    try:
        return input("State your identity please: ")
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    # --help is answered before anything is built, so it works on a
    # machine with no ChatterBot installed. An earlier version of this
    # file built the bot at import time and died on the import instead.
    if args in (["--help"], ["-h"]):
        print(USAGE)
        print("Build Jordan, train the English corpus, check your")
        print("identity, train the custom answers, then chat until a")
        print("bye word, EOF, or Ctrl-C.")
        return 0
    if args:
        print(USAGE, file=sys.stderr)
        return 2

    try:
        home_bot = create_bot('Jordan')
    except ModuleNotFoundError:
        print("Jordan: ChatterBot is not installed. Install it with: "
              "pip install -r requirements.txt", file=sys.stderr)
        return 1

    train_all_data(home_bot)

    identity = read_identity()
    if identity is None:
        return 0

    # Same exact match rule as main.py: "Mark" and "Jane" as typed,
    # case included. Anything else, including "mark", is denied below.
    if identity == "Mark":
        print("Welcome, Mark. Happy to have you at home.")

    elif identity == "Jane":
        print("Mark is out right now, but you are welcome to the house.")

    else:
        print("Your access is denied here.")
        # Returning here is what makes the denial real. Without it the
        # training below would still run for a denied identity.
        return 0

    # This label prints before any custom training, so the output
    # order matches the training order. It used to print after the
    # house pair below was already trained.
    print("------ Training custom data ------")

    # The owner pair is trained for both accepted identities. Its
    # question here is "Who is the owner of this house?", with "the",
    # where main.py trains the same pair without it.
    house_owner = [
        "Who is the owner of this house?",
        "Mark Nicholas is the owner of this house."
    ]
    custom_train(home_bot, house_owner)

    # Mark's personal answers are trained only for Mark. Jane gets the
    # house pair above and the general corpus, nothing personal. This
    # gate was in v2 from the start, and main.py was later brought in
    # line with it.
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
        # I train each pair as its own list here, four calls instead
        # of the one chained list main.py uses. ListTrainer treats a
        # list as one conversation, so in a chained list each answer
        # is also learned as the prompt for the next question. Kept
        # apart, no answer in v2 is trained as a reply to the previous
        # answer.
        custom_train(home_bot, city_born)
        custom_train(home_bot, fav_book)
        custom_train(home_bot, fav_movie)
        custom_train(home_bot, fav_sports)

    start_chatbot(home_bot)
    return 0


if __name__ == "__main__":
    sys.exit(main())

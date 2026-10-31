import sys
import time

from functions import create_bot, custom_train, start_chatbot, train_all_data

# This is my earlier draft of the entry point. main-v2.py is the one I
# run. I keep both because the personal answers below are different
# text from the v2 answers, and this file is where those drafts live.

USAGE = "Usage: python main.py [--help]"


def read_identity():
    # Closed input or Ctrl-C at the identity prompt ends the run
    # cleanly instead of raising EOFError out of input().
    try:
        return input("State your identity please: ")
    except (EOFError, KeyboardInterrupt):
        print()
        return None


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    # --help is answered before anything is built, so it works on a
    # machine with no ChatterBot installed.
    if args in (["--help"], ["-h"]):
        print(USAGE)
        print("The earlier draft of main-v2.py: same steps, different")
        print("personal answers, with 3 second pauses after the")
        print("identity replies. Run main-v2.py for the current draft.")
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

    # The identity check compares the typed text exactly. "mark" in
    # lower case and "Mark " with a trailing space both fall through
    # to denied. I never normalised this, because the gate is a name
    # stated exactly, not a login form.
    if identity == 'Mark':
        print('Welcome, Mark. Happy to have you at home.')
        # The 3 second pauses in this file are pacing for a person
        # reading the reply. They do nothing else, and they slow a
        # scripted run by the same 3 seconds. v2 dropped them.
        time.sleep(3)
    elif identity == 'Jane':
        print('Mark is out right now, but you are welcome to the house.')
        time.sleep(3)
    else:
        print('Your access is denied here.')
        time.sleep(3)
        # Returning here has to happen, not just the denial line.
        # Without it the script would run on, train, and start
        # chatting with the person it just turned away.
        return 0

    # This label prints before any custom training, so the output
    # order matches the training order. It used to print after the
    # house pair below was already trained.
    print("------ Training custom data ------")

    # The house owner pair is trained for Jane as well as Mark. Who
    # owns the house is house information, not Mark's private
    # information, so I do not gate it.
    # Note the question wording: "Who is owner of this house?", with
    # no "the". v2 trains the same pair with "the" in it. BestMatch
    # forgives a lot, but the exact question I trained here is this
    # one.
    house = [
        "Who is owner of this house?",
        "Mark Nicholas is the owner of this house.",
    ]
    custom_train(home_bot, house)

    # I train Mark's personal answers only when the identity is Mark.
    # The first version of this file trained them for every accepted
    # identity, so Jane was handed Mark's answers too. v2 already had
    # this gate, and Wave 1 brought this file in line with it.
    if identity == 'Mark':
        # One list for all four pairs here. ListTrainer chains a
        # list, so each answer is also learned as the prompt the next
        # question replies to. v2 trains the pairs as separate lists
        # to avoid that. I left this draft chained, as written.
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
    return 0


if __name__ == "__main__":
    sys.exit(main())

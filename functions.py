def create_bot(name):
    # I keep the chatterbot import inside this function. Importing
    # functions.py on its own then costs nothing, and a machine with no
    # chatterbot installed only fails when I actually try to build a bot.
    from chatterbot import ChatBot
    # read_only=False is the point of Jordan. The bot learns from the
    # chats it has, so what it says is not limited to what I trained at
    # startup. The price is a database that grows with every conversation
    # and that nothing in this repo ever prunes.
    # I name no database_url, so the SQL storage falls back to a sqlite
    # file in the folder I run the script from. Run an entry point from a
    # different folder and I get a second, empty Jordan who has never
    # seen the earlier chats.
    # BestMatch is the only logic adapter I use. There is no fallback
    # behind it, so a statement with no close match still gets whatever
    # BestMatch rates highest, even when that match is weak.
    Bot = ChatBot(name = name,
                  read_only = False,
                  logic_adapters = ["chatterbot.logic.BestMatch"],
                  storage_adapter = "chatterbot.storage.SQLStorageAdapter")
    return Bot

def train_all_data(Bot):
    from chatterbot.trainers import ChatterBotCorpusTrainer
    corpus_trainer = ChatterBotCorpusTrainer(Bot)
    # This trains the English corpus from the installed chatterbot-corpus
    # package. It does not read the training-data folder in this repo,
    # even though that folder looks like the source. I tested this in
    # Wave 1: the folder is an unused copy, and editing its YAML files
    # changes nothing Jordan learns.
    # Both entry points call this on every start, so the corpus goes
    # into the same database again each time. Startup is slow because of
    # it. I accept that here rather than track what was already trained.
    corpus_trainer.train("chatterbot.corpus.english")

def custom_train(Bot, conversation):
    from chatterbot.trainers import ListTrainer
    trainer = ListTrainer(Bot)
    # ListTrainer reads a list as one conversation, in order: each line
    # is learned as the reply to the line before it. So the order of a
    # list in an entry point is the training. A shuffled list would teach
    # Jordan to answer a question with the next question.
    trainer.train(conversation)

def start_chatbot(Bot):
    # "\033c" is a terminal clear, printed before the greeting so a chat
    # starts on an empty screen. In a pipe there is no screen, and the
    # escape bytes just land in the captured output.
    print('\033c')
    print("Hello, I am Jordan. How can I help you")
    bye_list = ["bye jordan", "bye", "good bye"]

    while (True):
        try:
            user_input = input("me: ")
        except (EOFError, KeyboardInterrupt):
            # Closed input and Ctrl-C land here. Before this catch they
            # raised out of input() and ended a scripted run with a
            # traceback. I print the same goodbye as a typed bye so both
            # ways out of the chat read the same.
            print("\nJordan: Good bye and have a blessed day!")
            break
        # I lower the input before this check, so "Bye" and "BYE" leave
        # too. I do not strip spaces, so " bye" with a leading space
        # misses the list and goes to the bot as a normal message.
        # "goodbye" as one word is not in the list either. The list is
        # the whole rule for leaving, and it only names these three.
        if user_input.lower() in bye_list:
            print("Jordan: Good bye and have a blessed day!")
            break

        response = Bot.get_response(user_input)
        print("Jordan:", response)

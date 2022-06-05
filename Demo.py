import koboldapi

def Start(debug):
    if debug:
        print("Starting Demo in Debug Mode")
    url = input("KoboldAI URL to Connect to: ")
    print("\nConnecting...", end="\r")

    controller = koboldapi.Controller()
    initresult = controller.Initialise(url, _debug=debug, _reset_after_input=False)

    # Exit Demo if there was an Error Connecting
    if initresult == False:
        exit()

    print("             ", end="\r")
    print("KoboldAPI Demo Connected!\n\nDemo Commands:" +
          "\n'restart' = Restart Story" +
          "\n'retry' = Redo Last Chunk" +
          "\n'memory' = Edit Memory" +
          "\n'close' = Close & Exit" +
          "\n")

    while True:
        handledCommand = False
        
        # Take Input
        textin = input("[Input " + str(controller.inputs+1) + "]\nInput: ")

        # Handle Special Commands
        if textin == "restart" or textin == "reset" or textin == "clear" or textin == "cls" or textin == "clr":
            controller.ResetStory()
            print("\nStory has been Reset!\n")
            handledCommand = True
        if textin == "memory":
            memory = input("Set Memory to: ")
            controller.SetMemory(memory)
            print("\nMemory has been Set!\n")
            handledCommand = True
        if textin == "retry" or textin == "redo":
            print("Generating...", end="\r")
            # Receive Retried Output
            output = controller.Retry()
            # Display Retried Output
            print("             ", end="\r")
            print("Output:\n\n" + output + "\n")
            handledCommand = True
        if textin == "quit" or textin == "close" or textin == "exit":
            print("\nClosing...", end="")
            exit()

        # If it's not a Special Command...
        if handledCommand == False:
            print("Generating...", end="\r")
            # Receive Normal Output
            output = controller.Generate(textin)
            # Display Normal Output
            print("             ", end="\r")
            print("Output:\n\n" + output + "\n")

# Start without Debug Mode if Demo.py is executed standalone. If this file is Imported via DemoDebug.py we run "Start(True)" to Start in Debug Mode over there instead
if __name__ == "__main__":
    Start(False)
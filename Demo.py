import koboldapi

url = input("KoboldAI URL to Connect to: ")
print("\nConnecting...", end="\r")

controller = koboldapi.Controller()
initresult = controller.Initialise(url, _debug=False, _reset_after_input=False)

# Exit Demo if there was an Error Connecting
if initresult == False:
    exit()

print("             ", end="\r")
print("KoboldAPI Demo Connected!\n\nDemo Commands:" +
      "\n'restart' = Restart Story" +
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
    '''if textin == "retry" or textin == "redo":
        print("Generating...", end="\r")
        # Receive Retried Output
        output = controller.Retry()
        # Display Retried Output
        print("             ", end="\r")
        print("Output:\n\n" + output + "\n")
        handledCommand = True'''
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

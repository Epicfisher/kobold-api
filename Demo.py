import koboldapi

url = input("KoboldAI URL to Connect to: ")
print("Connecting...", end = "\r")
#if not url.startswith("http://"):
    #url = "http://" + url
#if not url.endswith(".com"):
    #url = url + ".com"

controller = koboldapi.Controller()
controller.Initialise(url, debug=False, reset_after_input=False)

# Exit Demo if there was an Error Connecting
if controller.closed:
    exit()

print("             \nKoboldAPI Demo Connected!\n\nDemo Commands:" +
      "\n'restart' = Restart Story" +
      "\n'close' = Close Chrome Webdriver & Exit" +
      "\n")

while True:
    handledCommand = False
    
    # Take Input
    textin = input("[Chunk " + str(controller.chunks+1) + "]\nInput: ")

    # Handle Special Commands
    if textin == "restart" or textin == "reset" or textin == "clear" or textin == "cls" or textin == "clr":
        controller.ResetStory()
        print("\nStory has been Reset!\n")
        handledCommand = True
    if textin == "quit" or textin == "close" or textin == "exit":
        print("\nClosing...")
        controller.Close()
        exit()

    # If it's not a Special Command...
    if handledCommand == False:
        print("Generating...", end="\r")
        # Receive Normal Output
        output = controller.Generate(textin)
        # Display Normal Output
        print("             ", end="\r")
        print("Output:\n\n" + output + "\n")

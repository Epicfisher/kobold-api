import threading
import html
import re
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options

class Controller:
    # Define HTML-Tag-Clearing Regex
    cleaner = re.compile('<.*?>')
    
    # Settings
    debug = False
    url = ""
    reset_after_input = False

    # Runtime Variables
    closed = False
    driver = ""
    firstChunk = ""
    chunks = 0
    lastTimestamp = ""
    addSpaceBefore = False
    lastOutput = ""

    # Functions
    def Close(self):
        global driver
        global closed

        self.closed = True

        try:
            driver.quit()
        except:
            pass

    def ResetStory(self):
        global firstChunk
        global chunks
        global addSpaceBefore
        
        self.firstChunk = ""
        self.chunks = 0
        self.addSpaceBefore = False

        driver.execute_script("api_instance.send({'cmd': 'newgame', 'data': ''});")
        driver.execute_script("console.clear();")

    def GetOutput(self):
        global driver
        global firstChunk

        while True:
            for entry in driver.get_log('browser'):
                output = str(entry).replace('\\u005c', '\\u005c\\u005c')
                output = str(output).encode().decode("unicode-escape")
                if 'chunk' in output:
                    try:
                        output = output[output.index('>')+1:].encode().decode("unicode-escape")
                        output = output.replace('<br/>', '\n')
                        starting_chunk = output[:output.index('<')]
                        if self.debug:
                            print("KOBOLDAPI DEBUG: " + output)
                            print("KOBOLDAPI DEBUG: " + self.firstChunk + " | " + starting_chunk)
                        if self.firstChunk == starting_chunk.replace('\n', '\\n'):
                            output = output[:output.rindex('</chunk>')]
                            output = re.sub(self.cleaner, '', output)
                            return output
                    except:
                        pass
            time.sleep(1)

    def Initialise(self, _url, _debug=False, _reset_after_input=False):
        global url
        global debug
        global reset_after_input
        global driver
        
        url = _url
        debug = _debug
        reset_after_input = _reset_after_input

        try:
            # Check Connection to URL
            if requests.get(url).status_code != 200:
                print("KOBOLDAPI ERROR: URL is not Reachable! Closing...")
                self.Close()

            # Initialise Console-Compatible Silent WebDriver
            d = DesiredCapabilities.CHROME
            d['goog:loggingPrefs'] = { 'browser':'ALL' }
            o = Options()
            o.headless = True
            o.add_experimental_option("excludeSwitches", ["enable-logging"])
            driver = webdriver.Chrome(options=o, desired_capabilities=d)

            # Connect to KoboldAI Web Interface
            driver.get(url)

            # Create API Instance WebSocket
            driver.execute_script("api_instance = io.connect(loc.href);")

            # Create Event for Receiving Text Data
            driver.execute_script("api_instance.on('from_server', function(msg) {if(msg.cmd == 'updatescreen') {console.log(msg.data);}});")

            # Create New Game
            self.ResetStory()
        except:
            print("KOBOLDAPI ERROR: URL is not Reachable! Closing...")
            self.Close()

        if debug:
            print("DEBUG: KoboldAPI Ready!")

    def Generate(self, textin):
        global firstChunk
        global addSpaceBefore
        global lastOutput

        if self.addSpaceBefore:
            textin = " " + textin

        if self.chunks == 0:
            self.firstChunk = textin

        driver.execute_script("api_instance.send({'cmd': 'submit', 'data': '" + textin.replace("'", "\\'") + "'});")
        #if self.chunks == 0:
            #self.ResetStory()
        output = self.GetOutput().encode().decode("unicode-escape")
        self.lastOutput = output
        if not output.endswith("\n") and not output.endswith(" "):
            self.addSpaceBefore = True
        self.chunks+=1
        if self.reset_after_input:
            self.ResetStory()
        return output

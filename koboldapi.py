import threading
import html
import re
import time
import requests

class Controller:
    # Define HTML-Tag-Clearing Regex
    cleaner = re.compile('<.*?>')
    
    # Settings
    debug = False
    url = ""
    sid = ""
    reset_after_input = False

    # Runtime Variables
    chunks = []
    inputs = 0
    ready = False
    addSpaceBefore = False

    # Functions
    def ResetStory(self):
        global firstChunk
        global chunks
        global inputs
        global addSpaceBefore
        global ready
        
        self.chunks = []
        self.inputs = 0
        self.addSpaceBefore = False
        self.ready = False

        r = requests.post(self.url, data='42["message",{"cmd":"newgame","data":""}]')

    def SetMemory(self, memory):
        r = requests.post(self.url, data='42["message",{"cmd":"memory","data":""}]')
        r = requests.post(self.url, data='42["message",{"cmd":"submit","actionmode":0,"data":"' + memory + '"}]')

    '''def Retry(self):
        
        driver.execute_script("api_instance.send({'cmd': 'retry', 'data': ''});")
        output = self.GetOutput().encode().decode("unicode-escape")
        self.lastOutput = output
        if not output.endswith("\n") and not output.endswith(" "):
            self.addSpaceBefore = True
        return output'''

    def GetOutput(self):
        global ready
        
        if self.debug:
            print("KOBOLDAPI DEBUG: Started Output Loop Thread Successfully!")

        while True:
            r = requests.get(self.url) # Request Data
            r.encoding = 'utf-8'
            #output = str(r.content).encode('utf-8', 'surrogatepass').decode('unicode-escape') # Get Output
            output = str(r.content).encode('utf-8').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16') # Get Output
            if not output == "b'2'": # Ignore Keep-Alive Acknowledgement Outputs
                if self.debug:
                    print("KOBOLDAPI DEBUG: Received Initial Output: '" + output + "'")
                #while 'cmd' in output:
                if 'cmd' in output:
                    output = output[output.index('"cmd":"')+7:]
                    cmd = output[:output.index('"')]
                    #if cmd == 'connected':
                        #break
                    if (cmd == 'updatescreen' or cmd == 'updatechunk') and not 'generating story' in output:
                        while '<chunk' in output:
                            output = output[output.index('<chunk')+6:]
                            output = output[output.index('>')+1:]
                            chunk = output[:output.index('</chunk>')]
                            chunk = html.unescape(chunk)
                            chunk = chunk.replace('<br/>', '\n')
                            self.chunks.append(chunk)
                        self.ready = True
                        if self.debug:
                            print("KOBOLDAPI DEBUG: Ready with New Chunks!")
            r = requests.post(self.url, data="3") # Keep-Alive Request

    '''
    def GetOutputOld(self):
        global firstChunk

        valid_responses = 0

        while True:
            for entry in driver.get_log('browser'):
                output = str(entry)
                if self.debug:
                    print("KOBOLDAPI DEBUG: Received Initial Console Output: '" + output + "'")
                output = output.replace('\\u005c', '\\u005c\\u005c')
                output = str(output).encode().decode("unicode-escape")
                if 'chunk' in output:
                    try:
                        output = output[output.index('>')+1:].encode().decode("unicode-escape")
                        output = output.replace('<br/>', '\n')
                        starting_chunk = output[:output.index('<')]
                        if self.debug:
                            print("KOBOLDAPI DEBUG: '" + output + "'")
                            print("KOBOLDAPI DEBUG: '" + self.firstChunk.replace('\n', '\\n') + " | " + starting_chunk.replace('\n', '\\n') + "'")
                        if self.firstChunk.replace('\n', '\\n') == starting_chunk.replace('\n', '\\n'):
                            output = output[:output.rindex('</chunk>')]
                            output = re.sub(self.cleaner, '', output)
                            valid_responses += 1
                            #if valid_responses == 2:
                            return output
                    except:
                        pass
            time.sleep(1)
    '''

    def Initialise(self, _url, _debug=False, _reset_after_input=False):
        global url
        global debug
        global reset_after_input
        global sid

        self.url = _url
        self.debug = _debug
        self.reset_after_input = _reset_after_input

        if self.debug:
            print("KOBOLDAPI DEBUG: Debug Mode is Enabled!")

        try:
            # Check Connection to URL
            if requests.get(self.url).status_code != 200:
                print("KOBOLDAPI ERROR: URL is not Reachable! Halting...")
                return False
        except:
            print("KOBOLDAPI ERROR: URL is not Reachable! Halting...")
            return False

        if self.debug:
            print("KOBOLDAPI DEBUG: KoboldAPI Ready!")

        # Point URL to API Endpoint
        if self.url.endswith("#"):
            self.url = self.url[:-1]
        if not self.url.endswith("/"):
            self.url = self.url + "/"
        self.url = self.url + "socket.io/?EIO=4&transport=polling&t=0"

        # Get API Key
        r = requests.get(self.url)

        self.sid = str(r.content)
        self.sid = self.sid[self.sid.index('"sid":')+7:]
        self.sid = self.sid[:self.sid.index('"')]
        
        self.url = self.url + "&sid=" + self.sid

        # Connect to API
        r = requests.post(self.url, data="40")

        # Create New Game
        self.ResetStory()

        # Begin Output Loop Thread
        t = threading.Thread(target=self.GetOutput)
        t.daemon = True
        t.start()

        return True

    def Generate(self, textin, new_only=False):
        global addSpaceBefore
        global ready
        global inputs

        if self.addSpaceBefore:
            textin = " " + textin

        #textin.replace("'", "\\'")
        gen_cmd = '42["message",{"cmd":"submit","actionmode":0,"data":"' + textin.replace('"', '\\"').replace("\n", "\\n") + '"}]'
        if self.debug:
            print("KOBOLDAPI DEBUG: URL: " + self.url + " Payload: " + gen_cmd)

        r = requests.post(self.url, data=gen_cmd.encode('utf-8'), headers={'Content-type': 'text/plain; charset=utf-8'})

        output = ""
        if len(self.chunks) > 0:
            self.chunks.append(textin.replace("\\n", "\n"))
        while True:
            if self.ready == True:
                for chunk in self.chunks:
                    output = output + chunk
                self.ready = False
                break
        #output = self.GetOutput().encode().decode("unicode-escape")
        #output = ""
        output = output.encode('utf-8').decode('unicode-escape').encode('utf-16', 'surrogatepass').decode('utf-16')

        if self.reset_after_input:
            self.ResetStory()

        if new_only:
            output = textin.replace("\\n", "\n") + self.chunks[len(self.chunks)]

        if not output.endswith("\n") and not output.endswith(" "):
            self.addSpaceBefore = True

        self.inputs = self.inputs + 1

        return output

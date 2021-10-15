# KoboldAPI
A Work-In-Progress Python Module for Interfacing with [KoboldAI](https://github.com/KoboldAI/KoboldAI-Client)'s Console API.

To test this for Free (with certain restrictions) you can use [Google Colab.](https://colab.research.google.com/drive/1pG9Gz9PrqklNBESPNaXvfctMVnvwf_Q8)

## Features
```
* Connects to a KoboldAI Web Interface
* Sends & Receives Text from the AI
```

## Setup

### Install Requirements
To install requirements, you can install directly from the requirements.txt file
#### Linux
```
pip3 install -r requirements.txt
```
#### Windows
```
python -m pip install -r requirements.txt
```

## Usage

The Module can be imported with `import koboldapi`

Create an API Controller with `controller = koboldapi.Controller()`

See the supplied `Demo.py` for an example implementation

---

# API Classes

## koboldapi.Controller()

### Description

Class that Controls the API

# API Functions

## controller.Initialise(_url, _debug=False, _reset_after_input=False)

### Description

Initialises and Connects the API to KoboldAI. Returns True on Success, False on Failure

### Arguments
| Type   | Name                         | Description                                                                  |
|--------|------------------------------|------------------------------------------------------------------------------|
| STRING | `_url`                       | The KoboldAI Web URL To Connect To                                           |
| BOOL   | `_debug` = False             | Print Additional Debug Information                                           |
| BOOL   | `_reset_after_input` = False | Whether or not to Clear the AI's Memory of the Current Text after each Input |

### Returns
| Type | Name               | Description                                                                                  |
|------|--------------------|----------------------------------------------------------------------------------------------|
| BOOL | *No Name* | Success Boolean. Returns True on Initialisation Success, and False on Initialisation Failure |

## controller.Close()

### Description

Closes & Cleans Up the API

### Arguments
| No Arguments |
|--------------|

### Returns
| No Returns |
|------------|

## controller.Generate(textin, new_only=False)

### Description

Generates Text from the AI using a given Input Text, and returns the Generated Output Text

### Arguments
| Type   | Name               | Description                           |
|--------|--------------------|---------------------------------------|
| STRING | `textin`           | The Input Text to Generate Text After |
| BOOL   | `new_only` = False | Only return Newly Generated Text      |

### Returns
| Type   | Name      | Description        |
|--------|-----------|--------------------|
| STRING | *No Name* | The Generated Text |

## controller.GetOutput()

### Description

Gets the Text Output from the AI

### Arguments
| No Arguments |
|--------------|

### Returns
| Type   | Name     | Description        |
|--------|----------|--------------------|
| STRING | `output` | The Generated Text |

## controller.ResetStory()

### Description

Clears the AI's Memory of the Current Text

### Arguments
| No Arguments |
|--------------|

### Returns
| No Returns |
|------------|

## controller.SetMemory(memory)

### Description

Set the AI's Memory to the Given Text

### Arguments
| Type   | Name     | Description                              |
|--------|----------|------------------------------------------|
| STRING | `memory` | The Input Text to Set the AI's Memory to |

### Returns
| No Returns |
|------------|

## controller.Retry()

### Description

Tells the AI to Retry it's Last Generated Chunk

### Arguments
| No Arguments |
|--------------|

### Returns
| Type   | Name      | Description        |
|--------|-----------|--------------------|
| STRING | *No Name* | The Generated Text |

## controller.CommandParser()

### Description

Runs as a Background Thread to keep the Connection Alive and Handle Incoming Commands

### Arguments
| No Arguments |
|--------------|

### Returns
| No Returns |
|------------|
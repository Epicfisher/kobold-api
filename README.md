# KoboldAPI
A Work-In-Progress Python Module for Interfacing with KoboldAI's Console API.

## Features
```
* Connects to a KoboldAI Web Interface
* Sends & Receives Text from the AI
```

## Missing Features
```
Empty List as of Now
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

# API Functions

## controller.Initialise(_url, _debug = False, _reset_after_input = False)

### Arguments
| Type   | Name                         | Description                                                                  |
|--------|------------------------------|------------------------------------------------------------------------------|
| STRING | `_url`                       | The KoboldAI Web URL To Connect To                                           |
| BOOL   | `_debug` = False             | Print Additional Debug Information                                           |
| BOOL   | `_reset_after_input` = False | Whether or not to Clear the AI's Memory of the Current Text after each Input |

### Returns
| No Returns |
|------------|

```Initialises and Connects the API to KoboldAI```

## controller.Close()

### Arguments
| No Arguments |
|--------------|

### Returns
| No Returns |
|------------|

```Closes & Cleans Up the API + the Chrome WebDriver```

## controller.ResetStory()

### Arguments
| No Arguments |
|--------------|

### Returns
| No Returns |
|------------|

```Clears the AIs Memory of the Current Text```

## controller.Generate(textin)

### Arguments
| Type   | Name     | Description                           |
|--------|----------|---------------------------------------|
| STRING | `textin` | The Input Text to Generate Text After |

### Returns
| Type   | Name     | Description              |
|--------|----------|--------------------------|
| STRING | `output` | The Newly Generated Text |

```Generates Text from the AI using a given Input Text. Calls "controller.GetOutput()" Afterwards```

## controller.GetOutput()

### Arguments
| No Arguments |
|--------------|

### Returns
| Type   | Name     | Description              |
|--------|----------|--------------------------|
| STRING | `output` | The Newly Generated Text |

```Gets the Output of the last Generate()```
# Voice Assistant
A simple voice assistant that uses `vosk` for speech-to-text and `silero` for text-to-speech. The assistant can be activated using a wake word detection system from `picovoice`.
It can be easilty extended to include more features like weather, news, etc.
- [x] Wake word detection
- [x] Configurable commands that can be set using simple `.json` file
- [x] Possibility of executing shell commands or any other scripts you want
- [x] Easy ChatGPT integration
- [x] Text-to-speech using open source multilanguage pretrained `silero` models

## Prerequisites

### `vosk` model for **STT**
1. Go to https://alphacephei.com/vosk/models and choose the model you want to use
2. I recommend to first try small models like `vosk-model-small-en-us-0.15` or `vosk-model-small-en-us-0.4`
3. Download the model and extract it to the project folder
4. Add the path to the model in the `.env` file

### `picovoice` for wake word detection
1. go to https://picovoice.ai/platform/porcupine/ 
2. register and create a wake word for the assistant
3. Grab the API key and add it to the `.env` file to `PICOVOICE_API_KEY` variable
4. Download the `.ppn` file and add it to the project folder
5. Add the path to the `.ppn` file in the `.env` file to `PICOVOICE_KEYWORD_PATH` variable

### `silero` for **TTS**
1. Go [to the silero repo](https://github.com/snakers4/silero-models/blob/6b0bb8a7637d791fbb7adf22c56af1c89758ff19/models.yml#L323) and choose the model you want to use
2. Add needed variables to the `.env` file
3. Cache for the model will be created after the first launch in the `.cache/torch/hub/snakers4_silero-models_master` folder

## Installation
1. Clone the repository
2. Install poetry using `pip install poetry`
3. Run `poetry install` to install the dependencies
4. Create a `.env` file. You can use the `.env.example` file as a template
5. Follow the instructions above to prepare the `vosk` model and `picovoice` wake word detection
6. Run the assistant using `poetry run python main.py`
7. Say the wake word and ask the assistant to tell you `current time`
8. You are all set!
#### P.S. You can add more commands following [this guide](#adding-new-commands)

## Adding new commands
### Simple commands
1. Create a directory in the `commands` folder with the name of the command
2. Create a `config.json` file with the following structure:
```json
{
  "commands": [
    {
      "name": "hello",
      "action": "voice",
      "aliases": [
        "hey there",
        "hi",
        "hello"
      ],
      "responses": [
        "Hello, how can I help you?"
      ]
    }
  ]
}
```
3. That's basically it. You can add more commands to the `commands` array. The assistant will randomly choose one of the responses from the `responses` array

### Advanced commands
1. Create a directory in the `commands` folder with the name of the command
2. Create a `config.json` file with the following structure:
```json
{
  "commands": [
    {
      "name": "open_browser",
      "action": "script",
      "aliases": [
        "open browser",
        "run browser",
        "open google",
        "open chrome"
      ],
      "params": {
        "url": "https://www.google.com"
      }
    }
  ]
}
```
3. The `action` field should be set to `script` if you want to execute a script or a shell command
4. Create a `script.py` file in the command directory
5. It should contain a function with name `script` that looks like this:
```python
def script(*args, **kwargs) -> None:
    ...
```
6. You can add a `depends_on` property to the command, so it can use another command's script. In this case you don't need to create a separate folder and a new config.
    
    For example, you can add a `open_youtube` command that depends on `open_browser` command. 
    
    This is useful, because you don't need to write the same script multiple times. The `open_youtube` command can just call the `open_browser` script and then open youtube. The `config.json` file should look like this:
```json
{
  "commands": [
    {
      "name": "open_youtube",
      "action": "script",
      "aliases": [
        "open youtube",
        "run youtube"
      ],
      "depends_on": "open_browser",
      "params": {
        "url": "https://www.youtube.com"
      }
    }
  ]
}
```
7. **!NOT TESTED!** You can use any structure you want inside the command directory. But the main script should be named `script.py` and contain a function `script` that will be executed when the command is called.

## ChatGPT integration
1. Go to https://platform.openai.com/api-keys and create an API key
2. Add the API key to the `.env` file to the `OPENAI_API_KEY` variable
3. Add the `chat_gpt` command to the `commands` folder
4. The `config.json` file should look like this:
```json
{
  "commands": [
    {
      "name": "chat_gpt",
      "action": "chat_gpt",
      "aliases": [
        "tell me",
        "search for"
      ]
    }
  ]
}
```

## Possible issues
1. Current implementation of ChatGPT is not perfect. It only works with the success responses etc. Will be improved ASAP
2. You may face a problem with incorrect input device. Check `device_index` in the `_init_recorder` function in the `speech_to_text.py` file
3. Commands `open_browser` and `open_youtube` logs **WARNING** messages, because of the incorrect response of the script execution. This will be fixed in the future 
4. Any other issues can be reported in the issues section. I will try to help you as soon as possible

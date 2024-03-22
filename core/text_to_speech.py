import sounddevice as sd
import torch

import config


class TTS:
    def __init__(self):
        self.model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-models",
            model="silero_tts",
            language=config.LANGUAGE,
            speaker=config.MODEL_ID,
            trust_repo=True,
        )
        self.model.to(config.TTS_DEVICE)

    def speak(self, phrase: str) -> None:
        audio = self.model.apply_tts(
            text=phrase,
            speaker=config.SPEAKER,
            sample_rate=config.TTS_SAMPLE_RATE,
        )
        sd.play(audio, config.TTS_SAMPLE_RATE)
        sd.wait()
        sd.stop()


tts = TTS()

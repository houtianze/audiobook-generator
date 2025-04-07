# DON'T change the sampling frequecy, otherwise the speed of the audio will be
# srewed up, this 24K Hz is what Kokoro uses to generate audio.
# https://github.com/KoljaB/RealtimeTTS/blob/25b562c331d754185dfd260aae1b2ccd06a12232/RealtimeTTS/engines/kokoro_engine.py#L125
DEFAULT_SAMPLE_RATE=24000
DEFAULT_VOICE="af_heart"
DEFAULT_SPEED=1.0
DEFAULT_FORMAT="mp3"
DEFAULT_RESUME=True
DEFAULT_BARE_OUTPUT=False
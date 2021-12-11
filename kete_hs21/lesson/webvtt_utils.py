from webvtt import WebVTT, Caption


def convert_from_ms(milliseconds):
    seconds, milliseconds = divmod(milliseconds,1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    seconds = seconds + milliseconds/1000
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}.{int(milliseconds):04}"


def create_vtt_from_azure_output(azure_transcript_json: dict, vtt_output_filepath):
    vtt = WebVTT()
    for phrase in azure_transcript_json.get("recognizedPhrases"):
        offset_ms = phrase.get("offsetInTicks") / 10_000
        duration_ms = phrase.get("durationInTicks") / 10_000
        start_caption_ms = offset_ms
        end_caption_ms = offset_ms + duration_ms
        caption = phrase.get("nBest")[0].get("display")
        vtt.captions.append(
            Caption(
                convert_from_ms(start_caption_ms),
                convert_from_ms(end_caption_ms),
                (caption,)
            )
        )
    vtt.save(vtt_output_filepath)



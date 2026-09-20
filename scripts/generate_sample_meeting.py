import os
import wave
import struct
import win32com.client

def create_silence_chunk(duration_sec, sample_rate=16000, num_channels=1, sampwidth=2):
    num_frames = int(duration_sec * sample_rate)
    return b'\x00' * (num_frames * num_channels * sampwidth)

def generate_tts_segment(text, voice_name, rate=0, output_path="temp_seg.wav"):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    
    # Audio format: SAFT16kHz16BitMono = 18
    stream.Format.Type = 18
    stream.Open(output_path, 3) # 3 = SSFMCreateForWrite
    speaker.AudioOutputStream = stream
    
    # Select voice
    voices = speaker.GetVoices()
    for i in range(voices.Count):
        if voice_name.lower() in voices.Item(i).GetDescription().lower():
            speaker.Voice = voices.Item(i)
            break
            
    speaker.Rate = rate
    speaker.Speak(text)
    stream.Close()

def main():
    print("Generating 2-minute sample meeting audio...")
    
    dialogue = [
        ("David", "Good morning team, welcome to our weekly project sync. Today we need to review the Q3 release milestones, check the status of our backend migrations, and finalize the deployment schedule for this Friday."),
        ("Zira", "Thanks David. On the backend side, we successfully completed the database indexing updates and resolved the query latency issues. API response times are now down by roughly forty percent under high load."),
        ("David", "That is great news, Sarah. What about the user authentication service and the Webhook notification pipeline? Are there any blockers or edge cases we should be aware of?"),
        ("Zira", "All OAuth2 endpoints and token refresh cycles passed our automated regression tests. The webhook dispatcher is now resilient with automatic retries and HMAC signature verification. We also conducted load tests with five thousand simulated concurrent users without any packet drop."),
        ("David", "Excellent. Regarding the frontend and mobile responsiveness, have we tested the new dark mode theme across Safari, Chrome, and Edge browsers?"),
        ("Zira", "Yes, the UI styling fixes are merged. The responsive drawer menu and audio meters are working smoothly on both desktop and tablet resolutions. We fixed the layout overflow bug reported yesterday in the settings modal."),
        ("David", "Perfect. Let us go over our key action items before wrapping up. First, Sarah will deploy the release candidate build to staging by two PM today. Second, the QA team will complete the final sanity run by tomorrow morning. Third, once approved, we will proceed with the production rollout on Friday at five PM."),
        ("Zira", "Understood, David. I will monitor the staging logs and coordinate with the infrastructure team. Everything is on track for Friday."),
        ("David", "Awesome work, everyone. Thank you for your hard work and let us reconvene tomorrow for the quick pre-release check-in. Have a productive day.")
    ]
    
    temp_files = []
    combined_frames = bytearray()
    sample_rate = 16000
    channels = 1
    sampwidth = 2
    
    for idx, (speaker_name, text) in enumerate(dialogue):
        temp_file = f"temp_seg_{idx}.wav"
        temp_files.append(temp_file)
        
        voice = "David" if speaker_name == "David" else "Zira"
        rate = -1 # slightly natural conversational pace
        
        print(f"Generating segment {idx+1}/{len(dialogue)} ({speaker_name})...")
        generate_tts_segment(text, voice, rate, temp_file)
        
        # Read frames
        with wave.open(temp_file, 'rb') as wf:
            sample_rate = wf.getframerate()
            channels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            frames = wf.readframes(wf.getnframes())
            combined_frames.extend(frames)
            
        # Add 0.8 second pause between speakers
        silence = create_silence_chunk(0.8, sample_rate, channels, sampwidth)
        combined_frames.extend(silence)
        
    output_filename = "sample_meeting_2min.wav"
    with wave.open(output_filename, 'wb') as out_wf:
        out_wf.setnchannels(channels)
        out_wf.setsampwidth(sampwidth)
        out_wf.setframerate(sample_rate)
        out_wf.writeframes(combined_frames)
        
    # Clean up temp files
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)
            
    total_duration = len(combined_frames) / (sample_rate * channels * sampwidth)
    print(f"\nSuccessfully created '{output_filename}'!")
    print(f"Duration: {round(total_duration, 1)} seconds ({round(total_duration/60, 2)} minutes)")
    print(f"Format: {sample_rate}Hz, {channels} Channel(s), {sampwidth*8}-bit WAV PCM")

if __name__ == "__main__":
    main()

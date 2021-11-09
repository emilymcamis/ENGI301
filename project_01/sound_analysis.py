"""
--------------------------------------------------------------------------
Sound Analysis
--------------------------------------------------------------------------
License:   
Copyright 2020 Emily McAmis

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Describe here
"""
import pyaudio
import sys
from scipy.io.wavfile import write
import sounddevice as sd
import numpy as np
from scipy import arange
import soundfile
from aubio import source, pitch

"""
def findPeak(magnitude_values, noise_level=2000):
    
    splitter = 0
    # zero out low values in the magnitude array to remove noise (if any)
    magnitude_values = numpy.asarray(magnitude_values)        
    low_values_indices = magnitude_values < noise_level  # Where values are low
    magnitude_values[low_values_indices] = 0  # All low values will be zero out
    
    indices = []
    
    flag_start_looking = False
    
    both_ends_indices = []
    
    length = len(magnitude_values)
    for i in range(length):
        if magnitude_values[i] != splitter:
            if not flag_start_looking:
                flag_start_looking = True
                both_ends_indices = [0, 0]
                both_ends_indices[0] = i
        else:
            if flag_start_looking:
                flag_start_looking = False
                both_ends_indices[1] = i
                # add both_ends_indices in to indices
                indices.append(both_ends_indices)
                
    return indices

def extractFrequency(indices, freq_threshold=2):
    
    extracted_freqs = []
    
    for index in indices:
        freqs_range = freq_bins[index[0]: index[1]]
        avg_freq = round(numpy.average(freqs_range))
        
        if avg_freq not in extracted_freqs:
            extracted_freqs.append(avg_freq)

    # group extracted frequency by nearby=freq_threshold (tolerate gaps=freq_threshold)
    group_similar_values = split(extracted_freqs, where(diff(extracted_freqs) > freq_threshold)[0]+1 )
    
    # calculate the average of similar value
    extracted_freqs = []
    for group in group_similar_values:
        extracted_freqs.append(round(numpy.average(group)))
    
    print("freq_components", extracted_freqs)
    return extracted_freqs

if __name__ == '__main__':
    
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write('output.wav', fs, myrecording)
    
    file_path = 'myrecording'
    print('Open audio file path:', file_path)
    
    audio_samples, sample_rate  = soundfile.read(file_path, dtype='int16')
    number_samples = len(audio_samples)
    print('Audio Samples: ', audio_samples)
    print('Number of Sample', number_samples)
    print('Sample Rate: ', sample_rate)
    
    # duration of the audio file
    duration = round(number_samples/sample_rate, 2)
    print('Audio Duration: {0}s'.format(duration))
    
    # list of possible frequencies bins
    freq_bins = arange(number_samples) * sample_rate/number_samples
    print('Frequency Length: ', len(freq_bins))
    print('Frequency bins: ', freq_bins)
    
#     # FFT calculation
    fft_data = scipy.fft(audio_samples)
    print('FFT Length: ', len(fft_data))
    print('FFT data: ', fft_data)

    freq_bins = freq_bins[range(number_samples//2)]      
    normalization_data = fft_data/number_samples
    magnitude_values = normalization_data[range(len(fft_data)//2)]
    magnitude_values = numpy.abs(magnitude_values)
        
    indices = findPeak(magnitude_values=magnitude_values, noise_level=200)
    frequencies = extractFrequency(indices=indices)
    print("frequencies:", frequencies)
    

  """


"""
import pyaudio
from scipy.io.wavfile import write
import numpy as np
import sys
from aubio import source, pitch

fs = 44100  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write('output.wav', fs, myrecording)

audio_samples, sample_rate = soundfile.read(file_path, dype='int16')
number_samples = len(audio_samples)

freq_bins = arange(number_samples//2)*sample_rate/number_samples

fft_data = scipy.fft(audio_samples)

freq_bins = freq_bins[range(number_samples//2)]
normalization_data = fft_data/number_samples
magnitude_values = normalization_data[range(len(fft_data)//2)]
magnitude_values = numpy.abs(magnitude_values)

indices = findPeak(magnitude_values=magnitude_values, noise_leve=200)
frequencies=extractFrequency(indices=indices)
print(frequencies)"""

"""
from way 1
"""

win_s = 4096
hop_s = 512

fs = 4000  # Sample rate
seconds = 3  # Duration of recording

myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()
write('output.wav', fs, myrecording)

s = source("output.wav", fs, hop_s)
samplerate = s.samplerate


tolerance = 0.8

pitch_o = pitch("yin", win_s, hop_s, fs)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

pitches = []
confidences = []

total_frames = 0
while True:
    samples, read = s()
    pitch = pitch_o(samples)[0]
    pitches += [pitch]
    confidence = pitch_o.get_confidence()
    confidences += [confidence]
    total_frames += read
    if read < hop_s: break

frequency_value = int(np.array(pitches).mean())
print("Average frequency = " + str(np.array(pitches).mean()) + " hz")

"""


this doesnt work
def spectral_properties(y: np.ndarray, fs: int) -> dict:
    spec = np.abs(np.fft.rfft(y))
    freq = np.fft.rfftfreq(len(y), d=1 / fs)
    spec = np.abs(spec)
    amp = spec / spec.sum()
    mean = (freq * amp).sum()
    sd = np.sqrt(np.sum(amp * ((freq - mean) ** 2)))
    amp_cumsum = np.cumsum(amp)
    median = freq[len(amp_cumsum[amp_cumsum <= 0.5]) + 1]
    mode = freq[amp.argmax()]
    Q25 = freq[len(amp_cumsum[amp_cumsum <= 0.25]) + 1]
    Q75 = freq[len(amp_cumsum[amp_cumsum <= 0.75]) + 1]
    IQR = Q75 - Q25
    z = amp - amp.mean()
    w = amp.std()
    skew = ((z ** 3).sum() / (len(spec) - 1)) / w ** 3
    kurt = ((z ** 4).sum() / (len(spec) - 1)) / w ** 4

    result_d = {
        'mean': mean,
        'sd': sd,
        'median': median,
        'mode': mode,
        'Q25': Q25,
        'Q75': Q75,
        'IQR': IQR,
        'skew': skew,
        'kurt': kurt
    }

    return result_d
    
array=np.array(myrecording)
print(spectral_properties(array,fs))"""
'''
NOAA Weather satellite data decoder.
Open source project to train your Python and signal processing skills.
MIT Lisence, free to use as you wish. 
Project repository: https://github.com/mimimaki/NOAA_decoder

Written by Miikka Mäki (git: mimimaki), 5th August 2024.
'''

# Import these!
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import scipy.signal as signal
#from scipy.signal import butter, filtfilt, find_peaks
from PIL import Image
# Not mandatory, but helps to debug:
import pdb

filename = 'media/example.wav'      # Executing from project dir

# Read the wav file
fs, data = wavfile.read(filename)
data = data.astype(np.int32)

# Calculate time scale
t = np.arange(0.,len(data))/fs

# Plot waveform and spectrum for illustration
fig = plt.figure(figsize=(12, 4))
ax = fig.subplots(nrows=1,ncols=2)
ax[0].plot(t[10*fs:11*fs], data[10*fs:11*fs])
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude')
ax[0].set_title('Amplitude (32-bit accuracy and ' + str(fs/1000) + ' kHz fs)')
ax[0].grid()

# Resample
data = data[::4]
fs = fs//4

# Demodulate signal using scipy.signal Hilbert transform 
hilbert = signal.hilbert(data)
data_am = np.abs(hilbert)

ax[1].plot(data[10*fs:11*fs], label='Original signal')
ax[1].plot(data_am[10*fs:11*fs], label='Signal envelope')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Amplitude')
ax[1].set_title('Demodulated data with ' + str(fs/1000) + ' kHz fs')
ax[1].legend()

# Decode the demodulated data into a frame
width = int(0.5*fs)
height = data_am.shape[0]//width
image = Image.new('L', (width, height))
row = 0 
col = 0
for pixel in range(data_am.shape[0]):
    brightness = int(data_am[pixel]//32 - 32)
    if brightness < 0:
        brightness = 0
    elif brightness > 255: 
        brightness = 255
    image.putpixel((row, col), brightness)  # Place the pixel
    row += 1
    if row >= width:
        row = 0
        col += 1
        if col >= height:
            break

# Plot the decoded image
image = image.resize((width, 4*height))
plt.figure()
plt.imshow(image)
plt.xlabel('Pixels')
plt.ylabel('Pixels')
plt.title('Decoded NOAA Image')
plt.show()
import numpy as np
import pylab as plt
import cmath as cm
import scipy as sp
import scipy.fftpack as ft
import struct
import sys
import pyaudio
import wave
import os

#========================================================================================
#		AUDIO CLASS
#========================================================================================
class audio(object):
    """Audio class
    
    Attributes
    ----------
    name: string
      Audio name. Default: 'audio000'
      
    rate: integer
      Frequency of audio data. Default: 44100
      
    format: pyaudio format (paInt8, paInt16, paInt24, paInt32)
      Sample format (bits). Default: 16 bits
      
    channels: integer
      Number of channels. Default: 1
      
    chunk: integer
      Size of head of file. Default: 1024
    """
    #************************************************************************************
    #	ATTRIBUTES
    #************************************************************************************
    name = "'audio000'"
    rate = 44100
    format = pyaudio.paInt16
    channels = 1
    chunk = 1024
    time = 5


     #************************************************************************************
    #	METHODS
    #************************************************************************************
    def __init__(self,**kwargs):
	#Set attributes using: default and argument values
        updatedic(self.__dict__,audio.__dict__,**kwargs)
        #Data in number format
        self.data = []
        #Data in hexagesimal format
        self.datah = []
	#Fourier transform data
        self.fdata = []
        #Frequencies of fourier transform
        self.freqs = []
        #Time Array
        self.T = np.linspace(0,self.time, int(self.time*self.rate))
        #Auxiliar array
        self.h = []
        
        
    def load(self, Data):
	"""Load a array in audio file

        Parameters:
        ----------
        Data: Array
           Array of datas to generate a sound, this must be between -32767 and 32767.
           Preferably, its lenght must be a multiple of current audio rate.
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().load(Datos)
        """
	#Update of time of audio
	self.time = len(Data)/(1.0*self.rate*self.channels)
	#Time Array
        self.T = np.linspace(0,self.time, int(self.time*self.rate))
        #Numeric data
	self.data = Data
        #Hexagesimal data
	self.datah = []
	for i in xrange(0, len(self.data)):
	    packed_value = struct.pack('h', self.data[i])
	    self.datah.append(packed_value)
	    if self.channels == 2:
		self.datah.append(packed_value)


    def loadfourier(self, Fdata):
	"""Calculate the inverse fourier transform and load it in audio file

        Parameters:
        ----------
	Fdata: array
	Array of fourier datas to generate a sound.
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().fourier(440)
        """
	#Number of datas
	Nf = len( Fdata )
	N = 2*np.round(((2**np.ceil(np.log2(2*Nf)))/self.rate)-1)*self.rate
	
	Fdata = np.array([Fdata, Fdata[::-1]])
	Fdata = Fdata.flatten()
	
	#Fourier transform
	self.data = ft.ifft(Fdata,N)
	self.data = self.data[0:N/2.]

	#for i in xrange(0, len(self.data)):
	    #self.data[i] = np.abs(self.data[i])*N/2.*cm.phase(self.data[i])/np.abs(cm.phase(self.data[i]))
	self.data = np.real(self.data)*N/4.
	
	#Reload data array
	self.load(self.data)
        
        
    def loadwav(self, filename):
	"""Load a wav file

        Parameters:
        ----------
        filename: string
           Name of wav file.
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().loadwav('audio.wav')        
        """
	#Updating of audio parameters
	wf = wave.open(filename, 'rb')
	#Initializing PyAudio
        self.pa = pyaudio.PyAudio()
        
	self.format = self.pa.get_format_from_width(wf.getsampwidth())
	self.channels = wf.getnchannels()
	self.rate = wf.getframerate()

        #Loading wav data
	self.data = np.memmap(filename, dtype='h', mode='r')
	self.datah = []
	for i in xrange(0, len(self.data)):
	    packed_value = struct.pack('h', self.data[i])
	    self.datah.append(packed_value)
	    if self.channels == 2:
		self.datah.append(packed_value)
	#Update of time of wav file
	self.time = len(self.data)/(1.0*self.rate*self.channels)
	#Time Array
        self.T = np.linspace(0,self.time, int(self.time*self.rate*self.channels))
        self.T = self.T[0:min( (len(self.T), len(self.data)) )]
        self.data = self.data[0:min( (len(self.T), len(self.data)) )]
        #Terminating PyAudio
        self.pa.terminate()


    def savewav(self, filename):
	"""Save in wav file the current file

        Parameters:
        ----------
        filename: string
           Name of wav file.
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().savewav('audio.wav')  
        """
        wf = wave.open(filename, 'w')
        wf.setparams((
	    self.channels,
	    2,
	    self.rate,
	    0,
	    'NONE',
	    'not compressed'))
        value_str = ''.join(self.datah)
	wf.writeframes(value_str)
	wf.close()
	
	
    def play(self):
	"""Play the current file

        Parameters:
        ----------
        Nothing
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().play()        
        """
	#Initializing PyAudio
        self.pa = pyaudio.PyAudio()
	#Initializing a stream
	stream = self.pa.open( 
	    format = self.format,
            channels = self.channels**2,
            rate = self.rate,
            output = True)

	self.savewav('_tmp.wav')

	wf = wave.open('_tmp.wav', 'rb')
	dataplay = wf.readframes(self.chunk)
	
	#Playing file
	while dataplay != '':
	    stream.write(dataplay)
	    dataplay = wf.readframes(self.chunk)
	    
	wf.close()
	stream.close()
	os.system('rm _tmp.wav')
	#Terminating PyAudio
        self.pa = pyaudio.PyAudio()


    def record(self, time=None):
	"""Play the current file

        Parameters:
        ----------
	time: float
           time in seconds to record.
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().record(time = 5)
        """
	#Initializing PyAudio
        self.pa = pyaudio.PyAudio()
        #Update of audio time
        if time == None:
	    time = self.time
	else:
	    self.time = time
	    #Time Array
	    self.T = np.linspace(0,self.time, int(self.time*self.rate))
        
	#Initializing a stream
	stream = self.pa.open( 
	    format = self.format,
            channels = self.channels,
            rate = self.rate,
            input = True,
            frames_per_buffer = self.chunk)
                        
	#Recording
        print "* recording"
	alldata = []
	for i in range(0, int(self.rate/self.chunk*self.time)):
	    datarecord = stream.read(self.chunk)
	    alldata.append(datarecord)
	print "* done recording"
	
	self.datah = alldata
	stream.close()
	self.savewav('_tmp.wav')
	self.loadwav('_tmp.wav')
	os.system('rm _tmp.wav')
	#Terminating PyAudio
        self.pa.terminate()
	
	
    def fourier(self):
	"""Calculate the fourier transform

        Parameters:
        ----------
	Nothing
	
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().fourier(440)
        """
	#Number of datas
	N = len( self.data )
	Nf = 2**np.ceil(np.log(N)/np.log(2.0))
	
	#Fourier transform
	self.fdata = 2*ft.fft(self.data,Nf)/N
	self.fdata = self.fdata[0:Nf/(2*self.channels)]
	
	#Frequencies of sample
	self.freqs = N/(2*self.time*self.channels)*np.linspace(0,1,Nf/(2*self.channels))
	self.freqs = self.freqs[0:Nf/(2*self.channels)]

    def inv_fourier(self):
	"""Calculate the fourier transform

        Parameters:
        ----------
	Nothing
	
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().fourier(440)
        """
	#Number of datas
	Nf = len( self.fdata )
	#N = 2**( np.log2( Nf ) + 1 ) + self.rate
	N = Nf
	
	#Fourier transform
	self.data = ft.ifft(self.fdata,N)*N/2.
	self.normalize()
	self.time = N*1.0/(2*self.rate)
	self.load(np.real(self.data))
	


    def normalize(self):
	"""Normalizing the audio file respect the maxim value

        Parameters:
        ----------
	Nothing
	
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().normalize()
        """
        Maxim = np.max(abs(self.data[100:]))/Amplitude
	self.data = self.data / Maxim
	self.data[:100] = 0
	#Hexagesimal data
	self.datah = []
	for i in xrange(0, len(self.data)):
	    packed_value = struct.pack('h', self.data[i])
	    self.datah.append(packed_value)
	    if self.channels == 2:
		self.datah.append(packed_value)
	

    def plot(self):
	"""Plot a audio data vs time

        Parameters:
        ----------
	Nothing
	
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().fourier()
        """
        N = np.min( (len(self.data), len(self.T)) )
	plt.plot( self.T[:N], self.data[:N]/Amplitude, linewidth=0.5, label='Audio Signal' )
	plt.xlabel('Time [s]')
	plt.ylabel('Amplitude [normalized]')
	plt.title('Audio Signal')
	plt.ylim( (-1,1) )
	plt.legend()
	plt.grid()
	plt.show()


    def plotfourier(self):
	"""Plot a fourier transform data vs time

        Parameters:
        ----------
	Nothing
           
        Returns:
        -------
        Nothing

        Examples:
        --------
        >> audio().plot()
        """
	self.fourier()
	Nf = len(self.fdata)
	
	plt.plot(self.freqs, abs(self.fdata)/Amplitude,
	linewidth=0.5, label='Audio Signal' )
	
	plt.xlabel('Frequency [Hertz]')
	plt.ylabel('Fourier Amplitude [normalized]')
	plt.title('Fourier transform of audio Signal')
	plt.ylim( (0,np.max(self.fdata[int(len(self.fdata)/1000.):Nf/(2*self.channels)])/Amplitude) )
	plt.xlim( (0,np.max(self.freqs)) )
	plt.legend()
	plt.grid()
	plt.show()

#Update dictionary
def updatedic(dic,default,**kwargs):
    """Update dictionary using kwargs and default values in default dictionary
    
    Parameters:
    ----------
    dic: dictionart
       Dictionary to update

    default: dictionary
       Dictionary with default values to dic.  All the dict. entries
       must be strings with the form type(value)


    kwargs: dictionary
       New values

    Returns:
    -------
    Nothing

    Examples:
    --------
    See audio class for example

    """
    for attr in default:
        if (isinstance(attr,str)) and ('__' not in attr) and ('function' not in `type(default[attr])`):
            if attr in kwargs:
                dic[attr]=kwargs[attr]
            else:
                exec("dic['%s']=%s"%(attr,default[attr]))


#========================================================================================
#		CONSTANTS
#========================================================================================
note = {
    "C-1" : 8.176,
    "C#-1": 8.662,
    "D-1" : 9.177,
    "D#-1": 9.723,
    "E-1" : 10.301,
    "F-1" : 10.913,
    "F#-1": 11.562,
    "G-1" : 12.250,
    "G#-1": 12.978,
    "A-1" : 13.750,
    "A#-1": 14.568,
    "B-1" : 15.434,
    "C0"  : 16.352,
    "C#0" : 17.324,
    "D0"  : 18.354,
    "D#0" : 19.445,
    "E0"  : 20.602,
    "F0"  : 21.827,
    "F#0" : 23.125,
    "G0"  : 24.500,
    "G#0" : 25.957,
    "A0"  : 27.500,
    "A#0" : 29.135,
    "B0"  : 30.868,
    "C1"  : 32.703,
    "C#1" : 34.648,
    "D1"  : 36.708,
    "D#1" : 38.891,
    "E1"  : 41.203,
    "F1"  : 43.654,
    "F#1" : 46.249,
    "G1"  : 48.999,
    "G#1" : 51.913,
    "A1"  : 55.000,
    "A#1" : 58.270,
    "B1"  : 61.735,
    "C2"  : 65.406,
    "C#2" : 69.296,
    "D2"  : 73.416,
    "D#2" : 77.782,
    "E2"  : 82.407,
    "F2"  : 87.307,
    "F#2" : 92.499,
    "G2"  : 97.999,
    "G#2" : 103.826,
    "A2"  : 110.000,
    "A#2" : 116.541,
    "B2"  : 123.471,
    "C3"  : 130.813,
    "C#3" : 138.591,
    "D3"  : 146.832,
    "D#3" : 155.563,
    "E3"  : 164.814,
    "F3"  : 174.614,
    "F#3" : 184.997,
    "G3"  : 195.998,
    "G#3" : 207.652,
    "A3"  : 220.000,
    "A#3" : 233.082,
    "B3"  : 246.942,
    "C4"  : 261.626,
    "C#4" : 277.183,
    "D4"  : 293.665,
    "D#4" : 311.127,
    "E4"  : 329.628,
    "F4"  : 349.228,
    "F#4" : 369.994,
    "G4"  : 391.995,
    "G#4" : 415.305,
    "A4"  : 440.000,
    "A#4" : 466.164,
    "B4"  : 493.883,
    "C5"  : 523.251,
    "C#5" : 554.365,
    "D5"  : 587.330,
    "D#5" : 622.254,
    "E5"  : 659.255,
    "F5"  : 698.456,
    "F#5" : 739.989,
    "G5"  : 783.991,
    "G#5" : 830.609,
    "A5"  : 880.000,
    "A#5" : 932.328,
    "B5"  : 987.767,
    "C6"  : 1046.502,
    "C#6" : 1108.731,
    "D6"  : 1174.659,
    "D#6" : 1244.508,
    "E6"  : 1318.510,
    "F6"  : 1396.913,
    "F#6" : 1479.978,
    "G6"  : 1567.982,
    "G#6" : 1661.219,
    "A6"  : 1760.000,
    "A#6" : 1864.655,
    "B6"  : 1975.533,
    "C7"  : 2093.005,
    "C#7" : 2217.461,
    "D7"  : 2349.318,
    "D#7" : 2489.016,
    "E7"  : 2637.020,
    "F7"  : 2793.826,
    "F#7" : 2959.955,
    "G7"  : 3135.963,
    "G#7" : 3322.438,
    "A7"  : 3520.000,
    "A#7" : 3729.310,
    "B7"  : 3951.066,
    "C8"  : 4186.009,
    "C#8" : 4434.922,
    "D8"  : 4698.636,
    "D#8" : 4978.032,
    "E8"  : 5274.041,
    "F8"  : 5587.652,
    "F#8" : 5919.911,
    "G8"  : 6271.927,
    "G#8" : 6644.875,
    "A8"  : 7040.000,
    "A#8" : 7458.620,
    "B8"  : 7902.133,
    "C9"  : 8372.018,
    "C#9" : 8869.844,
    "D9"  : 9397.273,
    "D#9" : 9956.063,
    "E9"  : 10548.08,
    "F9"  : 11175.30,
    "F#9" : 11839.82,
    "G9"  : 12543.85,
}

#Amplitude of standart audio format
Amplitude = 32767.

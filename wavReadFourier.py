import recursion3 as amplitude

from scikits.audiolab import Sndfile
from scikits.audiolab import wavread
import numpy as np
import matplotlib.pyplot as plt
import fourier

from matplotlib import cm  
from numpy import meshgrid  
from mpl_toolkits.mplot3d import Axes3D

class wavReaderFourierTransformer:


    # Constructor
    def __init__(self, wavFileName, startSeconds, endSeconds, intervalWidthSeconds, intervalStartSeconds, spectrumWidth):
        self.wavFileName = wavFileName

        self.wavFile = Sndfile(self.wavFileName, 'r')
        self.fs=self.wavFile.samplerate
        self.nc=self.wavFile.channels
        self.enc=self.wavFile.encoding
        self.wavFile.close()
        del self.wavFile

        self.sampling_interval = 1.0/self.fs

        self.start = int(self.fs*startSeconds)
        self.end = int(self.fs*endSeconds)
        self.intervalWidth = int(self.fs*intervalWidthSeconds)
        self.intervalStartFrequency = int(self.fs*intervalStartSeconds)

        self.dataExists = False
        self.amplitudes = []
        self.frequencies = []
        self.times = []

        self.narrowDataExists = False
        self.narrowAmplitudes = []
        self.narrowFrequencies = []
        self.spectrumWidth = spectrumWidth
        self.cutOffIndex = 0

        self.compressedNarrowDataExists = False
        self.compressedNarrowAmplitudes = []
        self.compressedNarrowFrequencies = []
        self.colors = {
            "white": (1,1,1),
            "black": (0,0,0),
            "red": (232/255.0,4/255.0,4/255.0),
            "green": (82/255.0,237/255.0,13/255.0),
            "blue": (51/255.0,47/255.0,220/255.0),
            "yellow": (248/255.0, 220/255.0, 13/255.0),
            "darkblue": (0, 27/255, 81/255),
            "lightblue": (0, 180/255, 1)
        }

    # These are the functions to call to ask for data
    def getNonNarrowFrequencyAmplitudes(self):
        self.__requireData
        return self.frequencies, self.amplitudes

    def getFrequencyAmplitudes(self): # This is leftover from earlier fucked up times
        return self.getNarrowFrequencyAmplitudes()

    def getNarrowFrequencyAmplitudes(self):
        self.__requireNarrowData()
        return self.narrowFrequencies, self.narrowAmplitudes

    def getCompressedNarrowFrequencyAmplitudes(self):
        self.__requireCompressedNarrowData()
        return self.compressedNarrowFrequencies, self.compressedNarrowAmplitudes

    def getTimes(self):
        return self.times

    def getMaxFourierFrequency(self):
        return self.fs/2.0

    def getDeltaFourierFrequency(self):
        return self.fs/self.intervalWidth





    #These functions should not be used from outside
    def __requireData(self):
        if (not self.dataExists):
            self.__calcFreqAmps(narrow=False, compress=False)

    def __requireNarrowData(self):
        if (not self.narrowDataExists):
            if (self.dataExists):
                self.__narrowFrequencyAmplitudes()
            else:
                self.__calcFreqAmps(narrow=True, compress=False)

    def __requireCompressedNarrowData(self):
        if (not self.compressedNarrowDataExists):
            if (not self.narrowDataExists):
                if (self.dataExists):
                    self.__compressFrequencyAmplitudes()
                else:
                    self.__calcFreqAmps(narrow=True, compress=True)
            else:
                self.__compressNarrowFrequencyAmplitudes()
    
    # Multipurpose function for Fourier transform of the wav file
    def __calcFreqAmps(self, narrow=False, compress=False, intervalSize=10, compressionMethodString="maxMedianDifference"): 
        # Clear calculated data if already exists
        if (compress):
            self.compressedNarrowAmplitudes = []
            self.compressedNarrowFrequencies = []
        elif (narrow):
            self.narrowAmplitudes = []
            self.narrowFrequencies = []         
        else:
            self.amplitudes = []
            self.frequencies = []

        self.times = []

        # Compression is set to only work with narrowed data: compression of the entire spectrum is never interesting
        if (compress):
            print("Compressing works only with narrowed data")
            narrow = True

        # Find the place where the cutOff should occur if the spectrum should be narrowed down
        if (narrow):
            self.__calcCutOffIndex()
        
        # Read the wav file
        self.wavFile = Sndfile(self.wavFileName, 'r')

        # Get the intervals
        for intervalStartFrame in range(self.start, self.end, self.intervalStartFrequency):
            startTime = intervalStartFrame*self.sampling_interval
            endTime = (intervalStartFrame+self.intervalWidth)*self.sampling_interval
            self.times.append((startTime+endTime)/2.0)

            output = amplitude.output_signal(self.intervalWidth, intervalStartFrame, self.wavFile)
            frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)

            if (narrow):
                frequencies, amplitudes = self.__narrowSpectrum(frequencies, amplitudes, self.cutOffIndex)

            if (compress):
                frequencies, amplitudes = self.__compressSpectrum(frequencies, amplitudes, intervalSize, compressionMethodString)

            if (compress):
                self.compressedNarrowAmplitudes.append(amplitudes)
                self.compressedNarrowFrequencies = frequencies
            elif (narrow):
                self.narrowAmplitudes.append(amplitudes)
                self.narrowFrequencies = frequencies
            else:
                self.amplitudes.append(amplitudes)
                self.frequencies = frequencies

            print (intervalStartFrame/self.fs),"/",self.end/self.fs

        self.wavFile.close()
        del self.wavFile

        if (compress):
            self.compressedNarrowDataExists = True
        elif (narrow):
            self.narrowDataExists = True
        else:
            self.dataExists = True

    def __calcCutOffIndex(self):

        self.wavFile = Sndfile(self.wavFileName, 'r')
        output = amplitude.output_signal(self.intervalWidth, 0, self.wavFile)

        frequencies, amplitudes = fourier.getFFT(self.sampling_interval, output)

        spectrumWidth = -abs(self.spectrumWidth)

        cutOffIndex = -1

        for i in range(np.size(frequencies)-1):
            if ((frequencies[i]<spectrumWidth) and (frequencies[i+1]>spectrumWidth)
                    or frequencies[i]==spectrumWidth 
                    or (frequencies[i]>spectrumWidth) and (frequencies[i+1]<spectrumWidth)):
                cutOffIndex = i
                break

        if (cutOffIndex==-1):
            print("given frequency was not found")
            cutOffIndex = 0 # Don't cut the spectrum

        self.cutOffIndex = cutOffIndex
        del self.wavFile


    def __narrowSpectrum(self, frequencies, amplitudes, cutOffIndex):
        amplitudes = amplitudes[cutOffIndex:-cutOffIndex]
        frequencies = frequencies[cutOffIndex:-cutOffIndex]
        return frequencies, amplitudes

    def __getNarrowSpectra(self, inputfrequencies, inputamplitudes):
        amplitudes = []
        frequencies = []
        if (self.cutOffIndex == 0):
            self.__calcCutOffIndex()

        for amp in inputamplitudes:
            frequencies, amplitudes = self.__narrowSpectrum(inputfrequencies, amp, cutOffIndex)
            amplitudes.append(amplitude)
        return frequencies, amplitudes

    def __compressSpectrum(self, frequencies, amplitudes, intervalSize, compressionMethodString):
        resultFrequencies = []
        resultAmplitudes = []

        method = {
            "mean": self.__mean,
            "median": self.__median,
            "maxMeanDifference": self.__maxMeanDifference,
            "maxMedianDifference": self.__maxMedianDifference
        }.get(compressionMethodString, self.__mean)

        for i in range(0, np.size(amplitudes), intervalSize):
            currentInterval = amplitudes[i:i+intervalSize]
            resultAmplitudes.append(method(currentInterval))
            resultFrequencies.append(np.mean(frequencies[i:i+intervalSize]))

        return resultFrequencies, resultAmplitudes

    def __getCompressedSpectra(self, inputfrequencies, inputamplitudes, intervalSize=10, compressionMethodString="maxMedianDifference"):
        amplitudes = []
        frequencies = []
        for amp in inputamplitudes:
            frequencies, amplitude = self.__compressSpectrum(inputfrequencies, amp, intervalSize, compressionMethodString)
            amplitudes.append(amplitude)
        return frequencies, amplitudes

    def __median(self, amplitudes):
        return np.median(amplitudes)

    def __mean(self, amplitudes):
        return np.mean(amplitudes)

    def __maxMeanDifference(self, amplitudes):
        return np.amax(amplitudes)-np.mean(amplitudes)

    def __maxMedianDifference(self, amplitudes):
        return np.amax(amplitudes)-np.median(amplitudes)

    def __narrowFrequencyAmplitudes(self):
        self.narrowFrequencies, self.narrowAmplitudes = self.__getNarrowSpectra(self.amplitudes, self.frequencies, intervalSize, compressionMethodString)

    def __compressFrequencyAmplitudes(self, intervalSize=10, compressionMethodString="maxMedianDifference"):
        frequencies, amplitudes = self.__getNarrowSpectra(self.frequencies, self.amplitudes)
        self.compressedNarrowFrequencies, self.compressedNarrowAmplitudes = self.__getCompressedSpectra(frequencies, amplitudes, intervalSize, compressionMethodString)

    def __compressNarrowFrequencyAmplitudes(self, intervalSize=10, compressionMethodString="maxMedianDifference"):
        self.compressedNarrowFrequencies, self.compressedNarrowAmplitudes = self.__getCompressedSpectra(self.narrowFrequencies, self.narrowAmplitudes, intervalSize, compressionMethodString)


    # Plotting functions
    def plotNarrowFourierTransforms(self):
        self.__requireNarrowData()
        for i in range(len(self.narrowAmplitudes)):
            plt.plot(self.narrowFrequencies, self.narrowAmplitudes[i])
        plt.show()

    def saveFourierTransformPlots(self):
        self.__requireNarrowData()
        times = self.getTimes()
        for i in range(len(self.intervals)):
            plt.plot(self.frequencies, self.intervals[i][1])
            plt.savefig('img/fourier/fourier_' + str(times[i]) + '_seconds.png', bbox_inches='tight', dpi=400)
            plt.close()

    def plot2DWaterfallPlot(self, start=0.4, end=0.6, mode="disp", color1name="black", color2name="white"):
        self.__requireCompressedNarrowData()

        color1 = self.colors.get(color1name, (0,0,0))
        color2 = self.colors.get(color2name, (1,1,1))

        times = np.array(self.getTimes())
        amplitudes = np.array(self.compressedNarrowAmplitudes)
        frequencies = np.array(self.compressedNarrowFrequencies)

        freqGrid, timeGrid = np.meshgrid(frequencies, times)
        amplitudes = amplitudes[:-1, :-1]


        position=[0, start, end, 1]
        colors = [color1, color1, color2, color2]
        my_cmap = self.make_cmap(colors, position=position)

        a_min, a_max = -np.abs(amplitudes).max(), np.abs(amplitudes).max()

        ax = plt.subplot(1,1,1)
        plt.pcolormesh(frequencies, times, amplitudes, cmap=my_cmap, vmin=a_min, vmax=a_max)

        plt.axis([frequencies.min(), frequencies.max(), times.min(), times.max()])
        cbar = plt.colorbar()

        plt.title("2D waterfall plot")
        cbar.set_label("relative intensity (-)")
        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Time (sec)')

        if (mode == "disp"):
            plt.show()
        else:
            plt.savefig("img/waterfallPlots/waterfallPlot2D_"+color1name+"_"+color2name+"_"+str(start)+"_"+str(end)+".png", bbox_inches='tight', dpi=300)
        plt.close()

    def saveAll2DWaterfallPlots(self):
        self.__requireCompressedNarrowData()

        times = np.array(self.getTimes())
        amplitudes = np.array(self.compressedNarrowAmplitudes)
        frequencies = np.array(self.compressedNarrowFrequencies)

        freqGrid, timeGrid = np.meshgrid(frequencies, times)
        amplitudes = amplitudes[:-1, :-1]

        for color1name in self.colors:
            for color2name in self.colors:
                if (color1name is not color2name):
                    for start in np.arange(0.3, 0.7, 0.05):
                        for end in np.arange(start, 0.75, 0.05):
                            color1 = self.colors.get(color1name, (0,0,0))
                            color2 = self.colors.get(color2name, (1,1,1))
                            position=[0, start, end, 1]
                            colors = [color1, color1, color2, color2]
                            my_cmap = self.make_cmap(colors, position=position)

                            a_min, a_max = -np.abs(amplitudes).max(), np.abs(amplitudes).max()

                            ax = plt.subplot(1,1,1)
                            plt.pcolormesh(frequencies, times, amplitudes, cmap=my_cmap, vmin=a_min, vmax=a_max)

                            plt.axis([frequencies.min(), frequencies.max(), times.min(), times.max()])
                            cbar = plt.colorbar()

                            plt.title("2D waterfall plot")
                            cbar.set_label("relative intensity (-)")
                            ax.set_xlabel('Frequency (Hz)')
                            ax.set_ylabel('Time (sec)')
                            plt.savefig("img/waterfallPlots/waterfallPlot2D_"+color1name+"_"+color2name+"_"+str(start)+"_"+str(end)+".png", bbox_inches='tight', dpi=300)
                            plt.close()
    
    def plot3DWaterfallPlot(self):
        self.__requireCompressedNarrowData()

        tt = self.getTimes()
        ff = self.compressedNarrowFrequencies
        aa = self.compressedNarrowAmplitudes

        fig=plt.figure(1)

        ax=fig.add_subplot(1,1,1,projection='3d')

        X,Y=meshgrid(ff,tt)
        p = ax.plot_surface(X, Y, aa, rstride=4, cstride=4, cmap=cm.coolwarm, linewidth=0, antialiased=False)

        ax.view_init(elev=45, azim=-100)

        ax.set_xlabel('Frequency (Hz)')
        ax.set_ylabel('Time (sec)')
        ax.set_zlabel('Magnitude')
        
        plt.show() 
        
    def make_cmap(self, colors, position=None, bit=False):
        '''
        make_cmap takes a list of tuples which contain RGB values. The RGB
        values may either be in 8-bit [0 to 255] (in which bit must be set to
        True when called) or arithmetic [0 to 1] (default). make_cmap returns
        a cmap with equally spaced colors.
        Arrange your tuples so that the first color is the lowest value for the
        colorbar and the last is the highest.
        position contains values from 0 to 1 to dictate the location of each color.
        '''
        import matplotlib as mpl
        import numpy as np
        bit_rgb = np.linspace(0,1,256)
        if position == None:
            position = np.linspace(0,1,len(colors))
        else:
            if len(position) != len(colors):
                sys.exit("position length must be the same as colors")
            elif position[0] != 0 or position[-1] != 1:
                sys.exit("position must start with 0 and end with 1")
        if bit:
            for i in range(len(colors)):
                colors[i] = (bit_rgb[colors[i][0]],
                             bit_rgb[colors[i][1]],
                             bit_rgb[colors[i][2]])
        cdict = {'red':[], 'green':[], 'blue':[]}
        for pos, color in zip(position, colors):
            cdict['red'].append((pos, color[0], color[0]))
            cdict['green'].append((pos, color[1], color[1]))
            cdict['blue'].append((pos, color[2], color[2]))

        cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
        return cmap

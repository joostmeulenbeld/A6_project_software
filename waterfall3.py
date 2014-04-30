#   waterfall_FFT_plots         
#
from wavReadFourier import wavReaderFourierTransformer as wrft
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


wavFileName = "Delfi-n3xt.wav"	# the location of the wav file
start = 60*10.0					# What time is the first interval in seconds
end = 60*11.001					# What time is the last interval in seconds
intervalWidth = 1.0				# How many seconds is one interval
intervalStartFrequency = 60.0	# Every this many seconds a new interval starts

wavReader = wrft(wavFileName, start, end, intervalWidth, intervalStartFrequency)
frequencies, intervals = wavReader.getFrequencyAmplitudes()

aa=wavReader.getAmplitudes()
tt=wavReader.getTimes()
ff=wavReader.getFrequencies()


def  waterfallplot(freq_p,time_a,store_p): 
    from matplotlib import cm  
    from numpy import meshgrid  
    from mpl_toolkits.mplot3d import Axes3D
       
    fig=plt.figure(3)

    X,Y = meshgrid(store_p,freq_p)

    ax = fig.gca(projection='3d')
        
    surf = ax.plot_surface(X, Y, time_a,rstride=1, cstride=1, cmap=cm.jet,
            linewidth=0, antialiased=False)



    ax.view_init(elev=45, azim=-100)

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Time (sec)')
    ax.set_zlabel('Magnitude')
    #plt.ioff()
    
    plt.show() 
    
waterfallplot(ff,tt,aa)
    
#  




wav_file = 'D:\Delfi-n3Xt.wav';
[y,fs] = wavread(wav_file,[1 100]);

L=y(:,1);
R=y(:,2);
C=complex(R,L);
disp(fs)
F=fft(C,50)
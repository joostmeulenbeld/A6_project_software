import wave,binascii

flag=1
start=0
end=4;
n=10;
templ=[]
tempr=[]
final= [[0 for i in range(2)] for j in range(10)]

raw=wave.open('sample.wav','rb')
d=raw.getparams()
f=raw.readframes(n)

for i in range(0,n):
    l=''
    r=''
    for j in range(start,end):
        c=len(f[j])
        if c==1:
            if flag==1:
                l=l+binascii.hexlify(f[j])
                flag=flag*-1
            else:
                r=r+binascii.hexlify(f[j])
                flag=flag*-1
    start=start+4
    end=end+4
    final[i][0]=l
    final[i][1]=r

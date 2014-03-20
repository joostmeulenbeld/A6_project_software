import wave,binascii

flag=1
start=0
increment=6
end=increment;
frames=10;
final= [[0 for i in range(2)] for j in range(frames)]

raw=wave.open('Delfi-n3xt.wav','rb')
d=raw.getparams()
f=raw.readframes(frames)

for i in range(0,frames):
    l=''
    r=''
    for j in range(start,end):
        c=len(f[j])
        if c==1:
            if flag==1:
                l=l+binascii.hexlify(f[j])
                flag=flag*-1;
            else:
                r=r+binascii.hexlify(f[j])
                flag=flag*-1;
        if c==2:
            if flag==1:
                l=l+binascii.hexlify(l+f[j])
                count=len(l)
                temp1=''
                temp2=''
                for k in range(0,count-2):
                    temp1=temp1+l[k]
                temp2=temp2+l[count-2]
                temp2=temp2+l[count-1]
                l=temp1
                r=r+binascii.hexlify(r+temp2)
            else:
                r=r+binascii.hexlify(r+f[j])
                count=len(r)
                temp1=''
                temp2=''
                for k in range(0,count-2):
                    temp1=temp1+r[k]
                temp2=temp2+l[count-2]
                temp2=temp2+l[count-1]
                r=temp1
                l=l+binascii.hexlify(l+temp2) 
    start=start+increment
    end=end+increment
    final[i][0]=int(l,16)
    final[i][1]=int(r,16)
    
    
            

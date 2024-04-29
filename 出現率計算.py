import random
n=int(input())
k=int(input())
l=int(input())
d=0
e=0
f=0

for i in range(n):
    a=random.randint(k,l)
    b=random.randint(k,l)
    c=random.randint(k,l)
    print(a,b,c)
    if a==b==c:
        d+=1
        print("ゾロ目")
    elif a==b or b==c or a==c:
        e+=1
        print("リーチ")
    else:
        f+=1
        print("ノー点")
        
g=d/n
h=e/n
j=f/n

print("ゾロ目回数"+str(d)+"出現率"+str(g))
print("リーチ回数"+str(e)+"出現率"+str(h))
print("ノー点回数"+str(f)+"出現率"+str(j))
#list
a=[9,2,4,1,0,6,7,9]
for i in range(len(a)):
    for j in range(i+1,len(a)):
        if a[i]<a[j]:
            a[i],a[j]=a[j],a[i]
print("descending order is:",a)
# for i in range(20):
#     if (i+1)%3 == 0 or i == 19:
#         print(i)
#     else :
#         print(f"----{i}------")

test = ["123","12","123","123","123"]
print(len(test))
for i in range(len(test)):
    if (i+1)%3 == 0 or i == len(test)-1:
        print(str(i)+"넣는다"+ test[i])
    else :
        print(f"----{i}------" + test[i])

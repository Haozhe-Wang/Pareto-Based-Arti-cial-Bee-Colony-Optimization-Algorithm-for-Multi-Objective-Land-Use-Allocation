import os
sum=0
for file in os.listdir(".\\"):
    if file.endswith(".py"):
        with open(file,"r",encoding="UTF-8") as f:
            for i in f:
                sum+=1
print("Totall lines: %d"%sum)
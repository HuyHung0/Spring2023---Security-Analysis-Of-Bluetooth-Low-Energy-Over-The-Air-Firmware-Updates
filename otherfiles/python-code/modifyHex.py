
with open("python-code/app.dat", "rb") as f:
    data = f.read()
    #print(data)
    print(data.hex())
    print((data[:10]).hex())


with open('python-code/corrupted_appv2.dat','wb') as f:
    newdata = data[:10]+b'\x02'+data[11:]
    print(newdata.hex())
    f.write(newdata)
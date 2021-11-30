with open("data_subscale_11_20_launch1.csv",'r') as f:
    data = f.readlines()
    altdata = []
    #print(str(data[1]).split(',')[-2])
    data.pop(0)
    
    for line in data:
            split_data = str(line).split(',')
            if len(split_data) >= 3:
                altdata.append(float(split_data[-2]))
            #print(line)
            #altdata.append(str(line).split(',')[-2])
    print(max(altdata))
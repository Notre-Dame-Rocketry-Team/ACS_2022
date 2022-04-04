with open("data_fullscale_20220301_01.csv",'r') as f:
    data = f.readlines()
    altdata = []
    #print(str(data[1]).split(',')[-2])
    data.pop(0)
    
    for line in data:
            split_data = str(line).split(',')
            if len(split_data) >= 7:
                altdata.append(float(split_data[13]))
            #print(line)
            #altdata.append(str(line).split(',')[-2])
    print(f"Maximum Kalman Altitude (Apogee) = {max(altdata)}m = {max(altdata) * 3.28084}ft.")
    

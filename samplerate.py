import sys

with open(sys.argv[1],'r') as f:
    data = f.readlines()
    time = []
    #print(str(data[1]).split(',')[-2])
    data.pop(0)
    
    for line in data:
            split_data = str(line).split(',')
            if len(split_data) >= 3:
                time.append(float(split_data[0]))
            #print(line)
            #altdata.append(str(line).split(',')[-2])
    print(len(time)/(time[-1]-time[0]))

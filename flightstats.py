import sys

with open(sys.argv[1],'r') as f:
    data = f.readlines()
    altdata = []
    time = []
    data.pop(0)
    
    for line in data:
            split_data = str(line).split(',')
            if len(split_data) >= 3:
                altdata.append(float(split_data[-2]))
                time.append(float(split_data[0]))
    print("=================================================")
    print("             FLIGHT STATISTICS                   ")
    print("=================================================")
    print() 
    print(f"Max Altitude (Apogee) = {max(altdata):.3f} m = {max(altdata)*3.28084:.3f} ft")
    print(f"Sample Count = {len(time)}")
    print(f"Sample Rate = {len(time)/(time[-1]-time[0]):.3f} Hz")
    print()


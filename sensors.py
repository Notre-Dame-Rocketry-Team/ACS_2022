import analogio
import board

def init_sensors():
    x_axis = analogio.AnalogIn(board.A1)
    y_axis = analogio.AnalogIn(board.A2)
    z_axis = analogio.AnalogIn(board.A3)
    valtuple = (x_axis, y_axis, z_axis)
    x_name = "Acceleometer X acceleration:"
    y_name = "Acceleometer Y acceleration:"
    z_name = "Acceleometer Z acceleration:"
    nametuple = (x_name, y_name, z_name)
    return valtuple, nametuple

def read_sensors(valtuple):
    new_tuple = ()
    for val in valtuple: 
         # Convert axis value to float within 0...1 range.
        new_value = val / 65535
        # Shift values to true center (0.5).
        new_value -= 0.5
        # Convert to gravities.
        new_value = new_value * 3.0
        new_tuple.append(new_value)
    acc_x = new_tuple[0] #units: g
    acc_y = new_tuple[1] #units: g
    acc_z = new_tuple[2] #units: g
    return acc_x, acc_y, acc_z

    













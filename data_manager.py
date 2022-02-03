"""
This is an abstract-ish class which defines an interface
for working with the data.
"""

class Data:
    def __init__(self, name):
        self.name = name
        self.value = None

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def set_value(self, value):
        self.value = value

    def get_field_names(self):
        return [self.name]

    def get_value_list(self):
        return [self.value]

class Scalar_Data(Data):
    def __init__(self, name):
        super().__init__(name)
        self.value = 0

class Tuple_Data(Data):
    def __init__(self, name, num_vals=['x','y','z']):
        super().__init__(name)
        self.num_vals = num_vals
        self.value = [0 for i in num_vals]

    def set_dict_value(self, value):
        self.value = [value[i] for i in self.num_vals]

    def get_field_names(self):
        return [f'{self.name}_{i}' for i in self.num_vals]

    def get_value_list(self):
        return self.value


class Data_Manager:
    def __init__(self, active_sensors):
        self.data = {}
        self.active_sensors = active_sensors

    def add_data(self, data_obj):
        """
        Adds a field with a given name.
        """
        self.data[data_obj.get_name()] = data_obj

    def update_field(self, name, value):
        """
        Updates the value of a given field
        """
        self.data[name].set_value(value)

    def read_field(self, name):
        """
        Returns the value for a given key
        """
        return self.data[name]

    def update_dict_field(self, name, value):
        """
        Updates the value of a given field
        """
        self.data[name].set_dict_value(value)

    def get_field_names(self):
        """
        Returns a list of the flattened field names
        """
        return [i for j in self.data.values() for i in j.get_field_names()]

    def get_field_values(self):
        """
        Returns a list of data
        """
        return [i for j in self.data.values() for i in j.get_value_list()]

#Module: advanced Python
#Assignment #5 (October 18, 2021)
#
#--- Specifications
#- the class name must be VoltageData
#- the class must be initialized with two generic iterables of the same length
#  holding the numerical values of times and voltages
#- alternatively the class can be initialized from a text file
#- the class must expose two attributes: 'times' and 'voltages', each returning
#  a numpy array of type numpy.float64 of the corresponding quantity.
#- the values should be accessible with the familiar square parenthesis syntax:
#  the first index must refer to the entry, the second selects time (0) or
#  voltage (1). Slicing must also work.
#- calling the len() function on a class instance must return the number of
#  entries
#- the class must be iterable: at each iteration, a numpy array of two
#  values (time and voltage) corresponding to an entry in the file must be
#  returned
#- the print() function must work on class instances. The output must show one
#  entry (time and voltage), as well as the entry index, per line.
#- the class must also have a debug representation, printing just the values
#  row by row
#- the class must be callable, returning an interpolated value of the tension
#  at a given time
#- the class must have a plot() method that plots data using matplotlib.
#  The plot function must accept an 'ax' argument, so that the user can select
#  the axes where the plot is added (with a new figure as default). The user
#  must also be able to pass other plot options as usual
#- [optional] support a third optional column for the voltage errors
#- [optional] rewrite the run_tests() function in sandbox/test_voltage_data.py
#  as a sequence of proper UnitTests

""" Goal:
Write a class to handle a sequence of voltage measurements at different times.
"""

import numpy
from scipy import interpolate
from matplotlib import pyplot as plt

class VoltageData:
    """Class for handling a sequence of voltage measurments taken at
    different times
    """

    def __init__(self, times, voltages, d_voltages=None):
        """Class constructor. Times and voltages are iterables of same lenghts,
        the third column is optional
        """
        times = numpy.array(times, dtype=numpy.float64)
        voltages = numpy.array(voltages, dtype=numpy.float64)
        self.data = numpy.column_stack([times, voltages])
        if d_voltages is not None:
            d_voltages = numpy.array(d_voltages, dtype=numpy.float64)
            self.data = numpy.column_stack([times, voltages, d_voltages])
        self._spline = interpolate.InterpolatedUnivariateSpline(times,
                                                                voltages, w=d_voltages, k=3)

    @classmethod
    def from_file(cls, file_path):
        """Constructor from a file
        """
        columns = numpy.loadtxt(file_path, unpack=True)
        return cls(*columns)

    @property
    def times(self):
        """ Return the column of the times as numpy array
        """
        return self.data[:, 0]

    @property
    def voltages(self):
        """ Returns the column of voltages as numpy array
        """
        return self.data[:, 1]

    @property
    def d_voltages(self):
        """ Return the voltage errors as numpy errors only if they exists
        """
        try:
            return self.data[:, 2]
        except IndexError as exc:
            error_message = 'The optional column \'d_voltage\' is not present.'
            raise AttributeError(error_message) from exc

    def __len__(self):
        """Number of data points (or rows in the file, which is the same).
        """
        return len(self.data)

    def __getitem__(self, index):
        """ # We use composition and simply call __getitem__ from _data
        """
        return self.data[index]

    def __iter__(self):
        """Return the values row by row
        """
        for i in range(len(self)):
            yield self.data[i, :]

    def _str__(self):
        #output __str__=''
        #for row in enumerate(self):
            #line = f'(i) -> (row[0]:.1f), (row[1]: .2f)\n'
             #output_str += line
            #return output_str
        header = 'Row -> Time[s], Voltage [mV]\n'
        return header + '\n'.join([f'(i) -> {row[0]:.f}, {row[i]:.2f}'\
            for i, row in enumerate(self)])

    def __repr__(self):
        """
        """
        return '\n'.join([f'{row[0]} {row[1]} {row[2]})' for i, row in self])

    def __call__(self, voltages):
        """calla la spline
        """
        self._spline(voltages)

    def plot(self, a_x=None, draw_spline=False, **plot_opts):
        """Draw the data points.
        """
        if a_x is None:
            plt.figure('Voltage_vs_time')
        else:
            plt.sca(a_x)
        plt.errorbar(self.times, self.voltages, yerr=self.d_voltages, label='Data', **plot_opts)
        if draw_spline is True:
            x_v = numpy.linspace(min(self.times), max(self.times), 100)
            plt.plot(x_v, self(x_v), '-', label='Spline')
        plt.xlabel('T [s]')
        plt.ylabel('Voltage [mV]')
        plt.legend()
        plt.grid(True)


if __name__ == '__main__':

    T, V, DV = numpy.loadtxt('sample_data_file.txt', unpack=True)
    VDATA = VoltageData(T, V, DV)

    VDATA.plot(marker='o', linestyle='--', color='k', draw_spline=True)
    plt.show()

from email.utils import localtime
from scipy import interpolate
import time
from stepper import Stepper
		

az_motor = Stepper()
el_motor = Stepper()
	
def interpolate_pos_data(orig_arr):
	return interpolate.interp1d(orig_arr)

def main():
	positions = [...] #2d array [3 columns] (t, az, el) of positions during pass
	az_func = interpolate.interp1d(positions[:, [0,1]], kind='cubic')
	el_func = interpolate.interp1d(positions[:, [0,2]], kind='cubic')
	
	while(time.localtime() < positions[-1,0]):
		az_motor.moveTo(az_func(time.localtime()))
		el_motor.moveTo(el_func(time.localtime()))
import time
import logging
import os

LOG_FOLDER = '/home/pi/scripts/'

logging.basicConfig(filename='{}temperature.log'.format(LOG_FOLDER), filemode='a', format='%(created)f %(message)s', level=logging.INFO) 


def measure_temp(cmd):
    temp = os.popen(cmd).readline()
    if 'temp' in temp:
       return (temp.replace("temp=",""))
    return temp

if __name__ == '__main__':
    cpu = float(measure_temp("echo $(cat /sys/class/thermal/thermal_zone0/temp)")) / 1000
    cpu = '{0:.1f}'.format(cpu)
    gpu = measure_temp("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    gpu = '{0:.1f}'.format(float(gpu))

    logging.info('CPU_temp={} C and GPU_temp={} C'.format(cpu, gpu)) 

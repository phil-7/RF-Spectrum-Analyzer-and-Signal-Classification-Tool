import numpy as np

from math import pi, cos, sin
import sys
import wave

MODULATION = ("AM", "FM", "QPSK", "BPSK")

def main():
    
    # Check user inputs corrent CLI arguments and unpack results into  appropriate varibales
    file_name, mod_type, fs, duration, snr_db, freq_offset, symbol_rate, amplitude, bw = check_cli()
    
    samples = int(fs * duration)
    Ts = 1 / fs
    t = np.arange(samples) * Ts
    
    f_carrier = fs / 4.0
    f_message = symbol_rate / 2.0
    m = .5
    beta = symbol_rate / 2.0
    
    if mod_type == "AM":
        signal = amplitude * (1 + m * cos(2*pi * f_message * t)) * cos(2*pi * f_carrier * t)
    elif mod_type == "FM":
        signal = amplitude * cos(2*pi * f_carrier * t + beta * sin(2*pi * f_message * t))


            
            
def check_cli():
    # Check to make sure user inputs correct amount of arguments
    if len(sys.argv) < 5:
        sys.exit("Not enough arguments")
    if len(sys.argv) > 11:
        sys.exit("Too many arguments")

    # Check check filename validity
    file_name = sys.argv[1]
    if file_name.endswith(".wav") == False:
        sys.exit("File name must end with .wav")
    
    # Check mod_type validity
    mod_type = sys.argv[2].upper()
    if mod_type not in MODULATION:
        sys.exit("Enter valid Modulation")
    
    # Check Fs validity
    try:    
        fs = float(sys.argv[3])
    except ValueError:
        sys.exit("Sample frequency must be a number")
    
    if fs <= 0:
        sys.exit("Sample Frequency must be a positive number")
    
    # Check duration validity
    try:    
        duration = float(sys.argv[4])
    except ValueError:
        sys.exit("Duration must be a number")
    
    if duration <= 0:
        sys.exit("Duration must be a positive number")
        
    
    # Check snr_db validity  
    no_snr = False    
    try:
        snr_db = sys.argv[5]
    except IndexError:
        no_snr = True
        pass

    if no_snr:
        snr_db = 30.0
    else:
        try:
            snr_db = float(snr_db)
        except ValueError:
            sys.exit("SNR must be a number")

    # Check freq_offset validity
    no_freq_offset = False    
    try:
        freq_offset = sys.argv[6]
    except IndexError:
        no_freq_offset = True
        pass

    if no_freq_offset:
        freq_offset = 0.0
    else:
        try:
            freq_offset = float(freq_offset)
        except ValueError:
            sys.exit("Frequency Offset must be a number")
    
    if freq_offset >= fs/2.0:
        sys.exit("Freq Offset is too high. Decrease freq_offset or increase fs")
    
    # Check symbole_rate validity
    no_symbol_rate = False    
    try:
        symbol_rate = sys.argv[7]
    except IndexError:
        no_symbol_rate = True
        pass

    if no_symbol_rate:
        symbol_rate = fs/10.0
    else:
        try:
            symbol_rate = float(symbol_rate)
            if symbol_rate >= fs/2.0:
                sys.exit("Symbol Rate too high. Increase fs or decrease symbol_rate")
        except ValueError:
            sys.exit("Symbol Rate must be a number")
    
    
    # Check amplitude validity
    no_amplitude = False    
    try:
        amplitude = sys.argv[8]
    except IndexError:
        no_amplitude = True
        pass

    if no_amplitude:
        amplitude = 1.0
    else:
        try:
            amplitude = float(amplitude)
        except ValueError:
            sys.exit("Amplitude must be a number")
    if -1.0 <= amplitude <= 1.0:
        pass
    else:
        sys.exit("Amplitude needs be within [-1, 1]")
    
    # Check bandwidth validity
    no_bw = False    
    try:
        bw = sys.argv[9]
    except IndexError:
        no_bw = True
        pass

    if no_bw:
        if mod_type in ["QPSK", "BPSK"]:
            bw = symbol_rate * 1.2
        elif mod_type == "AM":
            bw = 2.0 * symbol_rate
        else:
            bw = 2.0 * (freq_offset + symbol_rate)
    else:
        try:
            bw = float(bw)
        except ValueError:
            sys.exit("Bandwidth must be a number")
    
    
            
    return file_name, mod_type, fs, duration, snr_db, freq_offset, symbol_rate, amplitude, bw

if __name__ == "__main__":
    main()
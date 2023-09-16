import pandas as pd
import numpy as np
from os import listdir
from typing import Union

decode_line = lambda lin: [x.strip() for x in lin.decode(errors='ignore').split('\t')]

BIN_HEADERS = ['<0.523', '0.542', '0.583', '0.626', '0.673', '0.723', '0.777', '0.835',
       '0.898', '0.965', '1.037', '1.114', '1.197', '1.286', '1.382', '1.486',
       '1.596', '1.715', '1.843', '1.981', '2.129', '2.288', '2.458', '2.642',
       '2.839', '3.051', '3.278', '3.523', '3.786', '4.068', '4.371', '4.698',
       '5.048', '5.425', '5.829', '6.264', '6.732', '7.234', '7.774', '8.354',
       '8.977', '9.647', '10.37', '11.14', '11.97', '12.86', '13.82', '14.86',
       '15.96', '17.15', '18.43', '19.81']

APS_BIN_MIDPOINTS = np.array([np.sqrt(.487 * .523), 0.542, 0.583, 0.626, 0.673, 0.723, 0.777, 0.835, 0.898, 0.965, 1.037, 1.114, 1.197, 1.286, 1.382, 1.486, 1.596,
1.715, 1.843, 1.981, 2.129, 2.288, 2.458, 2.642, 2.839, 3.051, 3.278, 3.523, 3.786, 4.068, 4.371, 4.698, 5.048, 5.425, 5.829, 6.264, 6.732, 
7.234, 7.774, 8.354, 8.977, 9.647, 10.37, 11.14, 11.97, 12.86, 13.82, 14.86, 15.96, 17.15, 18.43, 19.81 ])
APS_BIN_BOUNDS = np.array([.487, .523] + np.sqrt(APS_BIN_MIDPOINTS[2:] * APS_BIN_MIDPOINTS[1:-1]).tolist())
APS_DLOGDP = np.log10(APS_BIN_BOUNDS[1:]) - np.log10(APS_BIN_BOUNDS[:-1])

FLOAT_HEADERS = ['Inlet Pressure', 'Total Flow', 'Sheath Flow', 'Analog Input Voltage 0',
       'Analog Input Voltage 1', 'Digital Input Level 0',
       'Digital Input Level 1', 'Digital Input Level 2', 'Laser Power',
       'Laser Current', 'Sheath Pump Voltage', 'Total Pump Voltage',
       'Box Temperature', 'Avalanch Photo Diode Temperature',
       'Avalanch Photo Diode Voltage', 'Median(m)', 'Mean(m)',
       'Geo. Mean(m)', 'Mode(m)', 'Geo. Std. Dev.', 'Total Conc.(#/cm)'] + BIN_HEADERS

def _read_APS_text_file(path_to_file: str):
    # Read in file as raw bytes
    with open(path_to_file,'rb') as f:
        l = f.readlines()

    # First 6 lines aren't necessary
    l = l[6:]

    headers = decode_line(l[0])
    data = [decode_line(l) for l in l[1:] if (b'\t' in l and len(l.split(b'\t')) > 2 and b'<' not in l)]

    df = pd.DataFrame(data=data,columns=headers)

    bins = headers[4:56]
    df[bins] = df[bins].astype(float)
    df['bins'] = [r for r in df[bins].values.astype('float')]

    df['Total Conc.'] = df['Total Conc.'].apply(lambda st: st.split("(")[0]).apply(float)

    df['datetime'] = pd.to_datetime(df['Date'] + " " + df['Start Time'], format="%m/%d/%y %H:%M:%S")
    df.set_index('datetime', drop=True, inplace=True)

    return df

def _read_APS_text_file_2(filepath: str):
    with open(filepath, 'rb') as f:
        lines = f.readlines()
    stuff = []
    for l in lines:
        split_l = l.split(b'\t')
        if len(split_l) > 2:
            stuff.append(split_l)

    stuff = [[t.decode(errors='ignore').strip() for t in l] for l in stuff]
    stuff = dict(zip([x[0] for x in stuff], [x[1:] for x in stuff]))

    df = pd.DataFrame(data=stuff)

    df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Start Time'], format="%m/%d/%y %H:%M:%S")

    df.set_index('datetime', inplace=True)

    bins = df.columns[4:56]
    df[bins] = df[bins].astype(float)
    

    return df

def read_APS_file(filepath: str) -> Union[pd.DataFrame, None]:
    """
    Read an APS file [.txt format] and return as pandas.DataFrame.

    Args:
    * filepath (str): The path to the APS .txt file, can be relative or full.

    Returns:
    * pandas.DataFrame - if successful
    * None - otherwise
    """
    _df = None
    try:
        _df = _read_APS_text_file(filepath)
    except Exception as e:
        pass
    if _df is None:
        try:
            _df = _read_APS_text_file_2(filepath)
        except Exception as e:
            pass

    try:
        _df[FLOAT_HEADERS] = _df[FLOAT_HEADERS].astype(float, errors='ignore')
    except Exception as e:
        pass

    try:
        _df['bins'] = [r for r in _df[BIN_HEADERS].values.astype('float')]
    except Exception as e:
        pass

    return _df

    

def read_folder_APS(path_to_folder: str, file_suffix: str = ".txt") -> Union[pd.DataFrame, None]:
    """
    Read all APS files [.txt or otherwise specified suffix] in a given folder and return all data as a pandas.DataFrame.
    
    Args:
    * path_to_folder (str): The path to the folder containing the files to be read. May be full or relative.
    * file_suffix (str): Defaults to `'.txt'`. The file suffix for the files to be grabbed.
    
    Returns:
    * pandas.DataFrame - if successful
    * None - otherwise
    """
    dfs = []
    for fp in listdir(path_to_folder):
        if not fp.endswith(file_suffix):
            continue

        full_fp = f"{path_to_folder.rstrip('/')}/{fp}"

        _df = read_APS_file(full_fp)

        if _df is None:
            continue
        dfs.append(_df)
    if not dfs:
        return None
    
    df = pd.concat(dfs)
    df.sort_index(inplace=True)

    return df
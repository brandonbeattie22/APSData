import pandas as pd
import numpy as np
from os import listdir
from typing import Union

decode_line = lambda lin: [x.strip() for x in lin.decode(errors='ignore').split('\t')]

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
    df['bins'] = [r for r in df[bins].values.astype('float')]

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
        return _read_APS_text_file(filepath)
    except Exception as e:
        pass
    if _df is None:
        try:
            return _read_APS_text_file_2(filepath)
        except Exception as e:
            pass

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

        _df = None
        try:
            _df = _read_APS_text_file(full_fp)
        except Exception as e:
            pass
        if _df is None:
            try:
                _df = _read_APS_text_file_2(full_fp)
            except Exception as e:
                pass
        if _df is None:
            continue

        dfs.append(_df)
    if not dfs:
        return None
    
    df = pd.concat(dfs)
    df.sort_index(inplace=True)

    return df
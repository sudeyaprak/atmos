import numpy as np

def atmos(doy, trec, trecw, C1, rec, sp3, alpha, beta):
    """
    Main function for calculating atmospheric parameters.

    Parameters:
        doy (int): Day of year.
        trec (float): Receiver time in seconds.
        trecw (float): Receiver time for weather model in seconds.
        C1 (float): C1 pseudorange measurement.
        rec (numpy.ndarray): Receiver position in XYZ coordinates.
        sp3 (numpy.ndarray): Array containing satellite information.
        alpha (numpy.ndarray): Array of ionospheric model coefficients alpha.
        beta (numpy.ndarray): Array of ionospheric model coefficients beta.

    Returns:
        az (float): Azimuth angle in degrees.
        zen (float): Zenith angle in degrees.
        slantd (float): Slant distance in meters.
        dion (float): Ionospheric delay.
        TrD (float): Tropospheric dry delay.
        TrW (float): Tropospheric wet delay.
    """
    
    # Calculate satellite position
    fpos = sat_pos(trec, C1, sp3, rec)
    
    # Calculate local coordinates and atmospheric parameters
    az, zen, slantd = local(rec, fpos)
    azm = np.deg2rad(az)
    elv = np.deg2rad(zen)
    
    # Convert receiver coordinates to latitude, longitude, and height
    ellp = xyz2plh(rec)
    lat = np.deg2rad(ellp[0])
    lon = np.deg2rad(ellp[1])
    H = int(ellp[2])
    
    # Calculate ionospheric delay
    dion = Ion_Klobuchar(lat, lon, zen, az, alpha, beta, trecw)
    
    # Calculate tropospheric delays
    Trzd, Trzw, ME = trop_SPP(int(ellp[0]), doy, H, elv)
    
    # Apply mapping function to tropospheric delays
    TrD = Trzd * ME
    TrW = Trzw * ME
    
    return az, zen, slantd, dion, TrD, TrW

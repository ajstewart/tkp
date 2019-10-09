
import pandas as pd
from tkp.sourcefinder.utils import get_error_radius
import numpy as np
import random

class Selavy:
    
    def __init__(self, catalog_file):
        self.catalog_file = catalog_file
        self.df = pd.DataFrame()
        
        
    def read_catalog(self, remove_bad_sources=True, remove_islands=False, zero_rms_fill_val=0.034e-3):
        """
        Returns a pandas dataframe of the catalog.
        """
        with open(self.catalog_file, "r") as f:
            lines=f.readlines()
            
        columns=lines[0].split()[1:-1]
        data=[i.split() for i in lines[2:]]
    
        selavy=pd.DataFrame(data, columns=columns)
        
        if remove_bad_sources:
            selavy=selavy[selavy["flag_c4"].astype(int)==0].reset_index(drop=True)
            
        if remove_islands:
            selavy=selavy[selavy["has_siblings"].astype(int)==0].reset_index(drop=True)
        
        selavy.loc[ selavy.rms_image.astype(np.float)==0.0, "rms_image" ] =  zero_rms_fill_val
        selavy.loc[ selavy.flux_peak_err.astype(np.float)==0.0, "flux_peak_err" ] = selavy.loc[ selavy.flux_peak_err.astype(np.float)==0.0, "rms_image" ] 
        selavy.loc[ selavy.flux_int_err.astype(np.float)==0.0, "flux_int_err" ] = selavy.loc[ selavy.flux_peak_err.astype(np.float)==0.0, "rms_image" ] 
        
        self.df = selavy
        
        return selavy
        
        
    def serialize(self, ew_sys_err, ns_sys_err, wcs):
        if len(self.df.index) == 0:
            self.read_catalog()
        
        read_sources = []
        
        for i,row in self.df.iterrows():
            rndm = (random.randint(100000,999999)*1.e-9)
            read_sources.append([
                np.float(row["ra_deg_cont"]),
                np.float(row["dec_deg_cont"]),
                np.float(row["ra_err"])/3600.,
                np.float(row["dec_err"])/3600.,
                (np.float(row["flux_peak"])+rndm)/1.e3,
                (np.float(row["rms_image"])+rndm)/1.e3,
                (np.float(row["flux_int"])+rndm)/1.e3,
                (np.float(row["rms_image"])+rndm)/1.e3,
                (np.float(row["flux_peak"])+rndm)/(np.float(row["rms_image"])+rndm),
                np.float(row["maj_axis"])/2.,
                np.float(row["min_axis"])/2.,
                np.float(row["pos_ang"]),
                ew_sys_err,
                ns_sys_err,
                get_error_radius(wcs,np.float(row["ra_deg_cont"]), np.float(row["ra_err"])/3600.,np.float(row["dec_deg_cont"]),np.float(row["dec_err"])/3600.),
                True,
                np.float(row["chi_squared_fit"]),
                1.0,
            ])
            
        return read_sources
        
        
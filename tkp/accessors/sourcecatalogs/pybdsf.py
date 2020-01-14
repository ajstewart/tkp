
import pandas as pd
from tkp.sourcefinder.utils import get_error_radius
import numpy as np
import logging

logger = logging.getLogger(__name__)

class Pybdsf:
    
    def __init__(self, catalog_file):
        self.catalog_file = catalog_file
        self.df = pd.DataFrame()
        
        
    def read_catalog(self, remove_bad_sources=False, zero_rms_fill_val=0.034e-3):
        """
        Returns a pandas dataframe of the catalog.
        """
        pybdsf = pd.read_csv(self.catalog_file, skiprows=5, delimiter=", ", engine="python")
        
        pybdsf.rename(columns={"# Gaus_id":"Gaus_id"}, inplace=True)
        
        # To my knowledge pybdsf does not suffer from nan's, double sources, blanks like selavy
        # There is also no flag column for 'bad sources'
        # Hence no further filtering is needed.
        
        self.df = pybdsf
        
        return pybdsf
        
        
    def serialize(self, ew_sys_err, ns_sys_err, wcs):
        if len(self.df.index) == 0:
            self.read_catalog()
        
        read_sources = []
        
        for i,row in self.df.iterrows():
            read_sources.append([
                np.float(row["RA"]),
                np.float(row["DEC"]),
                np.float(row["E_RA"]),
                np.float(row["E_DEC"]),
                np.float(row["Peak_flux"]),
                np.float(row["E_Peak_flux"]),
                np.float(row["Total_flux"]),
                np.float(row["E_Total_flux"]),
                (np.float(row["Peak_flux"])/np.float(row["Resid_Isl_rms"])),
                np.float(row["Maj"])/2.,
                np.float(row["Min"])/2.,
                np.float(row["PA"]),
                ew_sys_err,
                ns_sys_err,
                get_error_radius(wcs,np.float(row["RA"]), np.float(row["E_RA"]),np.float(row["DEC"]),np.float(row["E_DEC"])),
                True,
                1.0,
                1.0,
            ])
            
        return read_sources
        
        
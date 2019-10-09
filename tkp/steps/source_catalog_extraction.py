import logging
from tkp.accessors import sourcefinder_image_from_accessor
from collections import namedtuple
from tkp.accessors.sourcecatalogs.selavy import Selavy

logger = logging.getLogger(__name__)


#Short-lived struct for returning results from the source extraction routine:
ExtractionResults = namedtuple('ExtractionResults',
                                   ['sources',
                                    'rms_min',
                                    'rms_max'])


def extract_sources(accessor, extraction_params):
    """
    Extract sources from an image catalog.

    args:
         images: a tuple of image DB object and accessor
        extraction_params: dictionary containing the settigns
        to find the associated catalogs defined by the user.
    returns:
        list of ExtractionResults named tuples containing source measurements,
        min RMS value and max RMS value
    """
    extension = extraction_params["catalogs_extension"]
    catalog_type = extraction_params["catalogs_format"]
    
    catalog_file = accessor.url+extension
    
    logger.debug("Reading sources from image {} using {} catalog {}".format(accessor, catalog_type, catalog_file))
    
    data_image = sourcefinder_image_from_accessor(accessor)
    
    # data_image._get_rm()

    # logger.debug("Employing margin: %s extraction radius: %s deblend_nthresh: %s",
    #              extraction_params['margin'],
    #              extraction_params['extraction_radius_pix'],
    #              extraction_params['deblend_nthresh']
    # )

    # "blind" extraction of sources
    # results = data_image.extract(
    #     det=extraction_params['detection_threshold'],
    #     anl=extraction_params['analysis_threshold'],
    #     deblend_nthresh=extraction_params['deblend_nthresh'],
    #     force_beam=extraction_params['force_beam']
    # )
    # logger.debug("Detected %d sources in image %s" % (len(results), accessor.url))
    
    if catalog_type.lower() == "selavy":
        the_catalog = Selavy(catalog_file)
        
    the_catalog.read_catalog(remove_islands=True)
    
    ew_sys_err = extraction_params['ew_sys_err']
    ns_sys_err = extraction_params['ns_sys_err']
    
    serialized = the_catalog.serialize(ew_sys_err, ns_sys_err, data_image.wcs)
    

    return ExtractionResults(sources=serialized,
                             rms_min=float(data_image.rmsmap.min()),
                             rms_max=float(data_image.rmsmap.max())
                             )




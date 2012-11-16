from tkp.database import DataBase, DataSet
import trap.quality
import trap.source_extraction
import trap.monitoringlist
import trap.persistence
import trap.transient_search
import trap.feature_extraction
import trap.classification
import trap.prettyprint
from lofarpipe.support.control import control

from images_to_process import images

#TODO: KeyError: 'dataset_id'

class TrapLocal(control):
    inputs = {}

    def pipeline_logic(self):
        quality_parset_file = self.task_definitions.get("quality_check", "parset")
        srcxtr_parset_file = self.task_definitions.get("source_extraction", "parset")
        transientsearch_file = self.task_definitions.get("transient_search", "parset")
        classification_file = self.task_definitions.get("classification", "parset")

        self.logger.info("creating dataset in database ...")
        dataset_id = trap.persistence.store(images, 'trap-local dev run')
        self.logger.info("added dataset with ID %s" % dataset_id)

        dataset = DataSet(id=dataset_id, database=DataBase())
        dataset.update_images()

        good_images = []
        for image in dataset.images:
            if trap.quality.noise(image.id, quality_parset_file):
                good_images.append(image)

        for image in good_images:
            trap.source_extraction.extract_sources(image.id, srcxtr_parset_file)

        # TODO: this should be updated to work on a list of images, not on a dataset ID
        trap.monitoringlist.mark_sources(dataset_id, srcxtr_parset_file)

        for image in good_images:
            trap.monitoringlist.update_monitoringlist(image.id)

        good_ids =[ i.id for i in good_images]
        transient_results = trap.transient_search.search_transients(good_ids, dataset_id,  transientsearch_file)

        transients = transient_results['transients']
        for transient in transients:
            trap.feature_extraction.extract_features(transient)
            trap.classification.classify(transient, classification_file)
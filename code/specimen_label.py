import cyrtranslit 
import logging
import extraction_helpers
import json


class SpecimenLabel:
    def __init__(self, verbatim, institution, genus, catalog_number, uuid, associated_media_uri):
        self.verbatim = verbatim
        self.translation = None

        self.label_lines = extraction_helpers.lines(verbatim)
        i, verbatim_id = extraction_helpers.verbatim_identification(self.label_lines, genus)

        if not verbatim_id:
            i, verbatim_id, genus = extraction_helpers.verbatim_identification_no_genus(self.label_lines)
        if i:
            self.label_lines = self.label_lines[i:]

        scientific_name = genus
        if verbatim_id:
            name_parts = verbatim_id.split(' ')
            if len(name_parts) > 1:
                scientific_name += ' ' + name_parts[1]
        
        elevation = extraction_helpers.elevation(self.label_lines)
        min, max = extraction_helpers.min_max_elevation_in_meters(elevation)

        self.dwc = {
            'institutionCode': institution,
            'catalognumber': catalog_number,
            'genus': genus,
            'occurrenceID': uuid,
            'associatedMedia': associated_media_uri,
            'verbatimIdentification': verbatim_id,
            'scientificName': scientific_name,
            'minimumElevationInMeters': min,
            'maximumElevationInMeters': max,
            'verbatimElevation': elevation,
            'recordNumber': extraction_helpers.record_number(self.label_lines),
            'year': extraction_helpers.year(self.label_lines),
            'dynamicProperties': {
                'verbatimTranscription': extraction_helpers.ipt_friendly_string(self.verbatim),
                'verbatimTransliteration': cyrtranslit.to_latin(extraction_helpers.ipt_friendly_string(self.verbatim), 'ru'),
            }   
        }

    def get_ipt_dwc(self):
        dwc = self.dwc
        dwc['dynamicProperties'] = json.dumps(self.dwc['dynamicProperties'], ensure_ascii=False).encode('utf8').decode()
        dwc['dynamicProperties'].replace('\n', '#')
        return dwc

    def fill_translated_fields(self, translated):
        self.translation = translated
        self.dwc['dynamicProperties']['verbatimTranslation'] = extraction_helpers.ipt_friendly_string(translated)
        self.dwc['recordedBy'] = extraction_helpers.names(extraction_helpers.lines(translated))
        self.dwc['country'] = extraction_helpers.country(extraction_helpers.lines(translated))

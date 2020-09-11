import logging
import xml.etree.ElementTree as ET

from Alma_Apis_Interface import Alma_Apis_Records, Alma_Sru
from Isbns import isbn

class Portfolio(object):
    """A set of function for interact with Alma Apis in area "Electronic"
    """

    def __init__(self, datas, apikey='',service='AlmaPy'):
        if apikey is None:
            raise Exception("Please supply an API key")
        self.apikey = apikey
        self.service = service
        self.logger = logging.getLogger(service)
        self.pf_id = datas['id']
        self.mms_id = datas['resource_metadata']['mms_id']['value']
        self.title = 'None'
        self.record_ids = 'None'
        self.publisher = 'None'
        self.date_of_publication = 'None'

        api = Alma_Apis_Records.AlmaRecords(apikey=self.apikey,region='EU',service=self.service)
        status,record = api.get_record(self.mms_id)
        if status == 'Success' :
            record_xml = ET.fromstring(record)
            self.record_ids = self.get_identifiers(record_xml)
            self.title = record_xml.find('title').text
            if (record_xml.find('publisher_const')) :
                self.publisher = record_xml.find('publisher_const').text
            if (record_xml.find('date_of_publication')) :
                self.date_of_publication = record_xml.find('date_of_publication').text
            self.originating_system_id = record_xml.find('originating_system_id').text


    def get_identifiers(self,record):
        dict_id = { 'e_isbn' : {
                                'field' : '020',
                                'subfield' : 'a',
                                'type' : 'online_identifier'
                                },
                    'e_issn' : {
                                'field' : '022',
                                'subfield' : 'a',
                                'type' : 'online_identifier'
                                },
                    'p_isbn' : {
                                'field' : '776',
                                'subfield' : 'z',
                                'type' : 'print_identifier'
                                },
                    'p_issn' : {
                                'field' : '776',
                                'subfield' : 'x',
                                'type' : 'print_identifier'
                                },
                    }
        record_ids_dict = { 'print_identifier' : [],
                            'online_identifier' : []
                            }
        for id_type in dict_id:
            if record.find("record/datafield[@tag='{}']/subfield[@code='{}']".format(dict_id[id_type]['field'],dict_id[id_type]['subfield'])) is not None :
                for bib_id in record.findall("record/datafield[@tag='{}']".format(dict_id[id_type]['field'])):
                    if bib_id.find("subfield[@code='{}']".format(dict_id[id_type]['subfield'])) is not None :
                        i = bib_id.find("subfield[@code='{}']".format(dict_id[id_type]['subfield'])).text
                        if id_type in ['p_isbn', 'e_isbn'] :
                            i = isbn.convert_10_to_13(i)
                        else :
                            i = i.replace('-','')
                        record_ids_dict[dict_id[id_type]['type']].append(i)
        return record_ids_dict

    def get_nz_mms_id(self):
        sru = Alma_Sru.AlmaSru(service=self.service, instance='Test')
        return sru.originatingSystemIdToMmsid(self.originating_system_id)
        



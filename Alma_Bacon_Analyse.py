#!/usr/bin/python3
# -*- coding: utf-8 -*-
# from Alma_Apis_Interface import Alma_Apis
from Alma_Apis_Interface import Alma_Apis_Ecollections, Alma_Apis
from Abes_Apis_Interface import Bacon_Id2Kabart
from Isbns import isbn
import xml.etree.ElementTree as ET
import json
import os
import Portfolio
import urllib.request
import pysftp

API_KEY = os.getenv("TEST_UB_API")
NZ_API_KEY = os.getenv("TEST_NETWORK_API")

ECOLLECTION_ID = '61154857880004672'
ESERVICE_ID = '62154857870004672'
BACON_PACKAGE = 'CAIRN_GLOBAL_OUVRAGES-EDUCATION'

REPORT_FILE = "/media/sf_Partage_LouxBox/{}_rapport.csv".format(BACON_PACKAGE)
LOADER_FILE = "/media/sf_Partage_LouxBox/{}_loader.tsv".format(BACON_PACKAGE)

IMPORT_JOB_ID = "S5952781050004671"


api = Alma_Apis_Ecollections.AlmaERecords(apikey=API_KEY, region='EU', service='Bacon_Alma_Analysis')

def incrementation(number):
    if number == 0 :
        number+=1;    
    number+=100;
    return number

def bacon_recovery(bib_id_dict) :
        bacon_matching = 'None'
        id_for_matching = 'None'
        ppn = 'None'
        title = 'None'
        publisher = 'None'
        online_date_pub = 'None'
        print_date_pub = 'None' 
        for id_type in ['online_identifier','print_identifier']:
            for bib_id in bib_id_dict['online_identifier'] :
                bacon_pk_info = Bacon_Id2Kabart.Bacon_Id2Kbart(bib_id)
                if bacon_pk_info.status == "Succes" :
                    bacon_matching = 'True'
                    id_for_matching = bib_id
                    ppn = bacon_pk_info.get_ppn()
                    title = bacon_pk_info.get_publication_title()
                    publisher = bacon_pk_info.get_publisher_name()
                    online_date_pub = bacon_pk_info.get_online_pubdate()
                    print_date_pub = bacon_pk_info.get_print_pubdate() 
                    return bacon_matching, id_type, id_for_matching, ppn, title, publisher, online_date_pub, print_date_pub
        return bacon_matching, id_type, id_for_matching, ppn, title, publisher, online_date_pub, print_date_pub
                

lf = open(LOADER_FILE, "w")
lf.write("001\t035$a\n")

rf = open(REPORT_FILE, "w")
rf.write("Alma MMS_ID\tAlma NZ_MMS_ID\tAlma Tire\tAlma Editeur\tAlma Date pub\tMatch dans Bacon\tType d'identifiant du matching\tIdentifiant du matching\tBacon PPN\tBacon Titre\tBacon Editeur\tBacon Date de pub.(online)\tBacon Date de pub.(print)\n")
# On checke si la collection et le service existe et on récupère le nombre de protfolios
status, pf_number = api.get_number_of_portfolios_for_eservice(ECOLLECTION_ID, ESERVICE_ID, accept='json')
# On défini le nombre d'appel à faire pour avoir la liste de tous les portfolios
offset = 0
while offset < pf_number:
# while offset < 1:
    status, pf_list = api.get_portfolios_list(ECOLLECTION_ID,ESERVICE_ID,limit=100,offset=offset)
    # print(pf_list)
    for pf in pf_list['portfolio']:
        # print(pf)
        portfolio = Portfolio.Portfolio(pf, apikey=API_KEY, service='Bacon_Alma_Analysis')
        nz_mms_id = portfolio.get_nz_mms_id()
        print("{} : {} --> {}".format(nz_mms_id,portfolio.title,portfolio.record_ids))
        bacon_matching, id_type, id_for_matching, ppn, title, publisher, online_date_pub, print_date_pub = bacon_recovery(portfolio.record_ids)
        if nz_mms_id != 'Ko' and ppn != 'None' :
            lf.write("{}\t(PPN){}\n".format(nz_mms_id,ppn))
        rf.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format( portfolio.mms_id,
                                                                                nz_mms_id,
                                                                                portfolio.title,
                                                                                portfolio.publisher,
                                                                                portfolio.date_of_publication,
                                                                                bacon_matching,
                                                                                id_type,
                                                                                id_for_matching,
                                                                                ppn,
                                                                                title, publisher, online_date_pub, print_date_pub))
        print ("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(bacon_matching, id_type, id_for_matching, ppn, title, publisher, online_date_pub, print_date_pub))
    offset = incrementation(offset)

lf.close()
rf.close()
print("{} - {} - {}".format(os.getenv("SFTP_UB_HOSTNAME"),os.getenv("SFTP_UB_LOGIN"),os.getenv("SFTP_UB_PW")))
with pysftp.Connection(host=os.getenv("SFTP_UB_HOSTNAME"), username=os.getenv("SFTP_UB_LOGIN"), password=os.getenv("SFTP_UB_PW")):
print() as sftp:
    print("Connection succesfully stablished ... ")
    localFilePath = LOADER_FILE
    # Define the remote path where the file will be uploaded
    remoteFilePath = '/DEPOT/NOTICES_MARC21/{}_loader.tsv'.format(BACON_PACKAGE)
    sftp.put(localFilePath, remoteFilePath)

job_api = Alma_Apis.Alma(apikey=NZ_API_KEY, region='EU', service='Bacon_Alma_Analysis')
job_api.post_job_without_data(IMPORT_JOB_ID)



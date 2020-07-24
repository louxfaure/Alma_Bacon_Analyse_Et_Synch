#!/usr/bin/python3
# -*- coding: utf-8 -*-
# from Alma_Apis_Interface import Alma_Apis
from Alma_Apis_Interface import Alma_Apis_Ecollections, Alma_Apis, Alma_Sru
from Abes_Apis_Interface import Bacon_Id2Kabart
import os
# for isbn in [9782296351004] :
#     bacon_pk_info = Bacon_Id2Kabart.Bacon_Id2Kbart(isbn)
#     print("{} : {} - {}".format(isbn, bacon_pk_info.status,bacon_pk_info.get_publication_title()))

# sru = Alma_Sru.AlmaSru("NETWORK")
# print(sru.originatingSystemIdToMmsid("2550000000098394"))
print(os.getenv("SFTP_UB_PW"))

import streamlit as st

import xml.etree.cElementTree as et
import pandas as pd

import xml.etree.ElementTree as ET
import logging
from .structure_data import (
    create_structured_dataframe,
    create_log_report,
    convert_df_to_csv,
    filter_df_by_unit,
    get_version_from_meta
)


class CdfToDf:
    logger = logging.getLogger(__name__)

    def convert(self, path):
        tree = et.parse(path)
        root = tree.getroot()

        # Here we will create a list of each variable/Feature which we want in CSV file
        SerialNumber = []
        ProductID = []
        ProductFamily = []
        Modality = []
        TimeStamp = []
        SecondTimeStamp = []
        SystemMode = []
        MachineName = []
        Description = []
        LogCategory = []
        InfoCategory = []
        EventCategory = []
        TimeFraction = []

        # We are using for loop to append each variable item to the list from XML
        for root1 in root.iter('MedicalSystem'):
            root2 = et.Element('root')
            root2 = root1
            for SystemConfiguration in root2.iter('SystemConfiguration'):
                root3 = et.Element('root')
                xml_serialNumber = SystemConfiguration.attrib['SerialNumber']
                xml_ProductID = SystemConfiguration.attrib['ProductID']
                xml_Modality = SystemConfiguration.attrib['Modality']
            for event in root2.iter('Event'):
                root4 = et.Element(root)
                xml_TimeStamp = event.attrib['TimeStamp']
                xml_TimeFraction = event.attrib['TimeFraction']
                xml_SecondTimeStamp = event.attrib['SecondTimeStamp']
                root4 = event
                for EventOriginatorInfo in root4.iter('EventOriginatorInfo'):
                    root5 = et.Element(root)
                    xml_SystemMode = EventOriginatorInfo.attrib['SystemMode']
                    xml_MachineName = EventOriginatorInfo.attrib['MachineName']
                for eventInfo in root4.iter('EventInfo'):
                    xml_Description = eventInfo.attrib['Description']
                    xml_LogCategory = eventInfo.attrib['LogCategory']
                    xml_InfoCategory = eventInfo.attrib['InfoCategory']
                    xml_EventCategory = eventInfo.attrib['EventCategory']
                    SerialNumber.append(xml_serialNumber)
                    ProductID.append(xml_ProductID)
                    Modality.append(xml_Modality)
                    TimeStamp.append(xml_TimeStamp)
                    SecondTimeStamp.append(xml_SecondTimeStamp)
                    SystemMode.append(xml_SystemMode)
                    MachineName.append(xml_MachineName)
                    Description.append(xml_Description)
                    LogCategory.append(xml_LogCategory)
                    InfoCategory.append(xml_InfoCategory)
                    EventCategory.append(xml_EventCategory)
                    TimeFraction.append(xml_TimeFraction)

        # Here we have created a Dictionary of lists
        data = {'SerialNumber': SerialNumber, 'ProductID': ProductID,
                'Modality': Modality, 'TimeStamp': TimeStamp,
                'TimeFraction': TimeFraction, 'SecondTimeStamp': SecondTimeStamp,
                'Description': Description, 'LogCategory': LogCategory,
                'InfoCategory': InfoCategory, 'EventCategory': EventCategory,
                'SystemMode': SystemMode, 'MachineName': MachineName,
                'FileName': path.filename, 'Unit': "STAND", 'Version': 1}

        # Converting Dictionary to Dataframe
        df = pd.DataFrame(data)
        return df

    def convert_all(self, filenames):
        data = {}
        final_data = []
        counter = 0

        done_files = []

        # parsing all the log files to get structured data
        for filename in filenames:
            #if os.path.getsize(filename.name) > 0:
            #file = filename.read()
            #file1_data = json.loads(json.dumps(xmltodict.parse(file)))
            #st.write(file1_data)

            if not filename.split('\\')[-1].startswith("Daily"):
                self.logger.warning(f" Skipping: {filename.split('/')[-1]}")
                continue

            self.logger.warning(f" Parsing: {filename.split('/')[-1]}")
            if filename.split('\\')[-1] in done_files:
                self.logger.warning(f" Skipping: {filename.split('/')[-1]}")
                continue
            else:
                done_files.append(filename.split('\\')[-1])
            try:
                tree = ET.parse(filename)
                #root = ET.fromstring(file)
                root = tree.getroot()
                for child in root:
                    if child.tag == "SystemConfiguration":
                        product_id = child.attrib.get('ProductID')
                        serial_number = child.attrib.get('SerialNumber')
                        for inner_child in child:
                            if inner_child.tag == "SoftwareVersion":
                                version = get_version_from_meta(inner_child.attrib)
                    if child.tag == "Event":
                        data.update(child.attrib)
                        for inner_child in child:
                            if inner_child.tag == "EventOriginatorInfo":
                                data.update(inner_child.attrib)
                            if inner_child.tag == "EventInfo":
                                data.update(inner_child.attrib)
                                for additional in inner_child:
                                    data.update(additional.attrib)
                    else:
                        continue
                    data.update({"FileName": filename.split('/')[-1]})
                    data.update({"Version": version})
                    data.update({"ProductID": product_id})
                    data.update({"SerialNumber": serial_number})
                    # serial_number
                    final_data.append(data)
                    data = {}
                    counter += 1
            except ET.ParseError:
                return st.error(f'{filename} might be empty')

        #st.write(final_data)
            #else:
                #st.error(f'{filename.name} is empty.')

        return create_structured_dataframe(final_data)

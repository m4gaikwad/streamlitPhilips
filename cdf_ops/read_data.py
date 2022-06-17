from datetime import datetime
import glob
import time
import xml.etree.ElementTree as ET
import logging 
from structure_data import (
    create_structured_dataframe,
    create_log_report,
    convert_df_to_csv,
    filter_df_by_unit,
    get_version_from_meta
)

logger = logging.getLogger(__name__)
filenames = glob.glob("/Users/shubham/Documents/work/Study/projects/philips/data_new/*/*/*/*.cdf")  # change the pattern to match your case


data = {}
final_data = []
counter = 0

done_files = []

# parsing all the log files to get structured data
for filename in filenames:
    if not filename.split('/')[-1].startswith("Daily"):
        logger.warning(f" Skipping: {filename.split('/')[-1]}")
        continue

    logger.warning(f" Parsing: {filename.split('/')[-1]}")
    if filename.split('/')[-1] in done_files:
        logger.warning(f" Skipping: {filename.split('/')[-1]}")
        continue
    else:
        done_files.append(filename.split('/')[-1])

    with open(filename, 'r', encoding="utf-8") as content:
        tree = ET.parse(content)
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
            data.update({"FileName":filename.split('/')[-1]})
            data.update({"Version":version})
            data.update({"ProductID":product_id})
            data.update({"SerialNumber":serial_number})
            serial_number
            final_data.append(data)
            data = {}
    time.sleep(0.01)

logger.warning("Populating gathered data to Dataframe ...")
time.sleep(0.5)

er_df = create_structured_dataframe(final_data)
er_df.to_pickle("full_data_new.pkl")

# logger.warning("Populating csv file from Dataframe ...")
# convert_df_to_csv(er_df,"structured_logs.csv")





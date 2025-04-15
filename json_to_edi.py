import json
import os
import sys
import logging
from helpers.enums import *
from loops.billing_loop import billing_provider_loop
from loops.subscriber_loop import subscriber_loop
from loops.patient_loop import patient_loop
from loops.claim_loop import claim_loop
from loops.rendering_and_facility_provider_loop import rendering_provider_and_services_loop
from helpers.shared_helpers import generate_random_string

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logging.basicConfig(level=logging.INFO)

def is_medicaid(json_data: dict) -> bool:
    # Returns True if the claim is a Medicaid claim
    # Check if the claimFilingCode is "MC" (Medicaid)
    return json_data.get("claimInformation", {}).get("claimFilingCode") == ClaimFilingIndicatorCode.Medicaid.value 

def has_dependent(json_data: dict) -> bool:
    # Check if the claim has a dependent
    return json_data.get("dependent") is not None


def generate_edi(json_data, test=False):
    hard_coded_header = """
ISA*00*          *00*          *ZZ*EVERGRNHLTH     *01*030240928      *240702*1531*^*00501*987654321*0*P*>~
GS*HC*EVERGRNHLTH*030240928*20240702*1533*987654321*X*005010X222A1~
ST*837*987654321*005010X222A1~
BHT*0019*00*1*20240702*1531*CH~
NM1*41*2*Evergreen Behavioral Health Center*****46*1234567890~
PER*IC*Dr. Casey Morgan*TE*2065550101~
NM1*40*2*PACIFIC HEALTHCARE NETWORK*****46*030240928~
HL*1**20*1~"""

    hard_coded_trailer = """SE*30*987654321~
GE*1*987654321~
IEA*1*987654321~"""

    # all loops in between the "envelope"
    claim_content = "\n".join(
        [
            *billing_provider_loop(json_data),
            *subscriber_loop(json_data, is_medicaid(json_data), has_dependent(json_data)),
            *patient_loop(json_data,has_dependent(json_data)),
            *claim_loop(json_data),
            *rendering_provider_and_services_loop(json_data)
        ]
    )
    edi = hard_coded_header + "\n" + claim_content + "\n" + hard_coded_trailer
    # print(edi)
    logging.info("EDI generated successfully")
    logging.info(f"EDI output:\n{edi}")
    # write output to a file for new jsonFiles
    if not test: 
        r = generate_random_string()
        output_filename =f"./examples/edifiles/{r}.edi"
        logging.info(f"EDI output file generated: {output_filename}")
        with open(output_filename, "w") as f:
            f.write(edi)
    
    return edi


def main():
    filename = "./examples/jsonfiles/example_1.json"
    # filename = "./examples/jsonfiles/example_2.json"
    # filename = "./examples/jsonfiles/example_3.json"
  
    logging.info(f"Input JSON file: {filename}")
    with open(filename) as file:
        json_data = json.load(file)

    ediFile = generate_edi(json_data)




main()

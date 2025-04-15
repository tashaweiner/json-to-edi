import enum
import json
from helpers.shared_helpers import (
    build_nm1_name_segment,
    build_address_segment,
    build_city_state_zip_segment,
    build_demographic_segment,
)
from helpers.enums import *


# Master patient loop
def patient_loop(json_data, has_dependent):
    # Both claims with and without a dependent will have a payer under the receiver
    segments = [helper_payer_name(json_data)]

    # If they don't have a dependent, move on to claims
    # If they have a dependent, go into the patient loop and add hierarchical -> PATient info
    if has_dependent:
        # Hierarchical Level
        hierarchy_segment = helper_patient_hierarchal(json_data)
        # PATient Information (dependent)
        patient_information = helper_patient_information(json_data)
        patient_name = build_nm1_name_segment(json_data, "dependent", "QC")
        patient_address = build_address_segment(json_data["dependent"])
        patient_city_state_zip = build_city_state_zip_segment(json_data["dependent"])
        dmg = build_demographic_segment(json_data["dependent"])
        segments += [
            hierarchy_segment,
            patient_information,
            patient_name,
            patient_address,
            patient_city_state_zip,
            dmg,
        ]

    return segments


def helper_patient_information(json_data):
    # Using .get instead of directly accessing the values in the JSON data so that if it doesn't exist, it will just get skipped
    # (helps with the optional fields)
    patient = json_data.get("dependent", {})
    relationship_to_subscriber_code = patient.get("relationshipToSubscriberCode", "")

    # Required
    segment = [SegmentHeader.PatientInformation.value, relationship_to_subscriber_code]

    # Optional (skip if empty)
    # PAT02–PAT04 are not used, so we skip to PAT05
    death_date = patient.get("patientDeathDate")
    if death_date:
        segment += ["", "", "", "D8", death_date]

    # Weight info
    unit = patient.get("unitOfMeasureCode")
    weight = patient.get("patientWeight")
    if unit and weight:
        segment += [unit, weight]

    # Pregnancy
    pregnancy = patient.get("pregnancyIndicator")
    if pregnancy:
        segment.append(pregnancy)

    return "*".join(segment) + "~"


def helper_patient_hierarchal(json_data):
    # Has a child if it is not Medicaid and it has a dependent
    # subscriber_has_child = not is_medicaid and has_dependent
    return "HL*3*2*23*0~"


# Can't use the shared helper because of too many differences
def helper_payer_name(json_data):
    payer_name = json_data["receiver"]["organizationName"].strip()
    payer_id = "WIMCD"  # Still hardcoded unless dynamic
    return "*".join(
        [
            SegmentHeader.Name.value,  # NM1
            "PR",  # Entity Identifier Code: Payer
            "2",  # Non-person entity
            payer_name,  # Organization name
            "", "", "", "",  # Empty optional name fields
            "PI",  # Identification Code Qualifier: Payor ID
            payer_id,
        ]
    ) + "~"

from helpers.shared_helpers import *
from helpers.enums import *

# Master subscriber loop
def subscriber_loop(json_data: dict, is_medicaid, has_dependent) -> list[str]:
    # Required
    hierarchySegment = helper_subscriber_hierarchal(json_data, is_medicaid, has_dependent)
    
    # Required
    subscriberInformation = helper_subscriber_information(json_data, has_dependent)
    subscriberName = build_nm1_name_segment(json_data, "subscriber", "IL")

    segments = [hierarchySegment, subscriberInformation + "~", subscriberName]
    
    # If they don't have a dependent
    if not has_dependent:
        subscriberAddress = build_address_segment(json_data["subscriber"])
        subscriberCityStateZip = build_city_state_zip_segment(json_data["subscriber"])
        subscriberDemographic = build_demographic_segment(json_data["subscriber"])
        segments += [subscriberAddress, subscriberCityStateZip, subscriberDemographic]
    
    # If they do have a dependent - then call patient loop
    return segments

def helper_subscriber_information(json_data, has_dependent):
    # Required
    paymentResponsibilityLevelCode = json_data["subscriber"]["paymentResponsibilityLevelCode"]
    
    # Optional
    if not has_dependent:
        individualRelationshipCode = RelationshipToSubscriber.Self.value
    else: 
        individualRelationshipCode = ""
    
    # Required
    claimFilingCode = json_data["claimInformation"]["claimFilingCode"]
    
    return "*".join([
        SegmentHeader.SubscriberInformation.value,
        paymentResponsibilityLevelCode,
        individualRelationshipCode,
        "", "", "", "", "", "", #(SBR03-SBR08)
        claimFilingCode
    ])

def helper_subscriber_hierarchal(json_data, is_medicaid, has_dependent):
    # Has a dependent (spouse) if it is not Medicaid and it has a dependent
    subscriber_has_dependent = not is_medicaid and has_dependent 

    if subscriber_has_dependent:
        return "HL*2*1*22*1~"
    else:
        return "HL*2*1*22*0~"

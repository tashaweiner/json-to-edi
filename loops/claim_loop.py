from helpers.enums import *

# Master claim loop
def claim_loop(json_data: dict) -> list[str]:
    segments = [
        helper_claim_information(json_data),
        helper_claim_reference(json_data),
        helper_claim_hi(json_data)
    ]
    return segments

# Helper for claim information
def helper_claim_information(json_data):
    claim = json_data["claimInformation"]
    
    charge_amount = str(float(claim["claimChargeAmount"]))  # Removes leading zeros
    place_of_service = claim.get("placeOfServiceCode", "")
    facility_code = claim.get("facilityCode", "B")  # Defaulting to "B" if not specified
    claim_freq_code = claim.get("claimFrequencyCode", "")

    composite_code = ">".join([place_of_service, facility_code, claim_freq_code])

    return "*".join([
        SegmentHeader.ClaimInformation.value,
        claim["patientControlNumber"],
        charge_amount,
        "", "",  # CLM03 & CLM04
        composite_code,
        claim["signatureIndicator"],
        claim["planParticipationCode"],
        claim["releaseInformationCode"],
        claim["benefitsAssignmentCertificationIndicator"]
    ]) + "~"

# Helper for claim prior authorization (optional value with REF)
def helper_claim_reference(json_data):
    prior_auth = json_data["claimInformation"].get("claimSupplementalInformation", {}).get("priorAuthorizationNumber")
    if prior_auth:
        return "*".join([SegmentHeader.Reference.value, ClaimReferenceQualifier.PriorAuthorization.value, prior_auth]) + "~"
    return ""

# Helper for claim diagnosis codes (HI)
def helper_claim_hi(json_data):
    hi_segments = []
    for diag in json_data["claimInformation"].get("healthCareCodeInformation", []):
        if diag.get("diagnosisTypeCode") and diag.get("diagnosisCode"):
            hi_segments.append("{}>{}".format(diag["diagnosisTypeCode"], diag["diagnosisCode"]))
    if hi_segments:
        return "HI*{}~".format("*".join(hi_segments))
    return ""
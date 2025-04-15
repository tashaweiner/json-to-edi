import random
import string
from helpers.enums import *
def build_nm1_name_segment(json_data: dict, person_key: str, role: str) -> str:
    person = json_data.get(person_key, {})

    fields = [
        "NM1",
        role,
        "1",
        person.get("lastName", ""),
        person.get("firstName", ""),
        person.get("middleName", ""),
        "",  # NM106: unused
        person.get("suffix", ""),
    ]

    # Only include Member ID for subscribers
    if person_key == "subscriber" and person.get("memberId"):
        fields += ["MI", person["memberId"]]
    #for rendering/service facility loop include NPI
    elif person_key in ["rendering", "serviceFacilityLocation"] and person.get("npi"):
        fields += [ReferenceIdentificationQualifier.NationalProviderIdentifier.value, person["npi"]]


    # Trim trailing empty fields
    while fields and fields[-1] == "":
        fields.pop()

    return "*".join(fields) + "~"

def build_address_segment(person: dict) -> str:
    """Build N3 segment with required address1 and optional address2."""
    address = person.get("address", {})
    segment = ["N3", address.get("address1", "")]
    if address.get("address2"):
        segment.append(address["address2"])
    return "*".join(segment) + "~"

def build_city_state_zip_segment(person: dict) -> str:
    address = person.get("address", {})
    return "*".join([
        "N4",
        address.get("city", ""),
        address.get("state", ""),
        address.get("postalCode", "")
    ]) + "~"

def build_demographic_segment(data: dict) -> str:
    """
    Build a DMG segment for demographic information (with tilde at the end).
    Expects keys: dateOfBirth and gender.
    Returns an empty string if either is missing.
    """
    dob = data.get("dateOfBirth")
    gender = data.get("gender")

    if not dob or not gender:
        return ""

    return "*".join(["DMG", "D8", dob, gender]) + "~"

def billing_and_service_facility_are_same(json_data):
    billing_npi = json_data.get("billing", {}).get("npi")
    facility_npi = json_data.get("claimInformation", {}).get("serviceFacilityLocation", {}).get("npi")
    return billing_npi and facility_npi and billing_npi == facility_npi

def has_multiple_services(json_data: dict) -> bool:
    service_lines = json_data.get("claimInformation", {}).get("serviceLines", [])
    # if there is more than exactly 1 item in the service line array then there are multiples
    return len(service_lines) > 1
def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

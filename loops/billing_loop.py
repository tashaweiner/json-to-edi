import enum
import json
from helpers.enums import *
from helpers.shared_helpers import (
    build_nm1_name_segment,
    build_address_segment,
    build_city_state_zip_segment,
)

# Master billing provider loop
def billing_provider_loop(json_data: dict) -> list[str]:
    billing_info = json_data.get("billing", {})
    segments = []

    # PRV Segment
    prv_segment = helper_billing_prv(billing_info)
    if prv_segment:
        segments.append(prv_segment)

    # NM1 Segment
    nm1_segment = helper_nm1_segment(billing_info)
    if nm1_segment:
        segments.append(nm1_segment)

    # Address Segment
    address_line = build_address_segment(billing_info)
    segments.append(address_line)

    # City/State/ZIP Segment
    city_state_zip = build_city_state_zip_segment(billing_info)
    segments.append(city_state_zip)

    # REF Segment (Employer ID)
    if billing_info.get("employerId"):
        segments.append(
            "*".join(
                [
                    SegmentHeader.Reference.value,
                    ReferenceIdentificationQualifier.EmployerIdentificationNumber.value,
                    billing_info["employerId"],
                ]
            )
            + "~"
        )

    # Optional PER Segment
    per_segment = optional_contact_info_inEDI(json_data)
    if per_segment:
        segments.append(per_segment + "~")

    return segments


def helper_billing_prv(billing_info):
    if billing_info.get("taxonomyCode"):
        return (
            "*".join(
                [
                    SegmentHeader.Provider.value,
                    ProviderType.Billing.value,
                    ReferenceIdentificationQualifier.TaxonomyCode.value,
                    billing_info["taxonomyCode"],
                ]
            )
            + "~"
        )
    return None


def helper_nm1_segment(billing_info):
    if billing_info.get("organizationName") and billing_info.get("npi"):
        # If organizationName is present, set entity_type to 2 (Organization)
        billing_name = billing_info.get("organizationName")
        billing_npi = billing_info.get("npi")
        entity_type = "2" if billing_info.get("organizationName") else "1"
        return (
            "*".join(
                [
                    SegmentHeader.Name.value,
                    EntityIdentifierCode.BillingProvider.value,
                    entity_type,
                    billing_name,
                    "", "", "", "",
                    ReferenceIdentificationQualifier.NationalProviderIdentifier.value,
                    billing_npi,
                ]
            )
            + "~"
        )
    return None


def billing_and_submitter_have_same_contact(json_data):
    billing_contact = json_data.get("billing", {}).get("contactInformation", {})
    submitter_contact = json_data.get("submitter", {}).get("contactInformation", {})

    return (
        billing_contact.get("name") == submitter_contact.get("name")
        and billing_contact.get("phoneNumber") == submitter_contact.get("phoneNumber")
    )


# This shouldn't be included if it was returned in the parent loop
def optional_contact_info_inEDI(json_data):
    if billing_and_submitter_have_same_contact(json_data):
        return None

    contact = json_data.get("billing", {}).get("contactInformation")
    if contact and contact.get("name") and contact.get("phoneNumber"):
        return "*".join(
            [
                SegmentHeader.Contact.value,
                ContactSegmentType.InformationContact.value,
                contact["name"],
                "TE",
                contact["phoneNumber"],
            ]
        )
    return None

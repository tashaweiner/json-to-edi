import enum
import json


class SegmentHeader(enum.Enum):
    Provider = "PRV"
    Name = "NM1"
    AddressLine1 = "N3"
    CityStatePostalCode = "N4"
    SubscriberInformation = "SBR"
    Reference = "REF"


class ProviderType(enum.Enum):
    Billing = "BI"


class RelationshipToSubscriber(enum.Enum):
    Self = "18"


class EntityIdentifierCode(enum.Enum):
    BillingProvider = "85"


class ReferenceIdentificationQualifier(enum.Enum):
    TaxonomyCode = "PXC"
    NationalProviderIdentifier = "XX"
    MemberId = "MI"
    EmployerIdentificationNumber = "EI"


class ClaimFilingIndicatorCode(enum.Enum):
    Medicaid = "MC"


class PaymentResponsibilityLevelCode(enum.Enum):
    Primary = "P"


# SBR*P*18*******MC~
# NM1*IL*1*Carson*Kenneth****MI*063997341~
# N3*Mojo Dojo Casa House~
# N4*Barbie Land*MA*000362919~
# DMG*D8*20141021*M~
def subscriber_loop(json_data: dict) -> list[str]:
    return [
        "*".join(
            [
                SegmentHeader.SubscriberInformation.value,
                PaymentResponsibilityLevelCode(
                    json_data["subscriber"]["paymentResponsibilityLevelCode"]
                ).value,
                RelationshipToSubscriber.Self.value,
                "",
                "",
                "",
                "",
                "",
                "",
                ClaimFilingIndicatorCode.Medicaid.value,
            ]
        )
        + "~",
        "*".join(
            [
                SegmentHeader.Name.value,
                "IL",
                "1",
                json_data["subscriber"]["lastName"],
                json_data["subscriber"]["firstName"],
                "",
                "",
                "",
                ReferenceIdentificationQualifier.MemberId.value,
                json_data["subscriber"]["memberId"],
            ]
        )
        + "~",
        "*".join(
            [
                SegmentHeader.AddressLine1.value,
                json_data["subscriber"]["address"]["address1"],
            ]
        )
        + "~",
        "*".join(
            [
                SegmentHeader.CityStatePostalCode.value,
                json_data["subscriber"]["address"]["city"],
                json_data["subscriber"]["address"]["state"],
                json_data["subscriber"]["address"]["postalCode"],
            ]
        )
        + "~",
    ]


def billing_provider_loop(json_data: dict) -> list[str]:
    # Billing provider
    # provider (PRV) segment
    return [
        "*".join(
            [
                SegmentHeader.Provider.value,
                ProviderType.Billing.value,
                ReferenceIdentificationQualifier.TaxonomyCode.value,
                json_data["billing"]["taxonomyCode"],
            ]
        )
        + "~",
        # name (NM1) segment
        "*".join(
            [
                SegmentHeader.Name.value,
                EntityIdentifierCode.BillingProvider.value,
                *(["2"] if "organizationName" in json_data["billing"] else ["1"]),
                json_data["billing"]["organizationName"],
                "",
                "",
                "",
                "",
                ReferenceIdentificationQualifier.NationalProviderIdentifier.value,
                json_data["billing"]["npi"],
            ]
        )
        + "~",
        # address line 1 (N3) segment
        "*".join(
            [
                SegmentHeader.AddressLine1.value,
                json_data["billing"]["address"]["address1"],
            ]
        )
        + "~",
        # city, state, postal code (N4) segment
        "*".join(
            [
                SegmentHeader.CityStatePostalCode.value,
                json_data["billing"]["address"]["city"],
                json_data["billing"]["address"]["state"],
                json_data["billing"]["address"]["postalCode"],
            ]
        )
        + "~",
        "*".join(
            [
                SegmentHeader.Reference.value,
                ReferenceIdentificationQualifier.EmployerIdentificationNumber.value,
                json_data["billing"]["employerId"],
            ]
        )
        + "~",
    ]


def main():
    hard_coded_header = """
ISA*00*          *00*          *ZZ*AV09311993     *01*030240928      *240702*1531*^*00501*415133923*0*P*>~
GS*HC*1923294*030240928*20240702*1533*415133923*X*005010X222A1~
ST*837*415133923*005010X222A1~
BHT*0019*00*1*20240702*1531*CH~
NM1*41*2*Mattel Industries*****46*1234567890~
PER*IC*Ruth Handler*TE*8458130000~
NM1*40*2*AVAILITY 5010*****46*030240928~
HL*1**20*1~"""

    hard_coded_trailer = """SE*30*415133923~
GE*1*415133923~
IEA*1*415133923~
"""
    filename = "./examples/mojo_dojo_casa_house.json"
    with open(filename) as file:
        json_data = json.load(file)

    claim_content = "\n".join(
        [
            *billing_provider_loop(json_data),
            "HL*2*1*22*0~",  # Hierarchical Level
            *subscriber_loop(json_data),
        ]
    )
    edi = hard_coded_header + "\n" + claim_content + "\n" + hard_coded_trailer
    print(edi)


main()

import enum

class SegmentHeader(enum.Enum):
    Provider = "PRV"
    Name = "NM1"
    AddressLine1 = "N3"
    CityStatePostalCode = "N4"
    SubscriberInformation = "SBR"
    Reference = "REF"
    PatientInformation = "PAT"
    ClaimInformation = "CLM"
    ClaimReference = "REF"
    HealthCareInformation = "HI"
    PriorAuthorization = "G1"
    Contact = "PER"
    ClaimSupplementalInformation = "HI"
    ClaimFrequency = "CLM"

class ProviderType(enum.Enum):
    Billing = "BI"
    Performing = "PE"

class RelationshipToSubscriber(enum.Enum):
    Self = "18"

class EntityIdentifierCode(enum.Enum):
    BillingProvider = "85"
    Subscriber = "IL"
    Patient = "QC"
    Payer = "PR"
    RenderingProvider = "82"
    ReferringProvider = "DN"
    ServiceFacility = "77"
    ServiceFacilityLocation = "77"

class ReferenceIdentificationQualifier(enum.Enum):
    TaxonomyCode = "PXC"
    NationalProviderIdentifier = "XX"
    MemberId = "MI"
    EmployerIdentificationNumber = "EI"
    PayorId = "PI"

class ClaimFilingIndicatorCode(enum.Enum):
    Medicaid = "MC"
    Commercial = "CI"

class PaymentResponsibilityLevelCode(enum.Enum):
    Primary = "P"

class ClaimReferenceQualifier(enum.Enum):
    PriorAuthorization = "G1"
    
class ContactSegmentType(enum.Enum):
    InformationContact = "IC"
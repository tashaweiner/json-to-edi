from helpers.enums import *
from helpers.shared_helpers import *

# #master rendering provider and services loop 
def rendering_provider_and_services_loop(json_data: dict):
    # all cases will run rendering loop 
    segments = []
    #everything will have a rendering provider
    rendering_segment = rendering_loop(json_data)
    services_segment = services_loop(json_data)
    if not billing_and_service_facility_are_same(json_data):
       service_facility =service_facility_loop(json_data)
       segments = segments +service_facility
    
    # if there are multiple SRV(procedure codes)with same provider 
    if has_multiple_services(json_data):
        segments = segments + rendering_segment 
        segments = segments + services_segment
    else:
        segments = segments + services_segment
        segments = segments + rendering_segment

    return segments


def service_facility_loop(json_data: dict):
    nm1 = helper_service_facility_nm1_segment(json_data)
    nm3 = build_address_segment(json_data["claimInformation"]["serviceFacilityLocation"])
    nm4 =  build_city_state_zip_segment(json_data["claimInformation"]["serviceFacilityLocation"])
    return [nm1, nm3, nm4]

def services_loop(json_data: dict):
    service_lines = json_data.get("claimInformation", {}).get("serviceLines", [])
    services = []
    for count, service in enumerate(service_lines, start=1):
        services.append(build_lx_segment(count))
        services.append(build_sv1_segment(service))
        dtp_segment = build_dtp_segment(service)
        if dtp_segment:
            services.append(dtp_segment)
    return services

def rendering_loop(json_data: dict) -> list[str]:
    # Check if rendering provider information is present
    # Determine which rendering key is present
    rendering_key = "rendering"
    if "rendering" in json_data:
        rendering_key = "rendering"
    elif "renderingProvider" in json_data["claimInformation"]["serviceLines"][0]:
        # Assume it's under serviceLines[0], update if needed
        json_data["rendering"] = json_data["claimInformation"]["serviceLines"][0]["renderingProvider"]
        rendering_key = "rendering"
    else:
        return []  # No rendering info found
    name_seg=build_nm1_name_segment(json_data, rendering_key, EntityIdentifierCode.RenderingProvider.value)
    rendering_info = json_data.get("rendering") or json_data.get("renderingProvider")

    #Rendering Provider Specialty Information
    rendering_provider= helper_rendering_provider_specialty(rendering_info)
    return [name_seg, rendering_provider]


  # rendering_info = json_data.get("rendering", {})
def helper_service_facility_nm1_segment(json_data: dict) -> str:
    facility = json_data.get("claimInformation", {}).get("serviceFacilityLocation", {})

    return "*".join([
        SegmentHeader.Name.value,                         # NM1
        EntityIdentifierCode.ServiceFacility.value,       # 77
        "2",                                               # Non-person entity
        facility.get("organizationName", ""),             # Organization name
        "", "", "", "",                                    # NM104–NM107 unused
        ReferenceIdentificationQualifier.NationalProviderIdentifier.value,  # XX
        facility.get("npi", "")                            # NPI
    ]) + "~"


def helper_rendering_provider_specialty(rendering_info):
    """
    Build a PRV segment for rendering provider specialty information.
    Expects keys: taxonomyCode.
    Returns an empty string if taxonomyCode is missing.
    """
    taxonomy_code = rendering_info.get("taxonomyCode")
    if not taxonomy_code:
        return ""
    return "*".join([
        SegmentHeader.Provider.value,
        ProviderType.Performing.value,
        ReferenceIdentificationQualifier.TaxonomyCode.value,
        taxonomy_code
    ]) + "~"

def build_lx_segment(index: int) -> str:
    return f"LX*{index}~"


def build_sv1_segment(line: dict) -> str:
    professional = line.get("professionalService", {})
    procedure_id = professional.get("procedureIdentifier", "")
    procedure_code = professional.get("procedureCode", "")
    charge_amount = str(float(professional.get("lineItemChargeAmount", "0")))
    unit = professional.get("measurementUnit", "")
    unit_count = str(float(professional.get("serviceUnitCount", "1")))

    # Diagnosis code pointers
    pointers = professional.get("compositeDiagnosisCodePointers", {}).get("diagnosisCodePointers", [])
    pointer_str = "*".join(pointers) if pointers else ""

    sv1_fields = [
        "SV1",
        f"{procedure_id}>{procedure_code}",
        charge_amount,
        unit,
        unit_count,
        "", "", # SV105, SV107 unused
        pointer_str
    ]

    return "*".join(sv1_fields) + "~"


def build_dtp_segment(line: dict) -> str:
    service_date = line.get("serviceDate", "")
    if service_date:
        return f"DTP*472*D8*{service_date}~"
    return ""
import json


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
    # Your code goes here
    hard_coded_trailer = """
SE*30*415133923~
GE*1*415133923~
IEA*1*415133923~
"""
    filename = "./examples/mojo_dojo_casa_house.json"
    with open(filename) as file:
        json_data = json.load(file)

    claim_content = "\n".join(
        [
            # Billing provider
            # provider (PRV) segment
            "*".join(["PRV", "BI", "PXC", json_data["billing"]["taxonomyCode"]]) + "~",
            # name (NM1) segment
            "*".join(
                [
                    "NM1",
                    "85",
                    *(["2"] if "organizationName" in json_data["billing"] else ["1"]),
                    json_data["billing"]["organizationName"],
                    "",
                    "",
                    "",
                    "",
                    "XX",
                    json_data["billing"]["npi"],
                ]
            )
            + "~",
            # address line 1 (N3) segment
            "*".join(["N3", json_data["billing"]["address"]["address1"]]) + "~",
            # city, state, postal code (N4) segment
            "*".join(
                [
                    "N4",
                    json_data["billing"]["address"]["city"],
                    json_data["billing"]["address"]["state"],
                    json_data["billing"]["address"]["postalCode"],
                ]
            )
            + "~",
        ]
    )
    edi = hard_coded_header + "\n" + claim_content + "\n" + hard_coded_trailer
    print(edi)


main()

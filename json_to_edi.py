import json


def main():
    hard_coded_header = """
ISA*00*          *00*          *01*BARBIE         *01*BLMC           *240224*0000*^*00501*415133923*0*P*>~
GS*HC*BARBIE*BLMC*20240224*0000*415133923*X*005010X222A2~
ST*837*415133923*005010X222A2~
BHT*0019*00*1*20240224*0000*CH~
NM1*41*2*Mattel Industries*****46*MATTELINC~
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
            # provideer segment
            f"PRV*BI*PXC*{json_data['billing']['taxonomyCode']}",
            # name segment
            f"NM1*85*{2 if 'organizationName' in json_data['billing'] else 1}*{json_data['billing']['organizationName']}*****XX*{json_data['billing']['npi']}~",
            # address line 1
            f"N3*{json_data['billing']['address']['address1']}~",
            # city, state, postal code
            f"N4*{json_data['billing']['address']['city']}*{json_data['billing']['address']['state']}*{json_data['billing']['address']['postalCode']}~",
        ]
    )
    edi = hard_coded_header + "\n" + claim_content + "\n" + hard_coded_trailer
    print(edi)


main()

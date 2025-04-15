JSON to EDI
=======

## Running the Project
### Python Version
Python 3.13.2
### Generate the EDI Output
json_to_edi.py returns a string that contains the entire EDI output for associated JSON files that are uploaded to examples folder 

```bash
python3 json_to_edi.py
```

### Test - example files provided
```bash
python3 -m unittest tests/test_edi_segments.py
```

## Loops Structure
Billing Provider
└── Subscriber
    └── Patient (if dependent exists)
        └── Claim
            ├── Service Facility (if different from Billing Provider)
            ├── Rendering Provider
            └── Service Lines


## Edge Cases/ Rules 
- Medicaid Claims 
	- Medicaid always lists the child as the subscriber. Dependents are not used for Medicaid claims.
- Private Insurance 
	- Can include either:
		- A subscriber-only claim (no dependent field).
		- a claim with a dependent listed seperately as the patient 
	- If no dependent is present, the subscriber is also the patient.
- Contact Info Rules
	- If the billing provider and submitter have the same contact info (name + phone), omit the PER segment in the billing loop to avoid duplication.
- NPI rules 
	- If the billing provider and service facility share the same NPI, treat them as the same legal entity and skip the service facility loop.

- When there are multiple service lines, it's assumed they share the same rendering provider, so it gets declared once before the lines.
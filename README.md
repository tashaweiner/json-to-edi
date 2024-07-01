barbEDI
=======


## Structure
barbiedi/
 => .git/
 => examples/
		=> mojo_dojo_casa_house.837
		=> mojo_dojo_casa_house.json
		=> multi_procedure_barbie.837
		=> multi_procedure_barbie.json
		=> subscriber_with_a_dekendent.837
		=> subscriber_with_a_dekendent.json
 => edi_to_json.py

The `examples` folder includes three example JSON files and the 837 files that they generate.

**Note**
The beginning envelope of the 837 Professional claim — the interchange, group set, and transaction set portions — are provided in `edi_to_json`. To cut down on implementation time, you may copy/paste these into your implementation.
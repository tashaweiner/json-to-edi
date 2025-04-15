import json
import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from json_to_edi import *

def load_example(filename):
    with open(filename) as f:
        return json.load(f)

# Load updated JSON test files
data1 = load_example("examples/jsonfiles/example_1.json")
data2 = load_example("examples/jsonfiles/example_2.json")
data3 = load_example("examples/jsonfiles/example_3.json")

is_medicade_data1 = is_medicaid(data1)
is_medicade_data2 = is_medicaid(data2)
is_medicade_data3 = is_medicaid(data3)

has_dependent_data1 = has_dependent(data1)
has_dependent_data2 = has_dependent(data2)
has_dependent_data3 = has_dependent(data3)

class TestBillingLoop(unittest.TestCase):
    def test_billing_provider_loop_file1(self):
        output = billing_provider_loop(data1)
        self.assertTrue(any("NM1*85*2*" in seg for seg in output))
        self.assertTrue(any("N3*" in seg for seg in output))
        self.assertTrue(any("N4*" in seg for seg in output))

    def test_billing_provider_loop_file2(self):
        output = billing_provider_loop(data2)
        self.assertTrue(any("NM1*85*2*" in seg for seg in output))
        self.assertTrue(any("REF*EI*" in seg for seg in output))

    def test_billing_provider_loop_file3(self):
        output = billing_provider_loop(data3)
        self.assertTrue(any("NM1*85*2*" in seg for seg in output))
        self.assertTrue(any("N3*" in seg for seg in output))
        self.assertTrue(any("N4*" in seg for seg in output))

    

class TestSubscriberLoop(unittest.TestCase):
    def test_subscriber_loop_file1(self):
        output = subscriber_loop(data1, is_medicade_data1, has_dependent_data1)
        self.assertTrue(any("NM1*IL*1*" in seg for seg in output))
        self.assertTrue(any("SBR*P*" in seg for seg in output))
        self.assertTrue(any("DMG*D8*" in seg for seg in output))

    def test_subscriber_loop_file2(self):
        output = subscriber_loop(data2, is_medicade_data2, has_dependent_data2)
        self.assertTrue(any("NM1*IL*1*" in seg for seg in output))

    def test_subscriber_loop_file3(self):
        output = subscriber_loop(data3, is_medicade_data3, has_dependent_data3)
        self.assertTrue(any("NM1*IL*1*" in seg for seg in output))
class TestPatientLoop(unittest.TestCase):
    def test_patient_loop_file3(self):
        output = patient_loop(data3, has_dependent_data3)
        if has_dependent_data3:
            self.assertTrue(any("NM1*QC*1*" in seg for seg in output))
            self.assertTrue(any("DMG*D8*" in seg for seg in output))

class TestClaimLoop(unittest.TestCase):
    def test_claim_loop_file1(self):
        output = claim_loop(data1)
        self.assertTrue(any("CLM*" in seg for seg in output))
        self.assertTrue(any("HI*ABK>" in seg for seg in output))

    def test_claim_loop_file2(self):
        output = claim_loop(data2)
        self.assertTrue(any("CLM*" in seg for seg in output))
        self.assertTrue(any("HI*ABK>" in seg for seg in output))

    def test_claim_loop_file3(self):
        output = claim_loop(data3)
        self.assertTrue(any("CLM*" in seg for seg in output))
        self.assertTrue(any("HI*ABK>" in seg for seg in output))


# class TestFacilityLoop(unittest.TestCase):
#     def test_facility_loop_file1(self):
#         output = rendering_provider_and_services_loop(data1)
#         self.assertTrue(any("NM1*77*" in seg for seg in output))

#     def test_facility_loop_file2(self):
#         output = rendering_provider_and_services_loop(data2)
#         self.assertTrue(any("NM1*77*" in seg for seg in output))

class TestServicesLoop(unittest.TestCase):
    def test_services_loop_file1(self):
        output = rendering_provider_and_services_loop(data1)
        self.assertTrue(any("LX*1~" in seg for seg in output))
        self.assertTrue(any("SV1*" in seg for seg in output))
        self.assertTrue(any("DTP*472*" in seg for seg in output))

    def test_services_loop_file2(self):
        output = rendering_provider_and_services_loop(data2)
        self.assertTrue(any("LX*1~" in seg for seg in output))
        self.assertTrue(any("LX*2~" in seg for seg in output))

    def test_services_loop_file3(self):
        output = rendering_provider_and_services_loop(data3)
        self.assertTrue(any("LX*1~" in seg for seg in output))
if __name__ == "__main__":
    unittest.main()

import unittest
from app import app
import json

class TestPlsRestApi(unittest.TestCase):

    # SET UP FOR TESTING
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    # TESTING FOR GENDER ENDPOINT
    def test_gender_male(self):
        result = self.app.get('pnums/gender/24129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745378", "gender": "male"}
        self.assertEqual(result, desired_result)
    
    def test_gender_female(self):
        result = self.app.get('pnums/gender/24129745478')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745478", "gender": "female"}
        self.assertEqual(result, desired_result)
    
    def test_gender_invalid_pnum(self):
        result = self.app.get('pnums/gender/2412974547')
        self.assertEqual(result.status_code, 400)
    
    def test_gender_no_pnum(self):
        result = self.app.get('pnums/gender')
        self.assertEqual(result.status_code, 404)
    
    # TESTING FOR AGE ENDPOINT
    def test_age(self):
        result = self.app.get('pnums/age/24129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745378", "age": "25"}
        self.assertEqual(result, desired_result)
    
    def test_age_early_birthday(self):
        result = self.app.get('pnums/age/24019745478')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24019745478", "age": "26"}
        self.assertEqual(result, desired_result)
    
    def test_age_future_birthdate(self):
        result = self.app.get('pnums/age/24122445478')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24122445478", "age": "98"}
        self.assertEqual(result, desired_result)
    
    def test_age_invalid_pnum(self):
        result = self.app.get('pnums/age/2412974547')
        self.assertEqual(result.status_code, 400)
    
    def test_age_no_pnum(self):
        result = self.app.get('pnums/age')
        self.assertEqual(result.status_code, 404)
    
    # TESTING FOR VALID PNUM ENDPOINT
    def test_valid_pnum(self):
        result = self.app.get('pnums/isvalid/24129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745378", "is valid pnum": "yes"}
        self.assertEqual(result, desired_result)
    
    def test_valid_pnum_with_whitespaces(self):
        result = self.app.get('pnums/isvalid/ 24129745378  ')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745378", "is valid pnum": "yes"}
        self.assertEqual(result, desired_result)
    
    def test_invalid_character_pnum(self):
        result = self.app.get('pnums/isvalid/4-129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "4-129745378", "is valid pnum": "no", "reason": "The input personal number contains invalid characters."}
        self.assertEqual(result, desired_result)
    
    def test_invalid_too_long_pnum(self):
        result = self.app.get('pnums/isvalid/224129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "224129745378", "is valid pnum": "no", "reason": "The input personal numbers must contain 11 digits."}
        self.assertEqual(result, desired_result)
    
    def test_invalid_too_short_pnum(self):
        result = self.app.get('pnums/isvalid/4129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "4129745378", "is valid pnum": "no", "reason": "The input personal numbers must contain 11 digits."}
        self.assertEqual(result, desired_result)
    
    def test_invalid_fake_day_pnum(self):
        result = self.app.get('pnums/isvalid/32122445378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "32122445378", "is valid pnum": "no", "reason": "The input personal numbers contains an invalid date of birth."}
        self.assertEqual(result, desired_result)
    
    def test_invalid_fake_month_pnum(self):
        result = self.app.get('pnums/isvalid/24132445378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24132445378", "is valid pnum": "no", "reason": "The input personal numbers contains an invalid date of birth."}
        self.assertEqual(result, desired_result)
    
    def test_valid_pnum_no_input(self):
        result = self.app.get('pnums/isvalid')
        self.assertEqual(result.status_code, 404)
    
    # TESTING FOR REGISTERED PNUM ENDPOINT
    def test_registered_pnum(self):
        result = self.app.get('pnums/isregistered/24129745378')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "24129745378", "is in dataset": "yes", "is valid pnum": "yes"}
        self.assertEqual(result, desired_result)
    
    def test_registered_invalid_pnum(self):
        result = self.app.get('pnums/isregistered/2412974537')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "2412974537", "is in dataset": "yes", "is valid pnum": "no"}
        self.assertEqual(result, desired_result)
    
    def test_nonregistered_pnum(self):
        result = self.app.get('pnums/isregistered/11111111111')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"pnum": "11111111111", "is in dataset": "no", "is valid pnum": "yes"}
        self.assertEqual(result, desired_result)
    
    def test_registered_pnum_no_input(self):
        result = self.app.get('pnums/isvalid')
        self.assertEqual(result.status_code, 404)
        
    # TESTING FOR LISTALL PNUM ENDPOINT
    def test_listall_pnum(self):
        result = self.app.get('pnums/listall')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {"total pnums": "6", "valid pnums": "4", "invalid pnums": "2", "male": "2", "female": "2"}
        self.assertEqual(result, desired_result)
    
    def test_listall_pnum_with_input(self):
        result = self.app.get('pnums/listall/24129745378')
        self.assertEqual(result.status_code, 404)
    
    # TESTING FOR LISTBYGROUPS PNUM ENDPOINT
    def test_listbygroups_pnum(self):
        result = self.app.get('pnums/listbygroups')
        result = json.loads(result.get_data(as_text=True))
        desired_result = {
            "('20 - 29 years', 'male')": "1",
            "('20 - 29 years', 'female')": "1",
            "('40 - 49 years', 'male')": "1",
            "('50 - 59 years', 'female')": "1"
            }
        self.assertEqual(result, desired_result)
    
    def test_listbygroups_pnum_with_input(self):
        result = self.app.get('pnums/listbygroups/24129745378')
        self.assertEqual(result.status_code, 404)

if __name__ == "__main__":
    unittest.main()
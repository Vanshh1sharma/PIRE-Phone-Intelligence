from phonenumbers import number_type as get_number_type, PhoneNumberType
from phonenumbers import carrier, geocoder, timezone
import phonenumbers


class RiskScorer:
    
    def __init__(self):
        self.weighted_scores = {}
        self.flags = []
        self.risk_details = []
        self.final_score = 0
        self.risk_level = "Unknown"
        
        # Weights for checking (total should be 100)
        self.weights = {
            "number_type": 15,
            "carrier": 20,
            "region": 15,
            "timezone": 10,
            "validity": 20,
            "formatting": 10,
            "metadata": 10
        }
    
    def check_number_type(self, parsed_number):
        try:
            type_result = get_number_type(parsed_number)
            score = 0
            message = ""
            
            if type_result == PhoneNumberType.MOBILE:
                score = 2  
                message = "Mobile Number - Low Risk"
            elif type_result == PhoneNumberType.FIXED_LINE:
                score = 3
                message = "Fixed Line Number - Low Risk"
            elif type_result == PhoneNumberType.VOIP:
                score = 14 
                message = "VOIP Number - High Risk (Dangerous)"
                self.flags.append("VOIP_DETECTED")
            elif type_result == PhoneNumberType.TOLL_FREE:
                score = 10
                message = "Toll Free Number - Medium Risk"
                self.flags.append("TOLL_FREE")
            elif type_result == PhoneNumberType.PREMIUM_RATE:
                score = 12
                message = "Premium Rate Number - High Risk"
                self.flags.append("PREMIUM_RATE")
            elif type_result == PhoneNumberType.UNKNOWN:
                score = 10
                message = "Unknown Number Type"
                self.flags.append("UNKNOWN_TYPE")
            else:
                score = 8
                message = "Unrecognized Number Type"
            
            self.weighted_scores["number_type"] = score
            self.risk_details.append({
                "check": "Number Type",
                "message": message,
                "score": score,
                "weight": self.weights["number_type"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Number Type",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["number_type"]
            })
    
    def check_carrier(self, parsed_number):
        try:
            carrier_name = carrier.name_for_number(parsed_number, "en")
            score = 0
            message = ""
            
            risky_providers = ["TextNow", "Dingtone", "FreedomPop", "Sonetel", 
                             "Hushed", "Google Voice", "Skype", "Telegram"]
            
            if not carrier_name:
                score = 12
                message = "No Carrier Detected - Suspicious"
                self.flags.append("NO_CARRIER")
            elif carrier_name in risky_providers:
                score = 18  # Out of 20
                message = f"Risky Carrier: {carrier_name}"
                self.flags.append(f"RISKY_CARRIER_{carrier_name.upper()}")
            else:
                score = 4
                message = f"Legitimate Carrier: {carrier_name}"
            
            self.weighted_scores["carrier"] = score
            self.risk_details.append({
                "check": "Carrier",
                "message": message,
                "score": score,
                "weight": self.weights["carrier"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Carrier",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["carrier"]
            })
    
    def check_region(self, parsed_number):
        try:
            region = geocoder.region_code_for_number(parsed_number)
            score = 0
            message = ""
            
            high_risk_countries = ["KP", "IR", "SY", "CU", "SD"]  
            suspicious_regions = ["XX", ""]  
            
            if region in high_risk_countries:
                score = 14
                message = f"High-Risk Region: {region}"
                self.flags.append(f"HIGH_RISK_REGION_{region}")
            elif region in suspicious_regions:
                score = 10
                message = "Unknown/Suspicious Region"
                self.flags.append("UNKNOWN_REGION")
            else:
                score = 2
                message = f"Region: {region}"
            
            self.weighted_scores["region"] = score
            self.risk_details.append({
                "check": "Region",
                "message": message,
                "score": score,
                "weight": self.weights["region"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Region",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["region"]
            })
    
    def check_timezone(self, parsed_number):
        try:
            timezones = timezone.time_zones_for_number(parsed_number)
            score = 0
            message = ""
            
            if not timezones:
                score = 8
                message = "No Timezone Data - Suspicious"
                self.flags.append("NO_TIMEZONE")
            elif len(timezones) > 3:
                score = 6
                message = f"Multiple Timezones ({len(timezones)}) - Suspicious"
                self.flags.append("MULTIPLE_TIMEZONES")
            else:
                score = 2
                message = f"Timezone: {timezones[0] if timezones else 'Unknown'}"
            
            self.weighted_scores["timezone"] = score
            self.risk_details.append({
                "check": "Timezone",
                "message": message,
                "score": score,
                "weight": self.weights["timezone"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Timezone",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["timezone"]
            })
    
    def check_validity(self, parsed_number):
        try:
            is_valid = phonenumbers.is_valid_number(parsed_number)
            is_possible = phonenumbers.is_possible_number(parsed_number)
            score = 0
            message = ""
            
            if is_valid and is_possible:
                score = 2
                message = "Valid and Possible - Low Risk"
            elif is_possible:
                score = 8
                message = "Possible but Not Valid - Suspicious"
                self.flags.append("INVALID_NUMBER")
            else:
                score = 15  # Out of 20
                message = "Invalid Number - Very Suspicious"
                self.flags.append("IMPOSSIBLE_NUMBER")
            
            self.weighted_scores["validity"] = score
            self.risk_details.append({
                "check": "Validity",
                "message": message,
                "score": score,
                "weight": self.weights["validity"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Validity",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["validity"]
            })
    
    def check_formatting(self, parsed_number):
        try:
            national_number = str(parsed_number.national_number)
            score = 0
            message = ""
            
            if national_number.startswith("0"):
                score = 5
                message = "Starts with 0 Potential formatting issue"
                self.flags.append("STARTS_WITH_ZERO")
            elif len(national_number) < 7:
                score = 8
                message = "Very short number - Suspicious"
                self.flags.append("TOO_SHORT")
            elif len(national_number) > 15:
                score = 6
                message = "Very long number - Suspicious"
                self.flags.append("TOO_LONG")
            else:
                score = 2
                message = f"Normal format - {len(national_number)} digits"
            
            self.weighted_scores["formatting"] = score
            self.risk_details.append({
                "check": "Formatting",
                "message": message,
                "score": score,
                "weight": self.weights["formatting"]
            })
        except Exception as e:
            self.risk_details.append({
                "check": "Formatting",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["formatting"]
            })
    
    def extract_metadata(self, parsed_number):
        try:
            metadata = {
                "country_code": parsed_number.country_code,
                "national_number": parsed_number.national_number,
                "number_type": str(get_number_type(parsed_number)),
                "region": geocoder.region_code_for_number(parsed_number),
                "carrier": carrier.name_for_number(parsed_number, "en"),
                "timezones": timezone.time_zones_for_number(parsed_number)
            }
            score = 2
            message = "Metadata extracted successfully"
            
            self.weighted_scores["metadata"] = score
            self.risk_details.append({
                "check": "Metadata",
                "message": message,
                "score": score,
                "weight": self.weights["metadata"],
                "metadata": metadata
            })
            
            return metadata
        except Exception as e:
            self.risk_details.append({
                "check": "Metadata",
                "message": f"Error: {e}",
                "score": 0,
                "weight": self.weights["metadata"]
            })
            return {}
    
    def calculate_weighted_score(self):
        total_weighted_score = 0
        total_weight = 0
        
        for check_name, weight in self.weights.items():
            if check_name in self.weighted_scores:
                score = self.weighted_scores[check_name]
                total_weighted_score += score * weight
                total_weight += weight * 10  
        
        
        if total_weight > 0:
            self.final_score = int((total_weighted_score / total_weight) * 100)
        else:
            self.final_score = 0
        
        
        self.final_score = min(100, self.final_score)
        
        return self.final_score
    
    def calculate_risk_level(self):
        if self.final_score <= 30:
            self.risk_level = "LOW"
        elif self.final_score <= 50:
            self.risk_level = "MEDIUM"
        elif self.final_score <= 70:
            self.risk_level = "HIGH"
        else:
            self.risk_level = "CRITICAL"
        
        return self.risk_level
    
    def generate_flags(self):
        return list(set(self.flags))  # because set - Remove duplicates
    
    def get_risk_report(self):
        self.calculate_weighted_score()
        self.calculate_risk_level()
        
        return {
            "risk_score": self.final_score,
            "risk_level": self.risk_level,
            "flags": self.generate_flags(),
            "risk_details": self.risk_details,
            "summary": f"Risk Score: {self.final_score}/100 - Level: {self.risk_level}",
            "flag_count": len(self.generate_flags())
        }


# this is the main thing for the main code here i it will pass the human value and uske baad 
# mere saare function me jake check hoga number

def calculate_risk(parsed_number):
    scorer = RiskScorer()
    
   
    scorer.check_number_type(parsed_number)
    scorer.check_carrier(parsed_number)
    scorer.check_region(parsed_number)
    scorer.check_timezone(parsed_number)
    scorer.check_validity(parsed_number)
    scorer.check_formatting(parsed_number)
    scorer.extract_metadata(parsed_number)
    
    
    return scorer.get_risk_report()
from cerberus import Validator

def validate_fields(json: dict):
    schema = {
        "free_cash_flow_to_total_debt": {'required': True, 'type': 'float'},  
        "accounts_payable_turnover":{'required': True, 'type': 'float'}, 
        "operating_margin": {'required': True, 'type': 'float'}, 
        "sales_per_employee": {'required': True, 'type': 'float'}, 
        "asset_turnover": {'required': True, 'type': 'float'}, 
        "total_debt_to_total_assets": {'required': True, 'type': 'float'}, 
        "current_ratio": {'required': True, 'type': 'float'}, 
        "revenue_growth_year_over_year": {'required': True, 'type': 'float'}, 
        "return_on_assets": {'required': True, 'type': 'float'}
    }
    return Validator(schema).validate(json)

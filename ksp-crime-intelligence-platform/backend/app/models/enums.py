from enum import Enum


class CaseStatus(str, Enum):
    OPEN = "open"
    UNDER_INVESTIGATION = "under_investigation"
    CHARGESHEET_FILED = "chargesheet_filed"
    CLOSED = "closed"
    COLD = "cold"


class CrimeCategory(str, Enum):
    THEFT = "theft"
    ROBBERY = "robbery"
    BURGLARY = "burglary"
    ASSAULT = "assault"
    HOMICIDE = "homicide"
    CYBERCRIME = "cybercrime"
    FINANCIAL_FRAUD = "financial_fraud"
    NARCOTICS = "narcotics"
    KIDNAPPING = "kidnapping"
    SEXUAL_OFFENSE = "sexual_offense"
    OTHER = "other"


class GraphNodeType(str, Enum):
    SUSPECT = "suspect"
    VICTIM = "victim"
    LOCATION = "location"
    INCIDENT = "incident"
    PHONE_NUMBER = "phone_number"
    VEHICLE = "vehicle"
    BANK_ACCOUNT = "bank_account"


class GraphEdgeType(str, Enum):
    SUSPECT_OF = "suspect_of"  # suspect -> incident
    VICTIM_OF = "victim_of"  # victim -> incident
    OCCURRED_AT = "occurred_at"  # incident -> location
    ASSOCIATED_WITH = "associated_with"  # suspect -> suspect
    CONTACTED = "contacted"  # phone_number -> phone_number (CDR)
    OWNS = "owns"  # suspect -> vehicle / bank_account
    SIMILAR_MO = "similar_mo"  # incident -> incident

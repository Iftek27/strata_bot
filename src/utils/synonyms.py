# Synonym map for key terms in the Unit Titles (Management) Act 2011 (ACT).
# Keeps synonyms tight and relevant to avoid pulling in noisy/unrelated sections.

SYNONYM_MAP = {
    # Maintenance / repairs
    "repairs": ["maintenance", "fixing damage", "repairing damage"],
    "roof repairs": ["roof maintenance", "roofing repairs", "waterproofing repairs"],
    "maintenance plan": ["capital works plan", "long-term maintenance plan"],
    "maintenance schedule": ["schedule of maintenance", "works schedule"],

    # Defined parts
    "defined parts": ["load-bearing walls", "balconies", "beams", "slabs", "columns"],

    # Leaks
    "leaks": ["water leak", "leakage"],   # keep tight to avoid dragging in insurance flood clauses

    # Common property & boundaries
    "common property": ["shared property", "owners corporation property", "body corporate property"],
    "exclusive use": ["special privilege", "exclusive privilege"],

    # Insurance
    "insurance": ["building insurance", "public liability insurance"],
    "insurance responsibilities": ["who insures", "insurance obligation"],

    # Funds & levies
    "levy": ["contribution", "strata fees"],
    "special levy": ["special contribution", "one-off levy"],
    "administrative fund": ["general fund", "admin fund"],
    "sinking fund": ["capital works fund", "reserve fund"],

    # Meetings, voting & governance
    "agm": ["annual general meeting"],
    "egm": ["extraordinary general meeting"],
    "ordinary resolution": ["simple majority"],
    "special resolution": ["75% resolution"],
    "unanimous resolution": ["100% resolution"],
    "quorum": ["meeting quorum"],
    "proxy": ["proxy vote"],
    "poll": ["vote by poll"],

    # Managers & committee
    "owners corporation": ["body corporate", "OC"],   # avoid generic "corporation"
    "executive committee": ["committee", "managing committee"],
    "manager": ["strata manager", "OC manager"],

    # Rules / by-laws
    "by-laws": ["rules", "strata rules"],

    # Disputes & orders
    "acat": ["tribunal", "ACT civil and administrative tribunal"],
    "dispute": ["complaint", "contravention"],
    "order": ["ACAT order", "compliance order"],

    # Access & entry
    "right of entry": ["access to unit", "entry to unit"],
    "records": ["OC records", "minutes", "register"],

    # Utilities / sustainability
    "utility infrastructure": ["services infrastructure", "water meters", "electricity meters"],
    "sustainability infrastructure": ["solar panels", "EV charging"],

    # Use of property / lifestyle
    "animals": ["pets"],
    "parking": ["car space", "visitor parking"],
    "nuisance": ["noise", "annoyance"],
}

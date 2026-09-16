#16/sept

COMPACTABLE_DONORS={
    'O-':  ['O-'],
    'O+':  ['O-', 'O+'],
    'A-':  ['O-', 'A-'],
    'A+':  ['O-', 'O+', 'A-', 'A+'],
    'B-':  ['O-', 'B-'],
    'B+':  ['O-', 'O+', 'B-', 'B+'],
    'AB-': ['O-', 'A-', 'B-', 'AB-'],
    'AB+': ['O-', 'O+', 'A-', 'A+', 'B-', 'B+', 'AB-', 'AB+'],
}

def get_compactable_donor_types(recipient_blood_group):
    """Given the blood type a recipient needs, return the list of donor
    blood types that are safe to give to them."""
    return COMPACTABLE_DONORS.get(recipient_blood_group, [])
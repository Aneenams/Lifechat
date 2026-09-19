from datetime import date, timedelta
from lifeapp.models import Profile

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


#19/sept

COOLDOWN_DAYS = 90

BADGE_THRESHOLDS = [
    (10, 'diamond'),
    (6, 'gold'),
    (3, 'silver'),
    (1, 'bronze'),
]

def calculate_badge_tier(verified_count):
    """Pure lookup: given a donation count, return the matching badge tier."""
    for threshold, tier in BADGE_THRESHOLDS:
        if verified_count >= threshold:
            return tier
    return 'none'

def apply_donation_cooldown(profile):
    """Called right after a donation is approved. Puts the donor into
    cooldown — sets when they'll be considered available again."""
    profile.blood_status = 'recently_donated'
    profile.donation_availability = date.today() + timedelta(days=COOLDOWN_DAYS)

def refresh_expired_cooldowns():
    """Bulk-flip any profile whose cooldown period has already passed
    back to 'available'. Call this at the start of any view that reads
    blood_status, so stale cooldowns don't linger past their expiry."""
    Profile.objects.filter(
        blood_status='recently_donated',
        donation_availability__lte=date.today(),
    ).update(blood_status='available', donation_availability=None)
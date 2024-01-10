from math import sin, cos, sqrt, atan2, pi
from utils.kidney_match_constants import A_NEGATIVE, A_POSITIVE, AB_NEGATIVE, AB_POSITIVE, B_NEGATIVE, B_POSITIVE, BLOOD_GROUP_WEIGHTAGE, EARTH_RADIUS, LOCATION_WEIGHTAGE, O_NEGATIVE, O_POSITIVE


def get_blood_group_compatability(receiver_blood_group, donor_blood_group):
    score = 0
    if receiver_blood_group == A_POSITIVE:
        if donor_blood_group in [A_POSITIVE, A_NEGATIVE, O_POSITIVE, O_NEGATIVE]:
            score += 10
        else:
            score += 0
    elif receiver_blood_group == A_NEGATIVE:
        if donor_blood_group in [A_NEGATIVE, O_NEGATIVE]:
            score += 10
        elif donor_blood_group in [A_POSITIVE, O_POSITIVE]:
            score += 9
        else:
            score += 0
    elif receiver_blood_group == B_POSITIVE:
        if donor_blood_group in [B_POSITIVE, B_NEGATIVE, O_POSITIVE, O_NEGATIVE]:
            score += 10
        else:
            score += 0
    elif receiver_blood_group == B_NEGATIVE:
        if donor_blood_group in [B_NEGATIVE, O_NEGATIVE]:
            score += 10
        elif donor_blood_group in [B_POSITIVE, O_POSITIVE]:
            score += 9
        else:
            score += 0
    elif receiver_blood_group == AB_POSITIVE:
        if donor_blood_group in [A_POSITIVE, B_POSITIVE, AB_POSITIVE, A_NEGATIVE, B_NEGATIVE, AB_NEGATIVE, O_POSITIVE, O_NEGATIVE]:
            score += 10
        else:
            score += 0
    elif receiver_blood_group == AB_NEGATIVE:
        if donor_blood_group in [A_NEGATIVE, B_NEGATIVE, O_NEGATIVE, AB_NEGATIVE]:
            score += 10
        elif donor_blood_group in [A_POSITIVE, B_POSITIVE, AB_POSITIVE, O_POSITIVE]:
            score += 9
    return score


def deg2rad(degree):
    return degree*(pi/180)


def get_location_compatability(receiver_location, donor_location):
    receiver_longitude, receiver_latitude = receiver_location
    donor_longitude, donor_latitude = donor_location
    latitude_in_degree = deg2rad(receiver_latitude - donor_latitude)
    longitude_in_degree = deg2rad(receiver_longitude - donor_longitude)

    a = sin(latitude_in_degree/2) * sin(latitude_in_degree/2) + cos(deg2rad(receiver_latitude)) * \
        cos(deg2rad(donor_latitude)) * \
        sin(longitude_in_degree/2) * sin(longitude_in_degree/2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    distance = EARTH_RADIUS * c

    score = 0
    if distance <= 100:
        score += 10
    elif distance <= 200:
        score += 8
    elif distance <= 300:
        score += 6
    elif distance <= 400:
        score += 4
    elif distance <= 500:
        score += 2
    else:
        score += 0
    return score


def get_viable_score(receiver_data, donor_data):
    score = get_blood_group_compatability(receiver_blood_group=receiver_data['blood_group'], donor_blood_group=donor_data['blood_group']) * BLOOD_GROUP_WEIGHTAGE 
    + get_location_compatability(receiver_location=receiver_data['location'], donor_location=donor_data['location']) * LOCATION_WEIGHTAGE
    return score

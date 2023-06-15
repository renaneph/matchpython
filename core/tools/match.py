from core.models.auxiliary_tables import Region, CLevel, CompanyIndustry, MatchKeysPoints
from django.shortcuts import get_object_or_404

def default_bool_check(startupkey, advisorkey):
    return (1, startupkey) if startupkey == advisorkey == True else (0, "")


def generic_list_check(startupkey, advisorkey):
    count = 0
    cases = []
    for i in startupkey:
        if i in advisorkey:
            count += 1
            cases.append(i)

    return count, cases


def match_routine(startup, advisor):
    match_points = 0
    match_cases = []

    # Parameters: startup key, advisor key, model to get points, especific list
    rules = [
        [
            "GTM-Strategy",
            "GTM-Strategy",
            MatchKeysPoints

        ],
        [
            "Sales-Business",
            "Sales-Business",
            Region,
            "Regions"
        ],
        [
            "C-level",
            "C-level",
            CLevel
        ],
        [
            "Fundraising",
            "Fundraising",
            MatchKeysPoints
        ],
        [
            "Tech",
            "Tech",
            MatchKeysPoints,
        ],
        [
            "Fintech",
            "Fintech",
            CompanyIndustry
        ],
        [
            "Commerce-Tech",
            "Commerce-Tech",
            CompanyIndustry
        ],
    ]

    for rule in rules:
        if rule[0] in ["C-level", "Fintech", "Commerce-Tech"]:
            count, cases = generic_list_check(startup[rule[0]], advisor[rule[1]])

        elif rule[0] == "Sales-Business":
            count, cases = generic_list_check(startup[rule[3]], advisor[rule[3]])

        else:
            count, cases = default_bool_check(startup[rule[0]], advisor[rule[1]])
            cases = [rule[0]]

        if count > 0:
            for key in cases:
                if rule[0] == "GTM-Strategy":
                    points = get_object_or_404(rule[2], gtm_name=key)
                    match_points += points.gtm_points

                elif rule[0] == "Fundraising":
                    points = get_object_or_404(rule[2], fundraising_name=key)
                    match_points += points.fundraising_points

                elif rule[0] == "Tech":
                    points = get_object_or_404(rule[2], tech_name=key)
                    match_points += points.tech_points

                else :
                    points = get_object_or_404(rule[2], name=key)
                    match_points += points.points
            match_cases.extend(cases)

    return match_points, match_cases


if __name__ == "__main__":
    from pathlib import Path
    import json

    BASE_DIR = Path(__file__).resolve().parent.parent.parent
    json_path = f'{BASE_DIR}/internal'

    startup_open = open(f'{json_path}/startups.json')
    advisor_open = open(f'{json_path}/advisors.json')

    startups = json.load(startup_open)
    advisors = json.load(advisor_open)

    for startup in startups:
        for advisor in advisors:
            result, cases = match_routine(startup[0], advisor[0])
            print("startup", startup[0])
            print("advisor", advisor[0])
            print(f'Match Points: {result}')
            print(f'Match Cases: {cases}')
            print('-='*30)
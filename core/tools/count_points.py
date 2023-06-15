from core.models.auxiliary_tables import Region, CLevel, CompanyIndustry, MatchKeysPoints

def countPoints(formated_match_keys):

    points = {
        'C-level' : {},
        'Fintech' : {},
        'Commerce-Tech' : {},
        'Regions' : {}
    }

    matchkeypoints = MatchKeysPoints.objects.first()
    clevels = CLevel.objects.all()
    companyindustry = CompanyIndustry.objects.all()
    regions = Region.objects.all()

    points['GTM-Strategy'] = matchkeypoints.gtm_points
    points['Fundraising'] = matchkeypoints.fundraising_points
    points['Tech'] = matchkeypoints.tech_points


    for clevel in clevels:
        points['C-level'][clevel.name] = clevel.points

    for company in companyindustry:
        if company.domain_id == 1:
            points['Fintech'][company.name] = company.points
        else:
            points['Commerce-Tech'][company.name] = company.points

    for region in regions:
        points['Regions'][region.name] = region.points

    count = 0

    if formated_match_keys.get('GTM-Strategy', False):
        count += points['GTM-Strategy']

    if formated_match_keys.get('Fundraising', False):
        count += points['Fundraising']

    if formated_match_keys.get('Tech', False):
        count += points['Tech']

    for clevel in formated_match_keys.get('C-level', []):
        count += points['C-level'].get(clevel, 0)

    for f in formated_match_keys.get('Fintech', []):
        count += points['Fintech'].get(f, 0)

    for c in formated_match_keys.get('Commerce-Tech', []):
        count += points['Commerce-Tech'].get(c, 0)

    for region in formated_match_keys.get('Regions', []):
        count += points['Regions'].get(region, 0)

    return count
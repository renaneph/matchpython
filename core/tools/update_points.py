from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser
from core.tools import count_points
from core.views.match import format_object


def updatePoints():

    advisors = AdvisorUser.objects.all()
    startups = StartupUser.objects.all()

    for advisor in advisors:
        formated_match_keys = format_object(advisor)
        count = count_points.countPoints(formated_match_keys)
        advisor.score = count
        advisor.save()
    
    for startup in startups:
        formated_match_keys = format_object(startup)
        count = count_points.countPoints(formated_match_keys)
        startup.score = count
        startup.save()

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db.models import Q
import json

from core.models.auxiliary_tables import Region, CLevel, CompanyIndustry, MatchKeysPoints

from django.db.models import Sum
from core.models.match import Match, MatchFiles
from core.models.advisor import AdvisorUser
from core.models.startup import StartupUser
from core.tools.match import match_routine
from core.forms.match import MatchFilesForm
from core.views.mail import email_connect_with_advisor, email_connect_with_startup


def format_object(obj):
    regions = set()
    if obj.international:
        regions.update([r.name for r in obj.regions_international.all()])
    if obj.domestic:
        regions.update([r.name for r in obj.regions_user.all()])

    clevels = []
    if obj.human_capital:
        clevels = [c.name for c in obj.c_level_user.all()]

    return {
        "GTM-Strategy": obj.gtm_strategy,
        "Sales-Business": {
            "International": obj.international,
            "Domestic": obj.domestic
        },
        "C-level": clevels,
        "Fundraising": obj.fundraising,
        "Tech": obj.tech,

        "Fintech": [f.name for f in obj.fintech_user.all()],
        "Commerce-Tech": [c.name for c in obj.commerce_tech_user.all()],
        "Regions": regions
    }

@login_required()
def match_list(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    matchs = Match.objects.all()
    advisors = AdvisorUser.objects.filter(enable_match=True, status=2).values("id", "user_id__first_name")
    startups = StartupUser.objects.filter(enable_match=True, status=2).values("id", "company_name")
    form = MatchFilesForm()

    if request.method == "POST":
        advisors_ids = request.POST.getlist("advisor-duallist", [])
        startups_ids = request.POST.getlist("startup-duallist", [])

        if not advisors_ids or not startups_ids:
            messages.warning(request, "Select at least 1 Advisor and 1 Startup")
        else:
            advisors_list = AdvisorUser.objects.filter(id__in=advisors_ids)
            startups_list = StartupUser.objects.filter(id__in=startups_ids)

            matchs = []
            region_max_points = Region.objects.aggregate(sum_scores=Sum('points'))
            clevel_max_points = CLevel.objects.aggregate(sum_scores=Sum('points'))
            company_industry_max_points = CompanyIndustry.objects.aggregate(sum_scores=Sum('points'))
            gtm_max_points = get_object_or_404(MatchKeysPoints, gtm_name='GTM-Strategy')
            fundrainsing_max_points = get_object_or_404(MatchKeysPoints, fundraising_name='Fundraising')
            tech_max_points = get_object_or_404(MatchKeysPoints, tech_name='Tech')

            max_score_result = region_max_points['sum_scores'] + clevel_max_points['sum_scores'] + company_industry_max_points['sum_scores'] \
            + gtm_max_points.gtm_points + fundrainsing_max_points.fundraising_points + tech_max_points.tech_points


            for ad in advisors_list:
                advisor = format_object(ad)

                for st in startups_list:
                    startup = format_object(st)
                    score, cases = match_routine(startup, advisor)
                    
                    if score <= 0:

                        matchstodelete = Match.objects.filter(advisor_id=ad.id, startup_id=st.id, closed=False)

                        if matchstodelete:
                            matchfiletodelete = MatchFiles.objects.filter(match_id_id=matchstodelete[0].id).delete()

                        matchstodelete.delete()

                    else:
                        matchsfromdb = Match.objects.filter(advisor_id=ad.id, startup_id=st.id)
                        
                        if matchsfromdb:
                            
                            for matchcheck in matchsfromdb:
                                
                                if matchcheck.closed == True:
                                    continue
                                
                                else :
                                    matchcheck.advisor=ad
                                    matchcheck.startup=st
                                    matchcheck.score=score
                                    matchcheck.cases=cases
                                    matchcheck.max_score=max_score_result

                                    matchcheck.save()
                                    matchs.append(matchcheck)
                                    break
                            else :

                                newmatch = Match.objects.create(advisor=ad, startup=st, score=score, cases=cases, max_score=max_score_result)
                                matchcheck.save()
                                matchs.append(matchcheck)
                        
                        else:
                            newmatch = Match.objects.create(advisor=ad, startup=st, score=score, cases=cases, max_score=max_score_result)
                            newmatch.save()
                            matchs.append(newmatch)
    else:
        messages.success(request, "Completed successfully")

    context = {
        "matchs": matchs,
        "advisors": advisors,
        "startups": startups,
        "form": form
    }

    return render(request, 'core/match/match_list.html', context)


def no_matches_list_for_user_id(user: AdvisorUser or StartupUser) -> list:
    """
    This function will look for users that do not match the user input parameter
    @param user: Startup or Advisor instance
    @return: List of unmatched users
    """

    if user.who_am_I == "Advisor":
        matches_from_user = Match.objects.filter(advisor__id=user.id)
        no_matches = StartupUser.objects.exclude(match__id__in=matches_from_user)
    else:
        matches_from_user = Match.objects.filter(startup__id=user.id)
        no_matches = AdvisorUser.objects.exclude(match__id__in=matches_from_user)
        
    return no_matches


## REVER
@login_required()
def matches_list_only(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    matches = Match.objects.all()
    advisors = AdvisorUser.objects.all()#enable_match=True, status=2).values("id", "user_id__first_name")
    startups = StartupUser.objects.all()#enable_match=True, status=2).values("id", "company_name")

    context = {
        "matches": matches,
        "advisors": advisors,
        "startups": startups,
    }
    return context

@login_required()
def match_list_for_startup(request):
    if not request.user.is_active:
        raise PermissionDenied

    advisor_list = []

    if request.method == "GET":
        advisor_list = match_list_for_startup_user_id(request.user.id)

    return advisor_list

def match_list_for_startup_user_id(id):
    advisor_list = []

    user_s = StartupUser.objects.get(user_id=id)

    if user_s.who_am_I == "Startup":
        matches = Match.objects.filter(startup__id=user_s.id).order_by('-score')

        for match in matches:
            advisor = {}
            advisor_user = AdvisorUser.objects.get(id=match.advisor.id)
            user = User.objects.get(id=match.advisor.user_id.id)
            advisor["platform_user"] = advisor_user
            advisor["user_form"] = user
            advisor["score"] = round(match.score / int(user_s.score) * 100)
            advisor["cases"] = match.cases
            advisor["id"] = match.id
            advisor["connected"] = match.connect_with_advisor
            advisor["closed"] = match.closed
            advisor_list.append(advisor)

    return advisor_list

@login_required()
def match_list_for_advisor(request):
    if not request.user.is_active:
        raise PermissionDenied

    startup_list = []
    if request.method == "GET":
        startup_list = match_list_for_advisor_user_id(request.user.id)

    return startup_list

def match_list_for_advisor_user_id(id):
    startups_list = []

    user_a = AdvisorUser.objects.get(user_id=id)

    if user_a.who_am_I == "Advisor":
        matches = Match.objects.filter(advisor__id=user_a.id).order_by("-score")

        for match in matches:
            startup = {}
            startup_user = StartupUser.objects.get(id=match.startup.id)
            user = User.objects.get(id=match.startup.user_id.id)
            startup["platform_user"] = startup_user
            startup["user_form"] = user
            startup["score"] = round(match.score / int(user_a.score) * 100)
            startup["cases"] = match.cases
            startup["id"] = match.id
            startup["connected"] = match.connect_with_startup
            startup["closed"] = match.closed
            startups_list.append(startup)

    return startups_list

@login_required()
def close_match(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    try:
        match = get_object_or_404(Match, id=pk)
        match.closed = not match.closed
        match.save()
    except Exception as error:
        print(error)
        return HttpResponse(json.dumps({"closed": False}), content_type="application/json")


    return HttpResponse(json.dumps({"closed": True}), content_type="application/json")

@login_required()
def connect_with_startup(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    try:
        match = get_object_or_404(Match, id=pk)
        match.connect_with_startup = not match.connect_with_startup
        match.save()
        email_connect_with_startup(
            match=match,
            host=str(request.get_host())
        )
    except Exception as error:
        print(error)
        return HttpResponse(json.dumps({"closed": False}), content_type="application/json")


    return HttpResponse(json.dumps({"closed": True}), content_type="application/json")

@login_required()
def connect_with_advisor(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    try:
        match = get_object_or_404(Match, id=pk)
        match.connect_with_advisor = not match.connect_with_advisor
        match.save()
        email_connect_with_advisor(
            match=match,
            host=str(request.get_host())
        )
    except Exception as error:
        print(error)
        return HttpResponse(json.dumps({"closed": False}), content_type="application/json")


    return HttpResponse(json.dumps({"closed": True}), content_type="application/json")

@login_required()
def get_match_files(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    match = get_object_or_404(Match, id=pk)
    files = MatchFiles.objects.filter(match_id=match)
    files_list = []
    for file in files:
        files_list.append({
            "id": file.id,
            "name": file.filename,
            "location": file.file.name,
            "created": file.created.strftime("%m/%d/%Y %H:%M"),
        })

    context = {
        "files": files_list,
        "startup_name": match.startup.company_name,
        "advisor_name": match.advisor.user_id.first_name
    }

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required()
def add_match_file(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    context = {}
    if request.method == "POST":
        form = MatchFilesForm(request.POST, request.FILES)
        if form.is_valid():
            match = get_object_or_404(Match, id=pk)
            file = form.save(commit=False)
            file.filename = str(request.FILES['file'])
            file.match_id = match

            file.save()

            context = {
                "name": file.filename,
                "location": file.file.name,
                "id": file.id,
                "created": file.created.strftime("%m/%d/%Y %H:%M")
            }

    return HttpResponse(json.dumps(context), content_type="application/json")

@login_required()
def del_match_file(request, pk):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    file = get_object_or_404(MatchFiles, id=pk)
    file.file.delete()
    file.delete()

    return HttpResponse(json.dumps({"del": True}), content_type="application/json")

@login_required()
def matches_closed(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    closed_matches_list = Match.objects.filter(closed=True)

    return closed_matches_list

@login_required()
def matches_interest_expressed(request):
    if not request.user.is_active and request.user.is_staff:
        raise PermissionDenied

    matches_interest_expressed_list = Match.objects.filter(Q(connect_with_startup=True) | Q(connect_with_advisor=True))

    return matches_interest_expressed_list

from django.urls import path

from core.views.advisor import advisor_list, advisor_form, advisor_edit, advisor_edit_from_home, advisor_delete, advisor_form_home
from core.views.c_level import c_level_list, c_level_form, c_level_edit, c_level_delete
from core.views.company_domain import (
    company_domain_list, company_domain_delete, company_domain_edit,
    company_domain_form
)
from core.views.company_industry import (
    company_industry_list, company_industry_form, company_industry_edit,
    company_industry_delete
)
from core.views.funding import funding_list, funding_form, funding_edit, funding_delete
from core.views.region import region_form, region_list, region_edit, region_delete
from core.views.startup import startup_form, startup_list, startup_edit, startup_edit_from_home, startup_delete, startup_form_home
from core.views.match import (
    match_list, close_match, connect_with_startup, connect_with_advisor,
    add_match_file, del_match_file, get_match_files
)
from core.views.match_keys_points import match_keys_points_edit
from core.views.testimonials import testimonials_list, testimonials_form, testimonials_edit, testimonials_delete
from core.views.interest_expressed import interest_expressed_list, interest_expressed_form, interest_expressed_edit, \
    interest_expressed_delete, interest_expressed_set
from core.views.terms_conditions import termsconditions_list, termsconditions_form, termsconditions_edit, termsconditions_delete

app_name = "core"

urlpatterns = [
    path("region/", region_list, name="region_list"),
    path("region/add/", region_form, name="region_create"),
    path("region/edit/<int:pk>/", region_edit, name="region_edit"),
    path("region/delete/<int:pk>/", region_delete, name="region_delete"),

    path("company-domain/", company_domain_list, name="company_domain_list"),
    path("company-domain/add/", company_domain_form, name="company_domain_create"),
    path("company-domain/edit/<int:pk>/", company_domain_edit, name="company_domain_edit"),
    path("company-domain/delete/<int:pk>/", company_domain_delete, name="company_domain_delete"),

    path("company-industry/", company_industry_list, name="company_industry_list"),
    path("company-industry/add/", company_industry_form, name="company_industry_create"),
    path("company-industry/edit/<int:pk>/", company_industry_edit, name="company_industry_edit"),
    path("company-industry/delete/<int:pk>/", company_industry_delete, name="company_industry_delete"),

    path("funding/", funding_list, name="funding_list"),
    path("funding/add/", funding_form, name="funding_create"),
    path("funding/edit/<int:pk>/", funding_edit, name="funding_edit"),
    path("funding/delete/<int:pk>/", funding_delete, name="funding_delete"),

    path("c-level/", c_level_list, name="c_level_list"),
    path("c-level/add/", c_level_form, name="c_level_create"),
    path("c-level/edit/<int:pk>/", c_level_edit, name="c_level_edit"),
    path("c-level/delete/<int:pk>/", c_level_delete, name="c_level_delete"),

    path("match-keys-points/edit/", match_keys_points_edit, name="match_keys_points_edit"),

    path("startup/", startup_list, name="startup_list"),
    path("startup/add/", startup_form, name="startup_create"),
    path("startup/add/home", startup_form_home, name="startup_create_home"),
    path("startup/edit/<int:pk>/", startup_edit, name="startup_edit"),
    path("startup/edit/home/<int:pk>/", startup_edit_from_home, name="startup_edit_from_home"),
    path("startup/delete/<int:pk>/", startup_delete, name="startup_delete"),

    path("advisor/", advisor_list, name="advisor_list"),
    path("advisor/add/", advisor_form, name="advisor_create"),
    path("advisor/add/home/", advisor_form_home, name="advisor_create_home"),
    path("advisor/edit/<int:pk>/", advisor_edit, name="advisor_edit"),
    path("advisor/edit/home/<int:pk>/", advisor_edit_from_home, name="advisor_edit_from_home"),
    path("advisor/delete/<int:pk>/", advisor_delete, name="advisor_delete"),

    path("match/", match_list, name="match_list"),
    path("match/close/<int:pk>/", close_match, name="close_match"),
    path("match/connect_with_startup/<int:pk>/", connect_with_startup, name="connect_with_startup"),
    path("match/connect_with_advisor/<int:pk>/", connect_with_advisor, name="connect_with_advisor"),
    path("match/get_match_files/<int:pk>/", get_match_files, name="get_match_files"),
    path("match/del_match_file/<int:pk>/", del_match_file, name="del_match_file"),
    path("match/add_match_file/<int:pk>/", add_match_file, name="add_match_file"),

    path("testimonials/", testimonials_list, name="testimonials_list"),
    path("testimonials/add/", testimonials_form, name="testimonials_create"),
    path("testimonials/edit/<int:pk>/", testimonials_edit, name="testimonials_edit"),
    path("testimonials/delete/<int:pk>/", testimonials_delete, name="testimonials_delete"),

    path("interest-expressed/", interest_expressed_list, name="interest_expressed_list"),
    path("interest-expressed/add/", interest_expressed_form, name="interest_expressed_create"),
    path("interest-expressed/edit/<int:pk>/", interest_expressed_edit, name="interest_expressed_edit"),
    path("interest-expressed/delete/<int:pk>/", interest_expressed_delete, name="interest_expressed_delete"),
    path("interest_expressed/interest_expressed_set/", interest_expressed_set, name="interest_expressed_set"), 
    #path("interest_expressed/interest_expressed_set/<str:pk>/", interest_expressed_set, name="interest_expressed_set"),

    path("termsconditions/", termsconditions_list, name="termsconditions_list"),
    path("termsconditions/add/", termsconditions_form, name="termsconditions_create"),
    path("termsconditions/edit/<int:pk>/", termsconditions_edit, name="termsconditions_edit"),
    path("termsconditions/delete/<int:pk>/", termsconditions_delete, name="termsconditions_delete"),
]

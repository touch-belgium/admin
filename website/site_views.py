from django.http import HttpResponse
from django.utils.html import escape
from django.template import loader
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import now
from django.contrib import messages
from fuzzywuzzy import fuzz

from .models import BelgianClub, Registration, TBMember


def create_tb_member(reg):
    """Creates and saves a new TBMember from the Registration object.

    """
    new_member = TBMember.objects.create(
        name=reg.name,
        dob=reg.dob,
        email=reg.email,
        club=reg.club,
        guardian_name=reg.guardian_name,
        guardian_email=reg.guardian_email,
        media_consent=reg.media_consent,
        registration_start_date=reg.reviewed_at,
        license_number=reg.license_number
    )
    new_member.save()


def similar_to_registered_member(name):
    """Returns true if the name passed as argument already looks like a
    name in the database

    """
    return max(list(map(lambda p: fuzz.ratio(p.name, name),
                        TBMember.objects.all()))) >= 80


def registrations(request, token):
    template = loader.get_template('registrations/index.html')
    not_found = loader.get_template('registrations/not_found.html')
    try:
        club = BelgianClub.objects.get(token=token)
        registrations = Registration.objects.filter(club=club, status="P")
        context = {
            'club': club,
            'registrations': registrations
        }
        return HttpResponse(template.render(context, request))
    except ObjectDoesNotExist:
        return HttpResponse(not_found.render({'token': token}, request))


def registrations_approve(request):
    reg = Registration.objects.get(id=request.POST["registration_id"])
    reg.reviewed_at = now()
    if similar_to_registered_member(reg.name):
        reg.status = "M"
    else:
        reg.status = "A"
        create_tb_member(reg)

    reg.save()
    messages.add_message(request, messages.SUCCESS,
                         "Player {} has been approved".format(reg.name))
    return redirect(request.headers["Referer"])


def registrations_reject(request):
    reg = Registration.objects.get(email=request.POST["registration_email"])
    reg.status = "R"
    reg.reviewed_at = now()
    reg.save()
    messages.add_message(request, messages.ERROR,
                         "Registration for player {} has been rejected".format(reg.name))
    return redirect(request.headers["Referer"])


def registrations_usage(request):
    return HttpResponse(escape("Usage: admin.touch-belgium.be/registrations/<team-token>"))

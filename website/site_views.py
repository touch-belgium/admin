from django.http import HttpResponse
from django.utils.html import escape
from django.template import loader
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist

from .models import Club, Registration


def registrations(request, token):
    template = loader.get_template('registrations/index.html')
    not_found = loader.get_template('registrations/not_found.html')
    try:
        club = Club.objects.get(token=token)
        registrations = Registration.objects.filter(club=club)
        context = {
            'club': club,
            'registrations': registrations
        }
        return HttpResponse(template.render(context, request))
    except ObjectDoesNotExist:
        return HttpResponse(not_found.render({'token': token}, request))


def registrations_approve(request):
    return redirect(request.headers["Referer"])


def registrations_reject(request):
    return redirect(request.headers["Referer"])


def registrations_usage(request):
    return HttpResponse(escape("Usage: admin.touch-belgium.be/registrations/<team-token>"))

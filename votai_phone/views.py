
from django.views.generic import View
from django.http import HttpResponse
from elections.models import Election, Topic
from django.conf import settings
from tropo import Tropo
from django.views.decorators.csrf import csrf_exempt


class MediaNaranjaView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MediaNaranjaView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        election = Election.objects.get(id=settings.PHONE_ELECTION_ID)
        tropo = Tropo()
        tropo.say(u"Hola. Vamos a comenzar la media naranja", voice=u"Soledad")
        topics = Topic.objects.filter(category__in=election.categories.all())
        for t in topics:
            choices = u""
            say_value = t.label + u" Presione "
            choice_counter = 1
            for p in t.positions.all():
                if choice_counter != 1:
                    choices += ", "
                choices += "%(choice_counter)s(%(position_id)s)" % {'position_label': p.label,
                                                                    'choice_counter': choice_counter,
                                                                    'position_id': p.id
                                                                    }
                say_value += "%(choice_counter)s para %(position_label)s" % {'position_label': p.label,
                                                                             'choice_counter': choice_counter
                                                                             }
                if choice_counter == t.positions.count() - 1:
                    say_value += " y "
                if choice_counter < t.positions.count() - 1:
                    say_value += ", "

                choice_counter += 1

            tropo.ask(choices=choices,
                  mode="dtmf",
                  timeout=60,
                  name=str(p.id),
                  say=say_value,
                  voice=u"Soledad")
        return HttpResponse(tropo.RenderJson())

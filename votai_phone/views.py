# coding=utf-8
from django.views.generic import View
from django.http import HttpResponse
from elections.models import Election, Topic
from candidator.models import Position
from django.conf import settings
from tropo import Tropo, Result
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse


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
                choices += "%(position_id)s(%(choice_counter)s)" % {'position_label': p.label,
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
                      mode="any",
                      timeout=90,
                      name=str(t.id),
                      say=say_value,
                      voice=u"Soledad",
                      attempts=3
                      )
            tropo.on('continue', next=reverse('phone_medianaranja_save'))
            tropo.on('incomplete', next=reverse('phone_medianaranja_problem'))
            tropo.on('error', next=reverse('phone_medianaranja_problem'))
            tropo.on('hangup', next=reverse('phone_medianaranja_problem'))
        return HttpResponse(tropo.RenderJson())


class MediaNaranjaTropoResult(Result):
    def getActionsLen(self):
        return len(self._actions)

    def getTopicId(self, index=0):
        """
        Get the value of the previously POSTed Tropo action.
        """
        actions = self._actions

        if (type(actions) is list):
            dict = actions[index]
        else:
            dict = actions
        # return dict['value'] Fixes issue 17
        return int(dict['name'])

# # **Tue May 17 07:17:38 2011** -- egilchri

    def getPositionId(self, index=0):
        """
        Get the value of the previously POSTed Tropo action.
        """
        actions = self._actions

        if (type(actions) is list):
            dict = actions[index]
        else:
            dict = actions
        return int(dict['value'])


class MediaNaranjaResponseView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MediaNaranjaResponseView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        r = MediaNaranjaTropoResult(request.body)
        for counter in range(0, r.getActionsLen()):
            t = Topic.objects.get(id=r.getTopicId(counter))
            p = Position.objects.get(id=r.getPositionId(counter))
        t = Tropo()
        answer = r.getInterpretation()
        value = r.getValue()
        t.say("You said " + answer + ", which is a " + value)
        return HttpResponse(t.RenderJson())


class MediaNaranjaProblemView(View):
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(MediaNaranjaProblemView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        r = Result(request.body)
        t = Tropo()
        t.say(u"Ocurrió un error")
        return HttpResponse(t.RenderJson())

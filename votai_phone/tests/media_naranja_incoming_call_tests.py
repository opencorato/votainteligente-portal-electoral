# coding=utf-8
from elections.tests import VotaInteligenteTestCase as TestCase
from elections.models import Election
from candidator.models import Position
import json
from django.core.urlresolvers import reverse
from django.test import override_settings


phone_election_id = 1


@override_settings(PHONE_ELECTION_ID=phone_election_id)
class CandidateInElectionsViewsTestCase(TestCase):
    maxDiff = None

    def setUp(self):
        super(CandidateInElectionsViewsTestCase, self).setUp()
        self.tarapaca = Election.objects.get(id=phone_election_id)

    def test_say_hello_and_read_questions(self):
        expected_answer = {
            u"tropo": [{u"say": {u"value": u"Hola. Vamos a comenzar la media naranja",
                                 u"voice": u"Soledad"
                                 }},
                       {u"ask": {u"say": {u"value": u"Le gusta la Fiera?? Presione 1 para Si, 2 para No y 3 para A veces"},
                                 u"timeout": 60,
                                 u"name": u"3",
                                 u"voice": u"Soledad",
                                 u"choices": {u"value": u"1(1), 2(2), 3(3)"}
                                 }},
                       # [<Position: <Si> to <Le gusta Benito??>>, <Position: <no> to <Le gusta Benito??>>]
                       {u"ask": {u"say": {u"value": u"Le gusta Benito?? Presione 1 para Si y 2 para no"},
                                 u"timeout": 60,
                                 u"name": u"5",
                                 u"voice": u"Soledad",
                                 u"choices": {u"value": u"1(4), 2(5)"}
                                 }},
                       # [<Position: <Si> to <Libre para todos??>>, <Position: <no> to <Libre para todos??>>]
                       {u"ask": {u"say": {u"value": u"Libre para todos?? Presione 1 para Si y 2 para no"},
                                 u"timeout": 60,
                                 u"name": u"7",
                                 u"voice": u"Soledad",
                                 u"choices": {u"value": u"1(6), 2(7)"}
                                 }}
                       ]
        }

        phone_answer = self.client.post(reverse('phone_medianaranja'))
        self.assertEquals(phone_answer.status_code, 200)
        self.assertEquals(json.loads(phone_answer.content), expected_answer)
        # topics = Topic.objects.filter(category__in=self.tarapaca.categories.all())
        # for t in topics:
        #     print t
        #     print t.positions.all()
        # self.fail()

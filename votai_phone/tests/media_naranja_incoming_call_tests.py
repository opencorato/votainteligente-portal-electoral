# coding=utf-8
from elections.tests import VotaInteligenteTestCase as TestCase
from elections.models import Election
import json
from django.core.urlresolvers import reverse
from django.test import override_settings
from votai_phone.views import MediaNaranjaTropoResult


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
                                 u"timeout": 90,
                                 u"name": u"1",
                                 u"voice": u"Soledad",
                                 u"attempts": 3,
                                 u"choices": {u"value": u"1(1), 2(2), 3(3)"}
                                 }},
                       {u'on': {u'event': u'continue',
                                u'next': u'/phone/phone_medianaranja_save'}},
                       {u'on': {u'event': u'incomplete',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'error',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'hangup',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       # [<Position: <Si> to <Le gusta Benito??>>, <Position: <no> to <Le gusta Benito??>>]
                       {u"ask": {u"say": {u"value": u"Le gusta Benito?? Presione 1 para Si y 2 para no"},
                                 u"timeout": 90,
                                 u"name": u"2",
                                 u"voice": u"Soledad",
                                 u"attempts": 3,
                                 u"choices": {u"value": u"4(1), 5(2)"}
                                 }},
                       {u'on': {u'event': u'continue',
                                u'next': u'/phone/phone_medianaranja_save'}},
                       {u'on': {u'event': u'incomplete',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'error',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'hangup',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       # [<Position: <Si> to <Libre para todos??>>, <Position: <no> to <Libre para todos??>>]
                       {u"ask": {u"say": {u"value": u"Libre para todos?? Presione 1 para Si y 2 para no"},
                                 u"timeout": 90,
                                 u"name": u"3",
                                 u"voice": u"Soledad",
                                 u"attempts": 3,
                                 u"choices": {u"value": u"6(1), 7(2)"}
                                 }},
                       {u'on': {u'event': u'continue',
                                u'next': u'/phone/phone_medianaranja_save'}},
                       {u'on': {u'event': u'incomplete',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'error',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       {u'on': {u'event': u'hangup',
                                u'next': u'/phone/phone_medianaranja_problem'}},
                       ]
        }

        phone_answer = self.client.post(reverse('phone_medianaranja'))
        self.assertEquals(phone_answer.status_code, 200)
        self.assertEquals(json.loads(phone_answer.content), expected_answer)

    def test_post_result(self):
        url = reverse('phone_medianaranja_save')
        result_json = {'sessionDuration': 10,
                       'calledid': '9991464188',
                       'complete': True,
                       'sequence': 1,
                       'callId': 'cf64a1a785f8326340f0559e4c3aee2f',
                       'state': 'ANSWERED',
                       'actions': [{'xml': '<?xml version="1.0"?>\r\n<result grammar="0@387e5862.vxmlgrammar">\r\n    <interpretation grammar="0@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '1',
                       'interpretation': '1',
                       'name': '1',
                       'value': '1',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'},
                       {'xml': '<?xml version="1.0"?>\r\n<result grammar="1@387e5862.vxmlgrammar">\r\n    <interpretation grammar="1@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '5',
                       'interpretation': '1',
                       'name': '2',
                       'value': '4',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'}, {'xml': '<?xml version="1.0"?>\r\n<result grammar="2@387e5862.vxmlgrammar">\r\n    <interpretation grammar="2@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '9',
                       'interpretation': '1',
                       'name': '3',
                       'value': '6',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'}],
                       'sessionId': '814ddcea73a9167bf8880ccbaa77e45f',
                       'error': None}
        data = {'result': result_json}
        result = self.client.post(url, content_type='application/json', data=json.dumps(data))
        self.assertEquals(result.status_code, 200)

    def test_medianaranja_iterpreter(self):
        result_json = {'sessionDuration': 10,
                       'calledid': '9991464188',
                       'complete': True,
                       'sequence': 1,
                       'callId': 'cf64a1a785f8326340f0559e4c3aee2f',
                       'state': 'ANSWERED',
                       'actions': [{'xml': '<?xml version="1.0"?>\r\n<result grammar="0@387e5862.vxmlgrammar">\r\n    <interpretation grammar="0@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '1',
                       'interpretation': '1',
                       'name': '1',
                       'value': '1',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'},
                       {'xml': '<?xml version="1.0"?>\r\n<result grammar="1@387e5862.vxmlgrammar">\r\n    <interpretation grammar="1@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '5',
                       'interpretation': '1',
                       'name': '2',
                       'value': '5',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'}, {'xml': '<?xml version="1.0"?>\r\n<result grammar="2@387e5862.vxmlgrammar">\r\n    <interpretation grammar="2@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '9',
                       'interpretation': '1',
                       'name': '3',
                       'value': '9',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'}, {'xml': '<?xml version="1.0"?>\r\n<result grammar="3@387e5862.vxmlgrammar">\r\n    <interpretation grammar="3@387e5862.vxmlgrammar" confidence="100">\r\n        \r\n      <input mode="dtmf">dtmf-1</input>\r\n    </interpretation>\r\n</result>\r\n',
                       'confidence': 100,
                       'concept': '13',
                       'interpretation': '1',
                       'name': '4',
                       'value': '13',
                       'attempts': 1,
                       'disposition': 'SUCCESS',
                       'utterance': '1'}],
                       'sessionId': '814ddcea73a9167bf8880ccbaa77e45f',
                       'error': None}

        result = MediaNaranjaTropoResult(json.dumps({'result': result_json}))
        # name is topic_id
        # value es the answer_id
        # 'interpretation': '1','name': '4','value': '1'
        # 'interpretation': '2','name': '8','value': '6'
        # 'interpretation': '3', 'name': '12', 'value': '11'
        # 'interpretation': '4', 'name': '16', 'value': '16'
        self.assertEquals(result.getTopicId(0), 1)
        self.assertEquals(result.getPositionId(0), 1)
        self.assertEquals(result.getTopicId(1), 2)
        self.assertEquals(result.getPositionId(1), 5)
        self.assertEquals(result.getTopicId(2), 3)
        self.assertEquals(result.getPositionId(2), 9)
        self.assertEquals(result.getTopicId(3), 4)
        self.assertEquals(result.getPositionId(3), 13)

        self.assertEquals(result.getActionsLen(), 4)

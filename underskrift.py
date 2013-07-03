from base64 import b64encode
from cStringIO import StringIO
import json
import mimetypes
import uuid
import os
import requests

__author__ = 'jens'


class UnderskriftException(Exception):
    pass


class Underskrift(object):

    _latest_response = None

    def __init__(self, username, password, environment="https://secure.underskrift.se/apiv1/"):
        self.username = username
        self.password = password
        self.environment = environment

    def get_latest_response(self):
        return self._latest_response

    def create_case(self,
                    name,
                    parties,
                    documents,
                    case_reference_id=None,
                    allowed_signature_types=("touch", "electronicId", "sms"),
                    continue_url=None,
                    continue_name=None,
                    continue_auto=False,
                    send_sign_request_email_to_parties=False,
                    send_finish_email_to_creator=False,
                    send_finish_email_to_parties=False,
                    send_recall_email_to_parties=False
                    ):
        """
        use according to https://secure.underskrift.se/apiv1
        parties takes an array of dicts, each dict should be (example):
            {
                "Name":"party name",
                "EmailAddress" : "email@party.com",
                "SocialSecurityNumber": "19121212-1212",
            }
        documents takes an array of files which will be encoded
        """
        if not case_reference_id:
            case_reference_id = str(uuid.uuid4())
        files = []
        for document in documents:
            document.seek(0)
            file_content = document.read()
            path, filename = os.path.split(document.name)
            mime_type, encoding = mimetypes.guess_type(document.name, strict=False)
            files.append({
                "Filename": filename,
                "Data": b64encode(file_content),
                "Size": len(file_content),
                "ContentType": mime_type
            })
        self._make_request("createcasecommand", params={
            "CaseReferenceId": case_reference_id,
            "Name": name,
            "Parties": parties,
            "Documents": files,
            "AllowedSignatureTypes": allowed_signature_types,
            "ContinueUrl": continue_url,
            "ContinueAuto": continue_auto,
            "ContinueName": continue_name,
            "SendSignRequestEmailToParties": send_sign_request_email_to_parties,
            "SendFinishEmailToCreator": send_finish_email_to_creator,
            "SendFinishEmailToParties": send_finish_email_to_parties,
            "SendRecallEmailToParties": send_recall_email_to_parties
        })

        return case_reference_id

    def get_case_url(self, case_id):
        return self._make_request(location="getviewcaseurlquery", params={"CaseReferenceID": case_id}).text

    def get_case_info(self, case_id):
        return self._make_request(location="getcaseinfoquery", params={"CaseReferenceID": case_id}).json()

    def get_case_list_info(self, from_date=None, to_date=None, case_status=None):
        return self._make_request(location="getcaseinfolistquery", params={
            "FromDate": from_date.isoformat(),
            "ToDate": to_date.isoformat(),
            "CaseStatus": case_status
        }).json()

    def remove_case(self, case_id):
        self._make_request(location="removecasecommand", params={"CaseReferenceID": case_id})

    def get_document(self, document_id):
        request = self._make_request(location="getdocumentquery", params={"DocumentId": document_id})
        return StringIO(request.content)

    def _make_request(self, location="", params=None):
        json_params = json.dumps(params) if params else ""

        response = requests.post(
            "%s%s" % (self.environment, location),
            auth=(self.username, self.password),
            data = json_params,
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        )

        self._latest_response = response

        if response.status_code == 200:
            return response

        # If not 200 something went wrong (underskrift.se always returns 200 according to documentation
        raise UnderskriftException(response.text)

from datetime import date, timedelta
import unittest
import uuid
from underskrift import Underskrift, UnderskriftException


class TestUnderskrift(unittest.TestCase):

    def setUp(self):
        self.underskrift = Underskrift(
            username="jens.alm@prorenata.se",
            password="TG7mqHVdABiz8CBkRQUaPH",
            environment="https://x-test.underskrift.se/apiv1/"
        )

    def test_create_read_and_remove_case(self):

        # Create case
        with open("test.pdf", "rb") as document:
            case_id = str(uuid.uuid1())
            self.underskrift.create_case(
                name=u"Testavtal",
                parties=[{
                    "Name": u"Teste Tetsson",
                    "EmailAddress": u"test@prorenata.se"
                }],
                documents=[document],
                case_reference_id=case_id,
            )
            self.assertEqual(self.underskrift.get_latest_response().status_code, 200)

            # Get case url
            case_url = self.underskrift.get_case_url(case_id=case_id)
            self.assertEqual(self.underskrift.get_latest_response().status_code, 200)
            self.assertTrue(case_url.startswith("http"))

            # Get case info
            case_info = self.underskrift.get_case_info(case_id=case_id)
            self.assertEqual(self.underskrift.get_latest_response().status_code, 200)
            self.assertEqual(case_info["Parties"][0]["Name"], u"Teste Tetsson")

            # Get case info list
            case_list_info = self.underskrift.get_case_list_info(
                from_date=date.today() - timedelta(days=1),
                to_date=date.today() + timedelta(days=1)
            )
            self.assertEqual(case_list_info[0]["Parties"][0]["Name"], u"Teste Tetsson")

            # Get document
            document_file = self.underskrift.get_document(case_info["Documents"][0]["Id"])
            document.seek(0)
            self.assertEqual(document_file.read(), document.read())

            # Remove case
            self.underskrift.remove_case(case_id=case_id)
            self.assertEqual(self.underskrift.get_latest_response().status_code, 200)

            # Fail to get case url from removed case
            with self.assertRaises(UnderskriftException):
                self.underskrift.get_case_info(case_id=case_id)

if __name__ == '__main__':
    unittest.main()
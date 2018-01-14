import uuid
import requests

from lxml import etree
from signxml import XMLSigner

from .data_store import DataStore
from .auth_config import DemoAuthConfig
from .data import DemoAuthData
from .const import LANGUAGES


class DemoAuthRequest():
    def __init__(self, aadhaar_number, demo_details, device_details, lang, config_file_path=None):
        self.aadhaar_number = aadhaar_number
        self.demo_details = demo_details
        self.device_details = device_details
        self.lang = lang
        self.lang_code = LANGUAGES.get(self.lang, '')
        self.cfg = DemoAuthConfig(config_file_path=config_file_path).setup()
        self.__txn = None

    def __setup_auth_data(self):
        self.data = DemoAuthData(cfg=self.cfg, uid=self.aadhaar_number, demo_details=self.demo_details, lang=self.lang_code)
        self.data.set_skey()
        self.data.set_data()
        self.data.set_hmac()

    def __get_txn__(self):
        if not self.__txn:
            self.__txn = uuid.uuid4().hex
        return self.__txn

    def __setup_xml_request(self):
        auth_node = etree.Element(
            "Auth",
            {
                'uid': self.aadhaar_number,
                'tid': self.cfg.common.tid,
                'ac': self.cfg.common.ac,
                'sa': self.cfg.common.sa,
                'ver': self.cfg.common.ver,
                'txn': self.__get_txn__(),
                'lk': self.cfg.common.license_key,
            }
        )
        # Uses Node
        etree.SubElement(auth_node, 'Uses', self.data.uses)
        # Meta Node
        etree.SubElement(auth_node, 'Meta', {
            'udc': self.device_details.get('unique_id', 'NA'),
            'fdc': self.device_details.get('fdc', 'NA'),
            'idc': self.device_details.get('fdc', 'NA'),
            'pip': self.device_details.get('ip', 'NA'),
            'lot': self.device_details.get('lot', 'NA'),
            'lov': self.device_details.get('lov', 'NA'),
        })
        # Session key Node
        skey_details = self.data.skey
        session_key_node = etree.SubElement(auth_node, 'Skey', {
            'ci': skey_details['cert_expiry'],
        })
        session_key_node.text = skey_details['text']

        # Data Node
        data_node = etree.SubElement(auth_node, 'Data', {'type': 'X'})
        data_node.text = self.data.data

        # HMAC node
        hmac_node = etree.SubElement(auth_node, 'Hmac')
        hmac_node.text = self.data.hmac
        self.request_xml_root = auth_node

        DataStore(self.aadhaar_number, self.__get_txn__(), self.cfg).store_raw_request(
                  auth_node)

    def __sign_auth_xml(self):
        aua_cer_file = self.cfg.common.aua_cer_file
        aua_private_key_file = self.cfg.common.aua_private_key_file

        with open(aua_cer_file) as f:
            cert = f.read()
        with open(aua_private_key_file) as f:
            private_key = f.read()
        private_key_passphrase = self.cfg.common.aua_private_key_file_passphrase

        self.request_xml_signed_root = XMLSigner().sign(self.request_xml_root, private_key, private_key_passphrase, cert)

        DataStore(self.aadhaar_number, self.__get_txn__(), self.cfg).store_signed_request(
                  self.request_xml_signed_root)

    def send_request(self):
        self.__setup_auth_data()
        self.__setup_xml_request()
        self.__sign_auth_xml()

        request_content = etree.tostring(self.request_xml_signed_root, encoding='UTF-8', xml_declaration=True)
        url = "{auth_url}/{first_digit}/{second_digit}/{key}".format(
            auth_url=self.cfg.common.auth_url,
            first_digit=self.aadhaar_number[0],
            second_digit=self.aadhaar_number[1],
            key=self.cfg.common.license_key
        )
        response = requests.post(
            url,
            request_content
        )
        DataStore(self.aadhaar_number, self.__get_txn__(), self.cfg).store_response(
                  response.content)
        return response

import os
from lxml import etree


class DataStore:
    def __init__(self, aadhaar_num, txn, cfg):
        self.aadhaar_num = aadhaar_num
        self.txn = txn
        self.cfg = cfg

    def dir_name(self):
        return "%s-%s" % (self.txn, self.aadhaar_num)

    def logs_path(self):
        try:
            return self.cfg.logs.location
        except AttributeError:
            return os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "logs/")

    def dir_path(self):
        return self.logs_path() + self.dir_name()

    def signed_request_file(self):
        return self.dir_path() + '/signed_request.xml'

    def raw_request_file(self):
        return self.dir_path() + '/raw_request.xml'

    def response_file(self):
        return self.dir_path() + '/response.xml'

    def ensure_dir(self):
        dir_path = self.dir_path()
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

    def store_raw_request(self, root_node):
        self.ensure_dir()
        with open(self.raw_request_file(), 'w+') as f:
            f.write(etree.tostring(root_node, encoding='UTF-8',
                                   xml_declaration=True, pretty_print=True))

    def store_signed_request(self, root_node):
        self.ensure_dir()
        with open(self.signed_request_file(), 'w+') as f:
            f.write(etree.tostring(root_node, encoding='UTF-8',
                                   xml_declaration=True, pretty_print=True))

    def store_response(self, xml_content):
        self.ensure_dir()
        with open(self.signed_request_file(), 'w+') as f:
            f.write(xml_content)

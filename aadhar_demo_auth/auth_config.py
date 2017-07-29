import os
from config import Config
from .exceptions import (
    RequiredDocumentMissing,
    InvalidConfiguration,
)


class DemoAuthConfig:
    """
    This sets the configuration for the auth process which includes all
    authentication specific details and path to various certificates and key files
    """
    def __init__(self, config_file_path=None):
        """
        :param config_file_path: Path to file to load custom config. Refer fixtures/auth.cfg for example.
        """
        if config_file_path:
            self.config_file_path = config_file_path
        else:
            # Find path to fixtures relative to this file
            self.fixtures_dir_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "fixtures/")
            self.config_file_path = self.fixtures_dir_path + "auth.cfg"
        # look for seeded certs and keys under fixtures if custom config file is not provided
        self.locate_docs_in_fixtures = not bool(config_file_path)

    @property
    def required_docs(self):
        return ['private_key', 'public_cert', 'uid_cert_path',
                'aua_cer_file', 'aua_private_key_file']

    def _update_docs_paths(self, cfg):
        certs_path = self.fixtures_dir_path + 'certs/'
        for doc in self.required_docs:
            if cfg.common.get(doc):
                cfg.common[doc] = certs_path + cfg.common[doc]

    def _ensure_required_docs(self, cfg):
        for doc in self.required_docs:
            try:
                file_path = cfg.common[doc]
                if not os.path.isfile(file_path):
                    raise RequiredDocumentMissing("Could not locate %s at %s" % (doc, file_path))
            except KeyError:
                raise InvalidConfiguration("Could not ensure document for config %s" % doc)

    def setup(self):
        # Read the configuration file
        cfg = Config(self.config_file_path)

        # update path to docs in case of default config
        if self.locate_docs_in_fixtures:
            self._update_docs_paths(cfg)
        self._ensure_required_docs(cfg)
        return cfg

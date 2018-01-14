from setuptools import setup, find_packages

setup(
    name='aadhaar_demo_auth',
    version='0.1',
    description='Demo Auth for aadhaar Authentication',
    url='http://github.com/dimagi/aadhaar-demo-auth',
    author='Dimagi',
    author_email='mkangia@dimagi.com',
    packages=find_packages(exclude=['*.pyc']),
    include_package_data=True,
    package_data={
        'aadhaar_demo_auth': ['fixtures/*', 'fixtures/certs/*']
    },
    install_requires=[
      'requests==2.10.0',
      'lxml==3.5.0',
      'signxml==2.3.0',
      'config==0.3.9',
      # https://gist.github.com/charlax/38ecd925a8bcb8cadcf5
      # https://github.com/pyca/cryptography/issues/3489#issuecomment-291749772
      # https://gitlab.com/m2crypto/m2crypto/blob/master/INSTALL.rst#id5
      'm2crypto==0.26.0',
    ],
)

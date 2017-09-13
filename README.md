Aadhar Demo Auth
===========

Aadhar Demo Auth provides the basic hook to interact with UIDAI API(1.6). It takes care of creating the request packet,
sending it to UIDAI and then parsing the response.
One can validate Aadhar Number against demographic details only.

### Certificates
There are a bunch of certificates used for creating the request package which needs to be added.
+ For UIDAI
  + Public Certificate to sign the session key used during encryption of pid block
+ For AUA/Sub-AUA (Authentication User Agency) i.e the system making the request
  + Private Key
  + Public Certificate
    to sign the final XML request

All test certificates provided by UIDAI are already included to perform requests and get started on integration without
any setup.

### Licences
A bunch of licences provided by UIDAI and also from AUA in case of a sub-AUA making request
that need to be added on each request to identify the requesting client
+ Licence Key: provided to AUA/Sub-AUA to be sent with each request
+ AC: a unique code for the AUA assigned by UIDAI
+ SA: a unique code for the Sub-AUA assigned by AUA (in case of AUA requesting this would be same as AC)

### Integration for all languages supported by UIDAI
+ Assamese
+ Bengali
+ Gujarati
+ Hindi
+ Kannada
+ Malayalam
+ Manipuri
+ Marathi
+ Oriya
+ Punjabi
+ Tamil
+ Telugu
+ Urdu

### Example Usage:

    >>> from aadhar_demo_auth.authenticate import AuthenticateAadharDemographicDetails
    >>> AuthenticateAadharDemographicDetails(
    ...             "999922220078",
    ...             {"Pi": {"name": "Kishore Shah", "lname": u"????? ???", "gender": "M", "dob": "1987-05-21", "dobt": "V"}},
    ...             {'ip': '127.0.0.1', 'unique_id': 'unique_id', 'lov': '110002', 'lot': 'P'},
    ...             'Hindi',
    ...         ).authenticate()
    True

    You can also set your own configuration file and pass that to be used for
    all certs and licenses.
    Notice the change in name for result in mismatch/failure

    >>> cfg_file_path = "/path/to/my/aadhar_conf.cfg"
    >>> AuthenticateAadharDemographicDetails(
    ...             "999922220078",
    ...             {"Pi": {"name": "Kishore Kumar", "gender": "M", "dob": "1987-05-21", "dobt": "V"}},
    ...             {'ip': '127.0.0.1', 'unique_id': 'unique_id', 'lov': '110002', 'lot': 'P'},
    ...             config_file_path=cfg_file_path
    ...         ).authenticate()
    False

    You can also run quick check to ensure you are set up well

    >>> AuthenticateAadharDemographicDetails.test_request()
    1. For Successful Match:
    Matched successfully.
    2. For Unsuccessful Match:
    Match failed as expected.
    3. For A Failure Response:
    Exception to be raised with error code 902. Got error: 902.

    Ultimately you would want to set your own configuration. The custom configuration
    need to be built on same structure as the default config file present
    at aadhar_demo_auth/fixtures/auth.cfg. The path to your custom file can be passed to bring it into play.
    Please note that when adding your own config the path to certificates should be full paths and not relative to avoid surprises.
    Again a quick check to ensure you are all set.

    >>> AuthenticateAadharDemographicDetails.test_request(config_file_path=cfg_file_path)
    1. For Successful Match:
    Matched successfully.
    2. For Unsuccessful Match:
    Match failed as expected.
    3. For A Failure Response:
    Exception to be raised with error code 902. Got error: 902.

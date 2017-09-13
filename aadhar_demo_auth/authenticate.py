# -*- coding: utf-8 -*-
from lxml import etree, objectify

from .request import DemoAuthRequest
from .exceptions import AadharAuthException
from .const import (
    SUCCESSFUL_MATCH_RESPONSE,
    UNSUCCESSFUL_MATCH_RESPONSE,
    UNSUCCESSFUL_MATCH_ERROR_CODDE,
)


class AuthenticateAadharDemographicDetails(object):
    def __init__(self, aadhar_number, demo_details, device_details, lang=None):
        self.request = DemoAuthRequest(aadhar_number, demo_details, device_details, lang)

    def authenticate(self):
        response = self.request.send_request()
        return self.__parse_response__(response)

    def __successful_match__(self, response_ret_value):
        return response_ret_value == SUCCESSFUL_MATCH_RESPONSE

    def __unsuccessful_match__(self, response_ret_value, response_err_value):
        # err code 100 corresponds to mismatch in Pi details which is expected
        # in case the authenticate fails. Just checking for 'n' is not enough
        # because the API returns 'n' in case of all error codes
        return (
            response_ret_value == UNSUCCESSFUL_MATCH_RESPONSE and
            response_err_value == UNSUCCESSFUL_MATCH_ERROR_CODDE
        )

    def __parse_response__(self, response):
        response_xml = objectify.fromstring(response.content)

        success_response = response_xml.get('ret')
        error_code = response_xml.get('err')
        if self.__successful_match__(success_response):
            return True
        elif self.__unsuccessful_match__(success_response, error_code):
            return False
        elif error_code:
            raise AadharAuthException(
                "Got error: {error_code}".format(error_code=error_code)
            )
        else:
            raise AadharAuthException(
                'Unexpected response received'
            )

    @classmethod
    def test_request(cls):
        print '1. For Successful Match:'
        response = AuthenticateAadharDemographicDetails(
            "999922220078",
            {"Pi": {"name": "Kishore Shah", "lname": u"किशोर शाह", "gender": "M", "dob": "1987-05-21", "dobt": "V"}},
            {'ip': '127.0.0.1', 'unique_id': 'unique_id', 'lov': '110002', 'lot': 'P'},
            'Hindi'
        ).authenticate()
        if response is True:
            print 'Matched successfully.'
        else:
            print 'Test Failed!!'

        print '2. For Unsuccessful Match:'
        response = AuthenticateAadharDemographicDetails(
            "999922220078",
            {"Pi": {"name": "Kishore Kumar", "gender": "M", "dob": "1987-05-21", "dobt": "V"}},
            {'ip': '127.0.0.1', 'unique_id': 'unique_id', 'lov': '110002', 'lot': 'P'}
        ).authenticate()
        if response is False:
            print 'Match failed as expected.'
        else:
            print 'Test Failed!!'

        print '3. For A Failure Response:'
        try:
            print AuthenticateAadharDemographicDetails(
                "999922220078",
                {"Pi": {"name": "Kishore Shah", "gender": "M", "dob": "1987-05-32", "dobt": "V"}},
                {'ip': '127.0.0.1', 'unique_id': 'unique_id', 'lov': '110002', 'lot': 'P'}
            ).authenticate()
            print 'Test Failed!!'
        except AadharAuthException as e:
            print "Exception to be raised with error code 902. %s." % e.message

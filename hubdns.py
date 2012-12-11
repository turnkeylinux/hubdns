# 
# Copyright (c) 2011 Alon Swartz <alon@turnkeylinux.org>
# 
# This file is part of HubDNS.
# 
# HubDNS is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
# 
from pycurl_wrapper import API

class HubDNS:
    """API interface to access the TurnKey Hub API for HubDNS"""
    Error = API.Error

    API_URL = 'https://hub.turnkeylinux.org/api/hubdns/'

    def __init__(self, apikey=None, subkey=None):
        self.apikey = apikey
        self.subkey = subkey
        self.api = API()

    def _api(self, method, uri, attrs={}):
        headers = {}
        if self.apikey:
            headers['apikey'] = self.apikey
        if self.subkey:
            headers['subkey'] = self.subkey
        return self.api.request(method, self.API_URL + uri, attrs, headers)

    def get_subkey(self):
        """Get hubdns API subkey"""
        response = self._api('GET', 'subkey/')
        self.subkey = response['subkey']

        return self.subkey

    def get_ipaddress(self, fqdn):
        """Get IP address associated with FQDN"""
        response = self._api('GET', 'ipaddress/', {'fqdn': fqdn})
        return response['ipaddress']

    def capture(self, fqdn):
        """Capture FQDN but don't set IP address of client (only TKLAPP.com)"""
        self._api('POST', 'capture/', {'fqdn': fqdn})
        
    def release(self, fqdn):
        """Release DNS records associated with FQDN (only TKLAPP.com)"""
        self._api('DELETE', 'release/', {'fqdn': fqdn})

    def update(self, fqdn):
        """Update FQDN with IP address of client"""
        response = self._api('PUT', 'update/', {'fqdn': fqdn})
        return response['ipaddress']


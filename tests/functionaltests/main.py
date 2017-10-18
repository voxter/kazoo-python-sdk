#!/usr/bin/env python
import kazoo
import unittest
import pprint
import random


class FunctionalTest(unittest.TestCase):
    def auth(self, username=None, password=None, account_name=None, base_url=None):
        if username is not None:
            self.username = username
        else:
            self.username = ''

        if password is not None:
            self.password = password
        else:
            self.password = ''

        if account_name is not None:
            self.account_name = account_name
        else:
            self.account_name = ''

        if base_url is not None:
            self.base_url = base_url
        else:
            self.base_url = 'http:'

        client = kazoo.Client(username=self.username, password=self.password, account_name=self.account_name,
                              base_url=self.base_url)
        client.authenticate()
        return client

    def testAuth(self):
        self.client = self.auth()
        self.assertGreater(len(self.client.account_id),0)

class DeviceTest(FunctionalTest):
    def test_0_CreateDevice(self):
        DeviceTest.client = FunctionalTest.auth(self)
        data={}
        DeviceTest.a_name = 'SDKTest'+str(random.randint(100,1000))
        data['name']= DeviceTest.a_name
        DeviceTest.a_device = DeviceTest.client.create_device(DeviceTest.client.account_id,data)
        self.assertGreater(len(DeviceTest.a_device['data']['id']),0)

    def test_1_FetchDevice(self):
        test_data = DeviceTest.client.get_device(DeviceTest.client.account_id,DeviceTest.a_device['data']['id'])
        self.assertEqual(DeviceTest.a_name, test_data['data']['name'])

    def test_2_UpdateDevice(self):
        DeviceTest.a_name = 'SDKTest'+str(random.randint(100,1000))
        data = {}
        data['name'] = DeviceTest.a_name
        DeviceTest.client.update_device(DeviceTest.client.account_id,DeviceTest.a_device['data']['id'], data)
        test_data = DeviceTest.client.get_device(DeviceTest.client.account_id, DeviceTest.a_device['data']['id'])
        self.assertEqual(DeviceTest.a_name, test_data['data']['name'])

    def test_3_DeviceListing(self):
        data = DeviceTest.client.get_devices(DeviceTest.client.account_id)
        self.assertEqual(len(data['data']), 1)

    def test_8_RemoveDevice(self):
        DeviceTest.client.delete_device(DeviceTest.client.account_id,DeviceTest.a_device['data']['id'])
        data = DeviceTest.client.get_devices(DeviceTest.client.account_id)
        self.assertEqual(len(data['data']), 0)

'''
    def testFetcDeviceFilter(self):
        test_data = DeviceTest.client.get_device(DeviceTest.client.account_id,DeviceTest.a_device['data']['id'])
        self.assertEqual(DeviceTest.a_name, test_data['data']['name'])

    def testDeviceListing(self):
        test_data = DeviceTest.client.get_device(DeviceTest.client.account_id,DeviceTest.a_device['data']['id'])
        self.assertEqual(DeviceTest.a_name, test_data['data']['name'])
'''

if __name__ == '__main__':
    unittest.main(verbosity=3)

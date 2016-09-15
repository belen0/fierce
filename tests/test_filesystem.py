#!/usr/bin/env python

import os
import textwrap
import unittest

import dns.resolver

from pyfakefs import fake_filesystem_unittest

import fierce


class TestFilesystem(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()

    def tearDown(self):
        # It is no longer necessary to add self.tearDownPyfakefs()
        pass

    def test_update_resolver_nameservers_empty_no_file(self):
        nameserver_filename = None
        nameservers = []

        resolver = dns.resolver.Resolver()

        expected = resolver.nameservers

        result = fierce.update_resolver_nameservers(
            resolver,
            nameservers,
            nameserver_filename
        )

        self.assertEqual(expected, result.nameservers)

    def test_update_resolver_nameservers_single_nameserver_no_file(self):
        nameserver_filename = None
        nameservers = ['192.168.1.1']

        resolver = dns.resolver.Resolver()

        result = fierce.update_resolver_nameservers(
            resolver,
            nameservers,
            nameserver_filename
        )

        expected = nameservers
        self.assertEqual(expected, result.nameservers)

    def test_update_resolver_nameservers_multiple_nameservers_no_file(self):
        nameserver_filename = None
        nameservers = ['192.168.1.1', '192.168.1.2']

        resolver = dns.resolver.Resolver()

        result = fierce.update_resolver_nameservers(
            resolver,
            nameservers,
            nameserver_filename
        )

        expected = nameservers
        self.assertEqual(expected, result.nameservers)

    def test_update_resolver_nameservers_no_nameserver_use_file(self):
        nameserver_filename = os.path.join("directory", "nameservers")
        nameservers = []
        contents = textwrap.dedent("""nameserver1
        nameserver2
        nameserver3
        """)

        self.fs.CreateFile(
            nameserver_filename,
            contents=contents
        )

        resolver = dns.resolver.Resolver()

        result = fierce.update_resolver_nameservers(
            resolver,
            nameservers,
            nameserver_filename
        )

        expected = contents.split()
        self.assertEqual(expected, result.nameservers)

    def test_update_resolver_nameservers_prefer_nameservers_over_file(self):
        nameserver_filename = os.path.join("directory", "nameservers")
        nameservers = ['192.168.1.1', '192.168.1.2']
        contents = textwrap.dedent("""nameserver1
        nameserver2
        nameserver3
        """)

        self.fs.CreateFile(
            nameserver_filename,
            contents=contents
        )

        resolver = dns.resolver.Resolver()

        result = fierce.update_resolver_nameservers(
            resolver,
            nameservers,
            nameserver_filename
        )

        expected = nameservers
        self.assertEqual(expected, result.nameservers)


if __name__ == "__main__":
    unittest.main()
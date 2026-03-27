import unittest

import quickstream
from quickstream.base import test_registry


class TestProviders(unittest.IsolatedAsyncioTestCase):
    async def test_providers(self):
        for url, expected in test_registry.items():
            with self.subTest(url=url):
                actual = await quickstream.extract(url)
                base = {k: v for k, v in actual.items() if k != 'stream'}
                self.assertEqual(base, expected)
                self.assertIsNotNone(actual['stream'])

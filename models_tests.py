#!/usr/bin/env python

import unittest
import cql
import models

class ModelsTestCase(unittest.TestCase):
    session = None

    def setUp(self):
        self.session = cql.session()
        models.init(self.session)
    
    def tearDown(self):
        models.teardown(self.session)

    def test_add_films(self):
        models.Films.objects.create(
            id="1",
            title="Film",
            episode_id=1,
            director="Director",
            producer="Producer",
            release_date="2017-01-01")
        self.assertEqual(1, models.Films.objects.count())

if "__main__" == __name__:
    unittest.main()
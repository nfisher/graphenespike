#!/usr/bin/env python

import cql
import models

def migrate():
    sess = cql.session()
    models.init(sess)

if "__main__" == __name__:
    migrate()
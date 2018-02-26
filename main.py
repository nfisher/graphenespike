#!/usr/bin/env python

import cql
import flask_graphql as graphql
import tracer
import models
import routes
import schema

def main():
    tracer.instance(routes.app)
    sess = cql.session()
    models.init(sess)
    view = graphql.GraphQLView.as_view(
        'graphql',
        schema=schema.schema,
        middleware=[tracer.middleware],
        graphiql=True,
        graphiql_template=schema.HTML)
    routes.app.add_url_rule("/graphql", view_func=view)
    routes.app.run(use_reloader=True, threaded=True)

if "__main__" == __name__:
    main()

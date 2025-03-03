import strawberry
from strawberry.fastapi import GraphQLRouter
from .query import Query

schema = strawberry.Schema(query=Query)

graphql_app = GraphQLRouter(schema)
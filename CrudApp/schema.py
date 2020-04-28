import graphene
from crud.schema import Query as query, Mutation as mutation

class Query(query, graphene.ObjectType):
    pass


class Mutation(mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

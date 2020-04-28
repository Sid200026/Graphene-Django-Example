import graphene
from graphene_django.types import DjangoObjectType
from .models import Country, State

# Transforms a Django model into an object type.
# A Graphene ObjectType is the building block used to define the 
# relationship between Fields in your Schema and how their data is retrieved.
class CountryType(DjangoObjectType):
    class Meta:
        model = Country

class StateType(DjangoObjectType):
    class Meta:
        model = State

# The input which will map the incoming query to python data type
class CountryInput(graphene.InputObjectType):
    id = graphene.Int()

# Input required to create Country
class CreateCountryInput(graphene.InputObjectType):
    name = graphene.String()
    continent = graphene.String()

# Inputs required to update Country
class UpdateCountryInput(graphene.InputObjectType):
    name = graphene.String()
    continent = graphene.String()

class StateInput(graphene.InputObjectType):
    id = graphene.Int()

class CreateStateInput(graphene.InputObjectType):
    name = graphene.String()

class UpdateStateInput(graphene.InputObjectType):
    name = graphene.String()

class Query:
    countries = graphene.List(CountryType, id=graphene.Int(), name=graphene.String(), continent_name=graphene.String())
    states = graphene.List(StateType, id=graphene.Int(), name=graphene.String(), country_name=graphene.String())

    def resolve_countries(self, info, **kwargs):
        countries = Country.objects.all()
        if kwargs.get("id"):
            countries = countries.filter(pk=kwargs.get("id"))
        if kwargs.get("name"):
            countries = countries.filter(name__icontains=kwargs.get("name"))
        if kwargs.get("continent_name"):
            countries = countries.filter(continent__icontains=kwargs.get("continent_name"))
        return countries
    
    def resolve_states(self, info, **kwargs):
        states = State.objects.all()
        if kwargs.get("id"):
            states = states.filter(pk=kwargs.get("id"))
        if kwargs.get("name"):
            states = states.filter(name__icontains=kwargs.get("name"))
        if kwargs.get("country_name"):
            states = states.filter(country__name__icontains=kwargs.get("country_name"))
        return states


class CreateState(graphene.Mutation):
    class Arguments:
        input = CreateStateInput(required=True)
        country = CountryInput(required=True)
    
    state = graphene.Field(StateType)
    errors = graphene.String()

    def mutate(self, info, country=None, input=None):
        country = Country.objects.filter(pk=country.id).first()
        if country is None:
            return CreateState(state=None, errors="Country does not exist")
        state = State(name=input.name, country=country)
        state.save()
        return CreateState(state=state, errors=None)


class UpdateState(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = CreateStateInput()
        country = CountryInput()
    
    state = graphene.Field(StateType)
    errors = graphene.String()

    def mutate(self, info, id,country=None, input=None):
        state = State.objects.filter(pk=id).first()
        if state is None:
            return UpdateState(state=None, errors="State does not exist")
        if country:
            country = Country.objects.filter(pk=country.id).first()
            if country is None:
                return UpdateState(state=None, errors="Country does not exist")
            state.country = country
        if input.name:
            state.name = input.name
        state.save()
        return UpdateState(state=state, errors=None)


class DeleteState(graphene.Mutation):
    class Arguments:
        input = StateInput(required=True)
    
    id = graphene.Int()
    errors = graphene.String()

    def mutate(self, info, input):
        state = State.objects.filter(pk=input.id).first()
        if state is None:
            return DeleteState(id=None, errors="State does not exist")
        state.delete()
        return DeleteState(id=input.id, errors=None)

class CreateCountry(graphene.Mutation):
    class Arguments:
        input = CreateCountryInput(required=True)
    
    country = graphene.Field(CountryType)
    errors = graphene.String()

    def mutate(self, info, input=None):
        country = Country.objects.filter(name=input.name).first()
        if country is not None:
            return CreateCountry(country=None, errors="Country already exists")
        country = Country(name=input.name, continent=input.continent)
        country.save()
        return CreateCountry(country=country, errors=None)
    
class UpdateCountry(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = UpdateCountryInput(required=True)
    
    country = graphene.Field(CountryType)
    errors = graphene.String()

    def mutate(self, info, id, input=None):
        country = Country.objects.filter(pk=id).first()
        if country is None:
            return UpdateCountry(country=None, errors="Country does not exists")
        countryTest = Country.objects.filter(name=input.name).first()
        if countryTest is not None:
            return UpdateCountry(country=None, errors="Country already exists")
        if input.name:
            country.name = input.name
        if input.continent:
            country.continent = input.continent
        country.save()
        return UpdateCountry(country=country, errors=None)

class DeleteCountry(graphene.Mutation):
    class Arguments:
        input = CountryInput(required=True)
    
    id = graphene.Int()
    errors = graphene.String()

    def mutate(self, info, input):
        country = Country.objects.filter(pk=input.id).first()
        if country is None:
            return DeleteCountry(id=None, errors="Country does not exist")
        country.delete()
        return DeleteCountry(id=input.id, errors=None)
    
class Mutation(graphene.ObjectType):
    create_state = CreateState.Field()
    update_state = UpdateState.Field()
    delete_state = DeleteState.Field()

    create_country = CreateCountry.Field()
    update_country = UpdateCountry.Field()
    delete_country = DeleteCountry.Field()


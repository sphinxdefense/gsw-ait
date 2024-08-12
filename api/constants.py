from enum import Enum


class ApiSpecTags(Enum):
    OTHER = "other"


# Uncommenting this will raise exceptions any time a lazy load of related objects happens.
# This is useful for finding N+1 query problems.
# TODO: find and fix N+1 queries.
sa_relationship_kwargs = (
    dict()
)  # dict(lazy="raise_on_sql") if Settings().ENVIRONMENT == Environment.DEVELOPMENT else dict()

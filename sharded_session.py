from sqlalchemy import create_engine
import os

shards = {
    'read': create_engine(os.environ.get("DATABASE_REPLICA_URL")),
    'write': create_engine(os.environ.get("DATABASE_URL"))
}

shard_lookup = {
    "read": "read",
    "write": "write",
}


def shard_chooser(mapper, instance, clause=None):
    """shard chooser.
    By default returns write since that's the main DB."""
    return "write"


def id_chooser(query, ident):
    """id chooser.

    given a primary key, returns a list of shards
    to search.  here, we don't have any particular information from a
    pk so we just return all shard ids. often, you'd want to do some
    kind of round-robin strategy here so that requests are evenly
    distributed among DBs.
    Adjusted from https://docs.sqlalchemy.org/en/14/_modules/examples/sharding/attribute_shard.html
    """
    if query.lazy_loaded_from:
        # if we are in a lazy load, we can look at the parent object
        # and limit our search to that same shard, assuming that's how we've
        # set things up.
        return [query.lazy_loaded_from.identity_token]
    else:
        return ["read", "write"]


def execute_chooser(query):
    """execute chooser.

    this also returns a list of shard ids, which can
    just be all of them.
    Adjusted from https://docs.sqlalchemy.org/en/14/_modules/examples/sharding/attribute_shard.html
    """
    return ["write"]

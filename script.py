from models import Session, Category


def query_categories():
    session = Session()

    categories = session.query(Category).limit(10)

    for category in categories:
        print(
            {"id": category.id, "name": category.name, "parent_id": category.parent_id}
        )


def query_categories_shard():
    session = Session()

    categories_query = session.query(Category).set_shard("read")
    categories = categories_query.limit(10)

    for category in categories:
        print(
            {"id": category.id, "name": category.name, "parent_id": category.parent_id}
        )


def add_category():
    category = Category(name="lalala2")

    try:
        session.add(category)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def update_category():
    session = Session()
    category = session.query(Category).get(1)

    category.name = "updated lalala"

    try:
        session.add(category)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def delete_category():
    session = Session()
    category = session.query(Category).get(1)

    try:
        session.delete(category)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    # query_categories()
    query_categories_shard()
    # add_category()
    # update_category()
    delete_category()

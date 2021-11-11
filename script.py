from models import Session, Category, CategorySchema


def query_categories():
    session = Session()
    print(session.get_bind())

    categories = session.query(Category).order_by(Category.id).offset(10).limit(10)

    # formatted = CategorySchema(many=True).dump(categories)

    # print(formatted)


def query_categories_shard():
    session = Session()

    categories = session.query(Category).set_shard("read").order_by(Category.id).offset(10).limit(10)

    formatted = CategorySchema(many=True).dump(categories)

    print(formatted)

    # for category in categories:
    #     print(
    #         {"id": category.id, "name": category.name, "parent_id": category.parent_id}
    #     )


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
    query_categories()
    query_categories_shard()
    # add_category()
    # update_category()
    # delete_category()

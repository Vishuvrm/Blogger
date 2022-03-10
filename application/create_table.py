import sqlalchemy as sa

def create_table(name, uri, db):
    # Create table user if it doesn't exists
    engine = sa.create_engine(uri)
    insp = sa.inspect(engine)
    if name not in insp.get_table_names():
        db.create_all()
        print(f"Created table {name}")
    else:
        print(f"Table {name} already exists")
        print(list(insp.get_table_names()))
from orm import *

def populate():
    admin = User('Ivan', 'ivan@pochta.ua', '12345678', True)
    db.session.add(admin)
    user = User('Ivan', 'ivan1@pochta.ua', '12345678', False)
    db.session.add(user)
    user1 = User('Ivan', 'ivan2@pochta.ua', '12345678', False)
    db.session.add(user1)
    db.session.commit()
    bigint = DataType('postgresql', 'bigint', 'bigint')
    db.session.add(bigint)
    integer = DataType('postgresql', 'integer', 'integer')
    db.session.add(integer)
    smallint = DataType('postgresql', 'smallint', 'smallint')
    db.session.add(smallint)
    text = DataType('postgresql', 'text', 'text')
    db.session.add(text)
    boolean = DataType('postgresql', 'boolean', 'boolean')
    db.session.add(boolean)
    bigint = DataType('cassandra', 'bigint', 'bigint')
    db.session.add(bigint)
    integer = DataType('cassandra', 'int', 'integer')
    db.session.add(integer)
    smallint = DataType('cassandra', 'smallint', 'smallint')
    db.session.add(smallint)
    text = DataType('cassandra', 'text', 'text')
    db.session.add(text)
    boolean = DataType('cassandra', 'boolean', 'boolean')
    db.session.add(boolean)

    typeEntity = DatabaseEntity('postgresql', 'useddefineddatatype')
    dataTable = DatabaseEntity('postgresql', 'datatable')
    db.session.add(typeEntity)
    db.session.add(dataTable)
    typeEntity = DatabaseEntity('cassandra', 'useddefineddatatype')
    dataTable = DatabaseEntity('cassandra', 'datatable')
    db.session.add(typeEntity)
    db.session.add(dataTable)

    migration = Migration(
        'postgresql',
        'cassandra',
        'https://drive.google.com/file/d/11eVsd2BJt5VAye6YwhX3KKalTb-jOApK/view?usp=sharing',
        'https://drive.google.com/file/d/1rJKM07l_O0ppa2xltse3text7vo-HjCf/view?usp=sharing',
        'https://drive.google.com/file/d/16OT-OjRQfLKvYqa5-cRuQ8K3EiOjbYMI/view?usp=sharing',
        user.id
    )

    migration2 = Migration(
        'postgresql',
        'cassandra',
        'https://drive.google.com/file/d/11eVsd2BJt5VAye6YwhX3KKalTb-jOApK/view?usp=sharing',
        'https://drive.google.com/file/d/1rJKM07l_O0ppa2xltse3text7vo-HjCf/view?usp=sharing',
        'https://drive.google.com/file/d/16OT-OjRQfLKvYqa5-cRuQ8K3EiOjbYMI/view?usp=sharing',
        user.id
    )

    migration3 = Migration(
        'postgresql',
        'cassandra',
        'https://drive.google.com/file/d/11eVsd2BJt5VAye6YwhX3KKalTb-jOApK/view?usp=sharing',
        'https://drive.google.com/file/d/1rJKM07l_O0ppa2xltse3text7vo-HjCf/view?usp=sharing',
        'https://drive.google.com/file/d/16OT-OjRQfLKvYqa5-cRuQ8K3EiOjbYMI/view?usp=sharing',
        user.id
    )

    db.session.add(migration)
    db.session.add(migration2)
    db.session.add(migration3)

    op1 = Operation('mysql', 'createtable')
    op2 = Operation('oracle', 'createtable')
    op3 = Operation('cassandra', 'createtable')

    db.session.add(op1)
    db.session.add(op2)
    db.session.add(op3)

    db.session.commit()

    s1 = Syntax('mysql', 'CREATE TABLE(\s+|)(.*)\);', op1.id)
    s2 = Syntax('oracle', 'CREATE TABLE(\s+|)(.*)\);', op2.id)
    s3 = Syntax('cassandra', 'CREATE TABLE(\s+|)(.*)\);', op3.id)

    db.session.add(s1)
    db.session.add(s2)
    db.session.add(s3)

    oco1 = OperationContainsOperation(op1.id, op2.id)
    oco2 = OperationContainsOperation(op1.id, op3.id)
    oco3 = OperationContainsOperation(op2.id, op3.id)

    db.session.add(oco1)
    db.session.add(oco2)
    db.session.add(oco3)

    oude1 = OperationUseDatabaseEntity(op1.id, typeEntity.id)
    oude2 = OperationUseDatabaseEntity(op2.id, typeEntity.id)
    oude2 = OperationUseDatabaseEntity(op2.id, typeEntity.id)

    db.session.add(oude1)
    db.session.add(oude2)
    db.session.add(oude2)

    db.session.commit()
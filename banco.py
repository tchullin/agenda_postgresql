import psycopg2


def ConexaoBanco():
    con = None
    try:
        con = psycopg2.connect(host='localhost',
                               database='agenda',
                               user='postgres',
                               password='lu050161')
    except Exception as ex:
        print(ex)
    return con

def dql(query): # select
    vcon=ConexaoBanco()
    c=vcon.cursor()
    c.execute(query)
    res=c.fetchall()
    vcon.close()
    return res

def dml(query): # insert , update, delete
    try:
        vcon = ConexaoBanco()
        c=vcon.cursor()
        c.execute(query)
        vcon.commit()
        vcon.close()
        vcon=ConexaoBanco()
    except Exception as ex:
        print(ex)

import sqlite3
import datetime

#Verifica se ja existe arquivo importado com a compentencia / cnpj declarante
def checarduplicidade(cnpj, competencia):
    list_delete = []
    sqliteConnection = sqlite3.connect("DataBase.db")
    cursor = sqliteConnection.cursor()
    delete = sqliteConnection.cursor()
    sql = (
        "Select count(*) from EFD_0000 WHERE CNPJ_DECLARANTE = '"
        + cnpj
        + "' AND COMPETENCIA = "
        + competencia
    )
    count = cursor.execute(sql)
    qtd = int(cursor.fetchall()[0][0])

    if qtd > 0:
        list_delete = []
        sql = (
            "select 'delete from ' || name || ' where CNPJ_DECLARANTE = "
            + cnpj
            + " and COMPETENCIA = "
            + competencia
            + ";' from sqlite_master where type = 'table' and tbl_name like 'EFD_%';"
        )
        
        count = cursor.execute(sql)

        for rows in cursor:
            delete.execute(rows[0])
            
        sqliteConnection.commit()
    sqliteConnection.close()


#faz o Insert no Banco com arquivo EFD
def insert(sql):
    sqliteConnection = sqlite3.connect("DataBase.db")
    cursor = sqliteConnection.cursor()
    count = cursor.executescript(sql)
    print("Registros Inseridos com Sucesso")
    cursor.close()
    print(datetime.datetime.now())


# abre Arquivo .txt do Sped Fiscal
def lerarquivo(caminho):
    print(datetime.datetime.now())

    with open(caminho) as f:

        lin = 1
        lines = f.readlines()
        cnpj = lines[0].split("|")[7]
        competencia = lines[0].split("|")[4]

        checarduplicidade(cnpj, competencia)

        tabela = lines[0].split("|")[1]
        StrSQL = ""
        idnotapai = 0
        registrospai = [
            "A100"
            "C100",
            "C300",
            "C400",
            "C500",
            "C600",
            "C700",
            "C800",
            "D100",
            "D200",
            "D300",
            "D400",
            "D600",
            "D700",
        ]

        # Enquanto houver linhas repete o Looping
        for x in lines:

            colunas = x.split("|")
            tabela = colunas[1]

            if tabela in registrospai:
                idnotapai = lin

            StrSQL = (
                StrSQL
                + "INSERT INTO EFD_"
                + tabela
                + " VALUES('"
                + cnpj
                + "','"
                + competencia
                + "','"
                + str(lin)
                + "','"
                + str(idnotapai)
                + "',"
            )

            for i in range(1, len(colunas) - 2):
                StrSQL = StrSQL + "'" + colunas[i].replace(",", ".") + "',"

            StrSQL = StrSQL + "'" + colunas[i + 1] + "');\n"
            lin = lin + 1
            #print(StrSQL)

    insert(StrSQL)

#Chama a função principal
lerarquivo("Arquivos/SpedFiscal.txt")

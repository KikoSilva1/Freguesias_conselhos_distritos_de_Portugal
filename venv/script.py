import csv
import mysql.connector

# MySQL Connection Configuration
""" mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'jdep'
} """

mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mypassword',
    'database': 'testdb'
}

try:
    # Establish MySQL Connection
    connection = mysql.connector.connect(**mysql_config)

    # Create a Cursor
    cursor = connection.cursor()

    # Read Data from CSV File
    csv_file_path = 'freguesias.csv'  # Replace with your CSV file name

    conselhos = []
    distritos = []
    id_concelho_atual = 0
    id_distrito_atual = 0
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=';')

        
        # Assuming the first row of the CSV file contains column headers
        header = next(csv_reader)
        
        for row in csv_reader:
            print(row)
            # Atualiza a tabela distritos
            distrito = row[1]
            if distrito not in distritos:
                distritos.append(distrito)
                cursor.execute('INSERT INTO distritos (nome) VALUES (%s)', (distrito,))
                id_distrito_atual +=1  

            # Atualiza a tabela concelhos
            conselho = row[2]
            if conselho not in conselhos:
                conselhos.append(conselho)
                cursor.execute('INSERT INTO concelhos (nome, id_distrito) VALUES (%s, %s)', (conselho, id_distrito_atual))
                id_concelho_atual +=1  

            # Atualiza a tabela freguesias
            cursor.execute('INSERT INTO freguesias (nome , id_concelho) VALUES (%s, %s)', (row[3], id_concelho_atual)) 

except mysql.connector.Error as e:
    # Se houver um erro ao abrir a conexão com o MySQL, exiba uma mensagem de alerta
    print(f"Erro ao abrir a conexão com o MySQL: {e}")

        
finally:

    # Commit Changes and Close Connections
    connection.commit()
    cursor.close()
    connection.close()

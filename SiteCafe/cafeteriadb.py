import sqlite3


def criar_banco():
    with sqlite3.connect('produtos.db') as conn:
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS cafes (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS lanches (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS marmitas_fits (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT NOT NULL,
                            preco REAL NOT NULL)''')

        cursor.executemany("INSERT INTO cafes (nome, preco) VALUES (?, ?)",
                        [("Café Expresso", 5.00),
                            ("Café com Leite", 6.50),
                            ("Capuccino", 8.00)])

        cursor.executemany("INSERT INTO lanches (nome, preco) VALUES (?, ?)",
                        [("Pão de Queijo", 4.00),
                            ("Croissant", 7.00),
                            ("Torrada com Requeijão", 6.00)])

        cursor.executemany("INSERT INTO marmitas_fits (nome, preco) VALUES (?, ?)",
                        [("Frango com Batata Doce", 15.00),
                            ("Salada Completa", 12.00),
                            ("Omelete Proteico", 10.00)])
        conn.commit()
        conn.close()


if __name__ == "__main__":
    criar_banco()
    print("Banco de dados criado e populado com sucesso!")

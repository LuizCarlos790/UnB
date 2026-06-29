from conexao import get_connection, close_connection

def inserir_usuario(nome, email, senha, id_departamento=None):
    """CREATE: Insere um usuário base.
    Retorna o ID gerado(SERIAL)."""
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    try:
        sql = """INSERT INTO usuario (Nome, Email, Senha, Status, idDeparamento)"
        VALUES (%s, %s, %s, 'ativo', %s)
        RETURNING ID"""
        cursor.execute(sql, (nome, email, senha, id_departamento))
        id_usuario = cursor.fetchone()[0]
        connection.commit()
        print(f"Usuario {nome} criado com ID {id_usuario}")
        return id_usuario
    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir usuário: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def listar_usuarios():
    """READ: Lista todos os usuários."""
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID, Nome, Email, Status, idDepartamento FROM usuario ORDER BY Nome")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def buscar_usuario_por_id(id_usuario):
    """READ: Busca um usuário específico."""
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ID, Nome, Email, Status, idDepartamento FROM usuario WHERE ID = %s", (id_usuario,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def atualizar_usuario(id_usuario, nome, email, senha=None):
    """UPDATE: Atualiza os dados de um usuário."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        if senha:
            sql = "UPDATE usuario SET Nome = %s, Email = %s, Senha = %s WHERE ID = %s"
            cursor.execute(sql, (nome, email, senha, id_usuario))
        else:
            sql = "UPDATE usuario SET Nome = %s, Email = %s WHERE ID = %s"
            cursor.execute(sql, (nome, email, id_usuario))
        connection.commit()
        print(f"Usuario {id_usuario} atualizado com sucesso")
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erro ao atualizar usuário: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def deletar_usuario(id_usuario):
    """Delete: Remove um usuário.
       Verifica se oo usuário é Aluno, Professor ou Admin antes de deletar."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se é Aluno
        cursor.execute("SELECT idUsuario FROM Aluno WHERE idUsuario = %s", (id_usuario,))
        is_aluno = cursor.fetchone() is not None

        # Verifica se é Professor
        cursor.execute("SELECT idUsuario FROM Professor WHERE idUsuario = %s", (id_usuario,))
        is_professor = cursor.fetchone() is not None

        # Verifica se é Admin
        cursor.execute("SELECT idUsuario FROM Admin WHERE idUsuario = %s", (id_usuario,))
        is_admin = cursor.fetchone() is not None

        # Se for aluno, verifica matriculas
        if is_aluno:
            cursor.execute("SELECT COUNT(*) FROM Aluno_Turma WHERE idAluno = %s", (id_usuario,))
            if cursor.fetchone()[0] > 0:
                print(f"Erro: Aluno ID {id_usuario} está matriculado em turmas.")
                return False
            
        # Se for professor, verifica turmas
        if is_professor:
            cursor.execute("SELECT COUNT(*) FROM Professor_Turma WHERE idProfessor = %s", (id_usuario,))
            if cursor.fetchone()[0] > 0:
                print(f"Erro: Professor ID {id_usuario} está alocado em turmas.")
                return False
            
        # tabelas filhas com ON DELETE CASCADE devem estar configuradas
        cursor.execute("DELETE FROM usuario WHERE ID = %s", (id_usuario,))
        connection.commit()
        print(f"Usuario {id_usuario} deletado com sucesso")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar usuário: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)
            
from conexao import get_connection, close_connection
from . import usuario_crud

def inserir_professor(nome, email, senha, dt_contrtacao, id_departamento=None):
    """CREATE: Insere um novo professor no banco de dados.
       ACESSA DUAS TABELAS: Usuario + Professor.
       Retorna o  ID do usuário criado ou None em caso de erro."""
    
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    try:
        # Insere os dados do usuário base
        id_usuario = usuario_crud.inserir_usuario(nome, email, senha, id_departamento)
        if not id_usuario:
            raise Exception("Falha ao criar usuário base para o professor.")
        
        # Insere os dados específicos de professor
        sql = """INSERT INTO professor (idUsuario, dt_contrtação) VALUES (%s, %s)"
                 VALUES (%s, %s, %s, %s, %s)"""
        cursor.execute(sql, (id_usuario, dt_contrtacao))
        connection.commit()
        print(f"Professor {nome} criado com ID {id_usuario}")
        return id_usuario
    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir professor: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)

def listar_professores():
    """READ: Lista todos os professores.
       ACESSA TRÊS TABELAS: Professor + Usuario + Departamento."""
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT u.ID, u.Nome, u.Email, u.Status, u.idDepartamento, p.dt_contratação, d.Nome as departamento
                          FROM professor p
                          JOIN usuario u ON p.idUsuario = u.ID
                          JOIN departamento d ON u.idDepartamento = d.ID
                          ORDER BY u.Nome""")
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar professores: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def busca_professor_por_id(id_professor):
    """READ: Busca um professor específico."""
    connection = get_connection()
    if connection is None:
        return None
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT u.ID, u.Nome, u.Email, u.Status, u.idDepartamento, p.dt_contratação, d.Nome as departamento
                          FROM professor p
                          JOIN usuario u ON p.idUsuario = u.ID
                          JOIN departamento d ON u.idDepartamento = d.ID
                          WHERE p.idUsuario = %s""", (id_professor,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar professor: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)


def buscar_professor_por_departamento(id_departamento):
    """READ: Busca todos os professores de um departamento específico."""
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        cursor.execute("""SELECT u.ID, u.Nome
                          FROM professor p
                          JOIN usuario u ON p.idUsuario = u.ID
                          WHERE u.idDepartamento = %s
                          ORDER BY u.Nome""", (id_departamento,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao buscar professores por departamento: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def atualizar_professor(id_professor, nome, email, dt_contratacao, senha=None):
    """UPDATE: Atualiza os dados de um professor.
       ACESSA DUAS TABELAS: Usuario + Professor."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Atualiza os dados do usuário base
        usuario_atualizado = usuario_crud.atualizar_usuario(id_professor, nome, email, senha)
        if not usuario_atualizado:
            raise Exception("Falha ao atualizar usuário base para o professor.")
        
        # Atualiza os dados específicos de professor
        sql = "UPDATE professor SET dt_contratação = %s WHERE idUsuario = %s"
        cursor.execute(sql, (dt_contratacao, id_professor))
        connection.commit()
        print(f"Professor {id_professor} atualizado com sucesso")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao atualizar professor: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

def deletar_professor(id_professor):
    """DELETE: Deleta um professor.
       ACESSA MULTIPLAS TABELAS: Professor_Turma, Forumlario, Professor e Usuario."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se está em turmas
        cursor.execute("SELECT COUNT(*) FROM professor_turma WHERE idProfessor = %s", (id_professor,))
        tem_turma = cursor.fetchone()[0] > 0
        if tem_turma:
            print(f"Não é possível deletar o professor {id_professor} porque ele está associado a turmas.")
            return False
        
        # Verifica se está em formulários
        cursor.execute("SELECT COUNT(*) FROM formulario WHERE idProfessor = %s", (id_professor,))
        tem_formulario = cursor.fetchone()[0] > 0
        if tem_formulario:
            print(f"Não é possível deletar o professor {id_professor} porque ele está associado a formulários.")
            return False

        # Deleta os dados específicos de professor
        cursor.execute("DELETE FROM professor WHERE idUsuario = %s", (id_professor,))
        
        # Deleta os dados do usuário base
        usuario_deletado = usuario_crud.deletar_usuario(id_professor)
        if not usuario_deletado:
            print(f"Falha ao deletar usuário base para o professor {id_professor}.")
            return False

        connection.commit()
        print(f"Professor {id_professor} deletado com sucesso")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar professor: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


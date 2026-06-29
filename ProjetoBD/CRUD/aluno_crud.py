from conexao import get_connection, close_connection
from CRUD import usuario_crud

def inserir_aluno(nome, email, senha, matricula, tipo_graduacao, semestre, id_departamento=None):
    """CREATE: Insere um aluno
       Acessa duas tabelas: Usuario + Aluno."""
    
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Insere o usuário base
        id_usuario = usuario_crud.inserir_usuario(nome, email, senha, id_departamento)
        if not id_usuario:
            raise Exception("Falha ao inserir usuário base.")
        
        # Insere o aluno
        sql = """INSERT INTO aluno (idUsuario, Matricula, TipoGraduacao, Semestre)
                 VALUES (%s, %s, %s, %s)"""
        cursor.execute(sql, (id_usuario, matricula, tipo_graduacao, semestre))
        connection.commit()
        print(f"Aluno {nome} inserido com sucesso")
        return id_usuario
    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir aluno: {e}")
        return None 
    finally:
        cursor.close()
        close_connection(connection)
def listar_alunos():
    """READ: Lista todos os alunos."""
    connection = get_connection()
    if connection is None:
        return []
    cursor = connection.cursor()
    try:
        sql = """SELECT u.ID, u.Nome, u.Email, a.Matricula, a.tipo_graduacao, a.semestre
                 FROM aluno a
                 JOIN usuario u ON a.idUsuario = u.ID
                 ORDER BY u.Nome"""
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar alunos: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)

def deletar_aluno(id_usuario):
    """DELETE: Deleta um aluno e o usuário associado.
       ACESSA MÚLTIPLAS TABELAS: Aluno_turma, Aluno, Usuario."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se esta matriculado em turmas
        cursor.execute("SELECT COUNT(*) FROM aluno_turma WHERE idAluno = %s", (id_usuario,))
        if cursor.fetchone()[0] > 0:
            print(f"Erro: Aluno está matriculado em turmas.")
            return False
        
        # Verifica se tem respostas
        cursor.execute("SELECT COUNT(*) FROM resposta WHERE idAluno = %s", (id_usuario,))
        if cursor.fetchone()[0] > 0:
            print(f"Erro: Aluno possui respostas registradas.")
            return False
        
        # Deleta da tabela aluno
        cursor.execute("DELETE FROM aluno WHERE idUsuario = %s", (id_usuario,))

        # Deleta da tabela usuario
        cursor.execute("DELETE FROM usuario WHERE ID = %s", (id_usuario,))  
        connection.commit()
        print(f"Aluno ID {id_usuario} deletado com sucesso")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar aluno: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)
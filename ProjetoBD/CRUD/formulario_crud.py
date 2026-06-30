from conexao import get_connection, close_connection
from datetime import datetime

def criar_formulario(titulo, instrucoes, data_inicio, data_fim, 
                     id_professor, id_turma, id_modelo=None, destinatario="Alunos"):
    """
    CREATE: Cria um novo formulário de avaliação.
    ACESSA TABELAS: Formulario + (verifica professor, turma, modelo)
    Retorna o ID do formulário criado ou None.
    """
    connection = get_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor()
    try:
        # Verifica se o professor existe
        cursor.execute("SELECT idUsuario FROM Professor WHERE idUsuario = %s", (id_professor,))
        if not cursor.fetchone():
            raise Exception(f"Professor ID {id_professor} não encontrado!")
        
        # Verifica se a turma existe
        cursor.execute("SELECT ID FROM Turma WHERE ID = %s", (id_turma,))
        if not cursor.fetchone():
            raise Exception(f"Turma ID {id_turma} não encontrada!")
        
        # Verifica se o modelo existe, se fornecido
        if id_modelo:
            cursor.execute("SELECT ID FROM Modelo WHERE ID = %s", (id_modelo,))
            if not cursor.fetchone():
                raise Exception(f"Modelo ID {id_modelo} não encontrado!")
        
        # Insere o formulário
        sql = """
            INSERT INTO Formulario 
            (titulo, instruções, data_inicio, data_fim, idProfessor, idTurma, 
             idModelo, destinatario, status, criado_em)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, 'ativo', CURRENT_TIMESTAMP)
            RETURNING ID
        """
        cursor.execute(sql, (titulo, instrucoes, data_inicio, data_fim, 
                            id_professor, id_turma, id_modelo, destinatario))
        id_formulario = cursor.fetchone()[0]
        connection.commit()
        print(f"Formulário '{titulo}' criado com ID {id_formulario}")
        return id_formulario
    except Exception as e:
        connection.rollback()
        print(f"Erro ao criar formulário: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)


def listar_formularios_completos():
    """
    READ: Lista todos os formulários com detalhes do professor e turma.
    ACESSA TABELAS: Formulario + Professor + Usuario + Turma + Materia
    """
    connection = get_connection()
    if connection is None:
        return []
    
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                f.ID,
                f.titulo,
                f.data_inicio,
                f.data_fim,
                f.status,
                u.Nome as nome_professor,
                t.codigo as codigo_turma,
                m.Nome as nome_materia
            FROM Formulario f
            JOIN Professor p ON f.idProfessor = p.idUsuario
            JOIN Usuario u ON p.idUsuario = u.ID
            JOIN Turma t ON f.idTurma = t.ID
            JOIN Materia m ON t.idMateria = m.ID
            ORDER BY f.data_inicio DESC
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar formulários: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def buscar_formulario_por_id(id_formulario):
    """READ: Busca um formulário específico com todos os dados."""
    connection = get_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                f.ID, f.titulo, f.instruções, f.data_inicio, f.data_fim,
                f.status, f.destinatario, f.idProfessor, f.idTurma, f.idModelo
            FROM Formulario f
            WHERE f.ID = %s
        """
        cursor.execute(sql, (id_formulario,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar formulário: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)


def atualizar_formulario(id_formulario, titulo=None, instrucoes=None, 
                         data_inicio=None, data_fim=None, status=None):
    """
    UPDATE: Atualiza dados do formulário.
    ACESSA TABELA: Formulario
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        updates = []
        params = []
        
        if titulo is not None:
            updates.append("titulo = %s")
            params.append(titulo)
        if instrucoes is not None:
            updates.append("instruções = %s")
            params.append(instrucoes)
        if data_inicio is not None:
            updates.append("data_inicio = %s")
            params.append(data_inicio)
        if data_fim is not None:
            updates.append("data_fim = %s")
            params.append(data_fim)
        if status is not None:
            updates.append("status = %s")
            params.append(status)
        
        if not updates:
            print("Nenhum dado para atualizar.")
            return False
        
        # Atualiza o campo atualizado_em
        updates.append("criado_em = CURRENT_TIMESTAMP")
        
        sql = f"UPDATE Formulario SET {', '.join(updates)} WHERE ID = %s"
        params.append(id_formulario)
        cursor.execute(sql, params)
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Formulário ID {id_formulario} atualizado!")
            return True
        else:
            print(f"Formulário ID {id_formulario} não encontrado.")
            return False
    except Exception as e:
        connection.rollback()
        print(f"Erro ao atualizar formulário: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def deletar_formulario(id_formulario):
    """
    DELETE: Remove um formulário.
    ATENÇÃO: ACESSA MÚLTIPLAS TABELAS para verificar integridade referencial: Resposta, Formulario
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # Verifica se tem respostas
        cursor.execute("SELECT COUNT(*) FROM Resposta WHERE idFormulario = %s", (id_formulario,))
        tem_respostas = cursor.fetchone()[0] > 0
        if tem_respostas:
            print(f"Erro: Formulário ID {id_formulario} já possui respostas!")
            return False
        
        # deleta o formulário
        cursor.execute("DELETE FROM Formulario WHERE ID = %s", (id_formulario,))
        connection.commit()
        print(f"Formulário ID {id_formulario} deletado com sucesso!")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar formulário: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


# Associar questões ao formulário (usando Modelo_Questao)
def associar_questao_formulario(id_formulario, id_questao):
    """
    Associa uma questão a um formulário.
    ACESSA TABELAS: Modelo, Modelo_Questao, Questao
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # Pega o idModelo do formulário
        cursor.execute("SELECT idModelo FROM Formulario WHERE ID = %s", (id_formulario,))
        resultado = cursor.fetchone()
        if not resultado or resultado[0] is None:
            print(f"Formulário ID {id_formulario} não possui modelo associado.")
            return False
        id_modelo = resultado[0]
        
        # Verifica se a questão existe
        cursor.execute("SELECT ID FROM Questao WHERE ID = %s", (id_questao,))
        if not cursor.fetchone():
            print(f"Questão ID {id_questao} não encontrada.")
            return False
        
        # Insere em Modelo_Questao
        cursor.execute(
            "INSERT INTO Modelo_Questao (idQuestao, idModelo) VALUES (%s, %s)",
            (id_questao, id_modelo)
        )
        connection.commit()
        print(f"Questão {id_questao} associada ao formulário {id_formulario}")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao associar questão: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)



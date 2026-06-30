from conexao import get_connection, close_connection

def salvar_respostas(id_aluno, id_formulario, respostas):
    """
    CREATE: Salva as respostas de um aluno a um formulário.
    ACESSA MÚLTIPLAS TABELAS PARA VALIDAÇÃO E INSERÇÃO:
        - Aluno (verifica existência)
        - Formulario (verifica existência e status)
        - Aluno_Turma (verifica matrícula)
        - Resposta (insere)
        - Questao (valida se cada questão pertence ao formulário via Modelo_Questao)
    PARÂMETROS:
        - id_aluno: ID do aluno (que é o idUsuario)
        - id_formulario: ID do formulário
        - respostas: lista de dicionários ou tuplas com (id_questao, conteudo)
          Exemplo: [{"id_questao": 1, "conteudo": "Ótimo!"}, ...]
    Retorna True se tudo foi inserido, False caso contrário.
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # VALIDAÇÃO 1: Aluno existe
        cursor.execute("SELECT idUsuario FROM Aluno WHERE idUsuario = %s", (id_aluno,))
        if not cursor.fetchone():
            raise Exception(f"Aluno ID {id_aluno} não encontrado!")
        
        # VALIDAÇÃO 2: Formulário existe e está ativo
        cursor.execute("SELECT ID, idTurma, status FROM Formulario WHERE ID = %s", (id_formulario,))
        resultado = cursor.fetchone()
        if not resultado:
            raise Exception(f"Formulário ID {id_formulario} não encontrado!")
        
        id_turma = resultado[1]
        status_form = resultado[2]
        if status_form != 'ativo':
            raise Exception(f"Formulário ID {id_formulario} não está ativo (status: {status_form})")
        
        # VALIDAÇÃO 3: Aluno está matriculado na turma do formulário?
        cursor.execute(
            "SELECT idAluno FROM Aluno_Turma WHERE idAluno = %s AND idTurma = %s",
            (id_aluno, id_turma)
        )
        if not cursor.fetchone():
            raise Exception(f"Aluno ID {id_aluno} não está matriculado na turma ID {id_turma}!")
        
        # VALIDAÇÃO 4: O aluno já respondeu este formulário?
        cursor.execute(
            "SELECT COUNT(*) FROM Resposta WHERE idAluno = %s AND idFormulario = %s",
            (id_aluno, id_formulario)
        )
        if cursor.fetchone()[0] > 0:
            raise Exception(f"Aluno ID {id_aluno} já respondeu o formulário ID {id_formulario}!")
        
        # VALIDAÇÃO 5: Cada questão pertence ao formulário?
        # Busca todas as questões associadas ao formulário via Modelo_Questao
        cursor.execute("""
            SELECT q.ID 
            FROM Questao q
            JOIN Modelo_Questao mq ON q.ID = mq.idQuestao
            JOIN Formulario f ON mq.idModelo = f.idModelo
            WHERE f.ID = %s
        """, (id_formulario,))
        questoes_validas = [row[0] for row in cursor.fetchall()]
        
        if not questoes_validas:
            raise Exception(f"Formulário ID {id_formulario} não possui questões cadastradas!")
        
        for resposta in respostas:
            id_questao = resposta['id_questao']
            conteudo = resposta['conteudo']
            
            if id_questao not in questoes_validas:
                raise Exception(f"Questão ID {id_questao} não pertence a este formulário!")
            
            # Insere a resposta
            sql = """
                INSERT INTO Resposta (idAluno, idFormulario, idQuestao, conteudo, respondido_em)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP)
            """
            cursor.execute(sql, (id_aluno, id_formulario, id_questao, conteudo))
        
        connection.commit()
        print(f"Respostas do aluno ID {id_aluno} salvas com sucesso!")
        return True
        
    except Exception as e:
        connection.rollback()
        print(f"Erro ao salvar respostas: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def listar_respostas_por_formulario(id_formulario):
    """
    READ: Lista todas as respostas de um formulário, agrupadas por aluno.
    ACESSA TABELAS: Resposta + Aluno + Usuario + Questao
    """
    connection = get_connection()
    if connection is None:
        return []
    
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                u.Nome as aluno_nome,
                q.enunciado as questao_texto,
                r.conteudo as resposta,
                r.respondido_em
            FROM Resposta r
            JOIN Aluno a ON r.idAluno = a.idUsuario
            JOIN Usuario u ON a.idUsuario = u.ID
            JOIN Questao q ON r.idQuestao = q.ID
            WHERE r.idFormulario = %s
            ORDER BY u.Nome, q.ID
        """
        cursor.execute(sql, (id_formulario,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar respostas: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def contar_respostas_por_formulario(id_formulario):
    """READ: Conta quantas respostas foram dadas a um formulário (número de alunos que responderam)."""
    connection = get_connection()
    if connection is None:
        return 0

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT COUNT(DISTINCT idAluno) FROM Resposta WHERE idFormulario = %s",
            (id_formulario,)
        )
        return cursor.fetchone()[0]
    except Exception as e:
        print(f"Erro ao contar respostas: {e}")
        return 0
    finally:
        cursor.close()
        close_connection(connection)


def atualizar_resposta(id_resposta, novo_conteudo):
    """
    UPDATE: Atualiza o conteúdo de uma resposta específica.
    ACESSA TABELA: Resposta
    (Útil para correções ou edições posteriores)
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        cursor.execute(
            "UPDATE Resposta SET conteudo = %s, respondido_em = CURRENT_TIMESTAMP WHERE ID = %s",
            (novo_conteudo, id_resposta)
        )
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erro ao atualizar resposta: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def deletar_resposta(id_resposta, id_aluno=None):
    """
    DELETE: Remove uma resposta específica.
    ACESSA TABELA: Resposta
    Pode ser usado apenas pelo professor ou admin.
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # Verifica se a resposta pertence ao aluno
        if id_aluno:
            cursor.execute(
                "SELECT idAluno FROM Resposta WHERE ID = %s",
                (id_resposta,)
            )
            row = cursor.fetchone()
            if row and row[0] != id_aluno:
                print("Erro: Esta resposta não pertence ao aluno informado.")
                return False
        
        cursor.execute("DELETE FROM Resposta WHERE ID = %s", (id_resposta,))
        connection.commit()
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar resposta: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

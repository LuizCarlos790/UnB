from conexao import get_connection, close_connection

def criar_turma(codigo, turno, horario, id_materia, lista_id_professores=None):
    """
    CREATE: Cria uma nova turma e associa os professores responsáveis.
    ACESSA TABELAS: Turma + Professor_Turma (e também Materia para verificação)
    PARÂMETROS:
        - codigo: código da turma (ex: "T01")
        - turno: "Manhã", "Tarde", "Noite"
        - horario: texto com horários (ex: "Segunda 10:00-12:00")
        - id_materia: ID da matéria
        - lista_id_professores: lista de IDs de professores que serão alocados
    Retorna o ID da turma criada ou None em caso de erro.
    """
    connection = get_connection()
    if connection is None:
        return None
    
    cursor = connection.cursor()
    try:
        # Verifica se a matéria existe
        cursor.execute("SELECT ID FROM Materia WHERE ID = %s", (id_materia,))
        if not cursor.fetchone():
            raise Exception(f"Matéria ID {id_materia} não encontrada!")
        
        # Insere a turma
        sql_turma = """
            INSERT INTO Turma (idMateria, Turno, Horario, codigo)
            VALUES (%s, %s, %s, %s)
            RETURNING ID
        """
        cursor.execute(sql_turma, (id_materia, turno, horario, codigo))
        id_turma = cursor.fetchone()[0]
        
        # Se houver lista de professores, insere as associações
        if lista_id_professores:
            for id_professor in lista_id_professores:
                # Verifica se o professor existe
                cursor.execute("SELECT idUsuario FROM Professor WHERE idUsuario = %s", (id_professor,))
                if not cursor.fetchone():
                    print(f"Aviso: Professor ID {id_professor} não existe. Ignorando.")
                    continue
                # Insere em Professor_Turma
                cursor.execute(
                    "INSERT INTO Professor_Turma (idProfessor, idTurma) VALUES (%s, %s)",
                    (id_professor, id_turma)
                )
        
        connection.commit()
        print(f"Turma {codigo} criada com ID {id_turma}")
        return id_turma
    except Exception as e:
        connection.rollback()
        print(f"Erro ao criar turma: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)


def listar_turmas_completas():
    """
    READ: Lista todas as turmas com detalhes da matéria e professores.
    ACESSA TABELAS: Turma + Materia + Professor_Turma + Professor + Usuario
    """
    connection = get_connection()
    if connection is None:
        return []
    
    cursor = connection.cursor()
    try:
        sql = """
            SELECT 
                t.ID,
                t.codigo,
                t.Turno,
                t.Horario,
                m.Nome as nome_materia,
                m.Codigo as codigo_materia,
                (SELECT string_agg(u.Nome, ', ')
                 FROM Professor_Turma pt
                 JOIN Professor p ON pt.idProfessor = p.idUsuario
                 JOIN Usuario u ON p.idUsuario = u.ID
                 WHERE pt.idTurma = t.ID) as professores
            FROM Turma t
            JOIN Materia m ON t.idMateria = m.ID
            ORDER BY t.codigo
        """
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        print(f"Erro ao listar turmas: {e}")
        return []
    finally:
        cursor.close()
        close_connection(connection)


def buscar_turma_por_id(id_turma):
    """READ: Busca uma turma específica com seus detalhes."""
    connection = get_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    try:
        sql = """
            SELECT t.ID, t.codigo, t.Turno, t.Horario, t.idMateria,
                   m.Nome as materia_nome
            FROM Turma t
            JOIN Materia m ON t.idMateria = m.ID
            WHERE t.ID = %s
        """
        cursor.execute(sql, (id_turma,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar turma: {e}")
        return None
    finally:
        cursor.close()
        close_connection(connection)


def atualizar_turma(id_turma, codigo=None, turno=None, horario=None, id_materia=None):
    """
    UPDATE: Atualiza os dados básicos da turma.
    ACESSA TABELA: Turma
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # Construir a query dinamicamente (apenas os campos fornecidos)
        updates = []
        params = []
        
        if codigo is not None:
            updates.append("codigo = %s")
            params.append(codigo)
        if turno is not None:
            updates.append("Turno = %s")
            params.append(turno)
        if horario is not None:
            updates.append("Horario = %s")
            params.append(horario)
        if id_materia is not None:
            updates.append("idMateria = %s")
            params.append(id_materia)
        
        if not updates:
            print("Nenhum dado para atualizar.")
            return False
        
        sql = f"UPDATE Turma SET {', '.join(updates)} WHERE ID = %s"
        params.append(id_turma)
        cursor.execute(sql, params)
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Turma ID {id_turma} atualizada com sucesso!")
            return True
        else:
            print(f"Turma ID {id_turma} não encontrada.")
            return False
    except Exception as e:
        connection.rollback()
        print(f"Erro ao atualizar turma: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def deletar_turma(id_turma):
    """
    DELETE: Remove uma turma.
    ATENÇÃO: ACESSA MÚLTIPLAS TABELAS para verificar integridade referencial:
        - Aluno_Turma (verifica se há alunos matriculados)
        - Formulario (verifica se há formulários associados)
        - Professor_Turma (deleta associações de professores)
        - Turma (deleta a turma em si)
    """
    connection = get_connection()
    if connection is None:
        return False
    
    cursor = connection.cursor()
    try:
        # Verifica se tem alunos matriculados
        cursor.execute("SELECT COUNT(*) FROM Aluno_Turma WHERE idTurma = %s", (id_turma,))
        tem_alunos = cursor.fetchone()[0] > 0
        if tem_alunos:
            print(f"Erro: Turma ID {id_turma} possui alunos matriculados!")
            return False
        
        # Verifica se tem formulários associados
        cursor.execute("SELECT COUNT(*) FROM Formulario WHERE idTurma = %s", (id_turma,))
        tem_formularios = cursor.fetchone()[0] > 0
        if tem_formularios:
            print(f"Erro: Turma ID {id_turma} possui formulários associados!")
            return False
        
        # Deleta as associações de professores (se houver)
        cursor.execute("DELETE FROM Professor_Turma WHERE idTurma = %s", (id_turma,))
        
        # Deleta a turma
        cursor.execute("DELETE FROM Turma WHERE ID = %s", (id_turma,))
        connection.commit()
        print(f"Turma ID {id_turma} deletada com sucesso!")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao deletar turma: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)



def associar_professor_turma(id_professor, id_turma):
    """Associa um professor a uma turma."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se a associação já existe
        cursor.execute(
            "SELECT 1 FROM Professor_Turma WHERE idProfessor = %s AND idTurma = %s",
            (id_professor, id_turma)
        )
        if cursor.fetchone():
            print(f"Professor {id_professor} já está associado à turma {id_turma}")
            return True
        
        cursor.execute(
            "INSERT INTO Professor_Turma (idProfessor, idTurma) VALUES (%s, %s)",
            (id_professor, id_turma)
        )
        connection.commit()
        print(f"Professor {id_professor} associado à turma {id_turma}")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao associar professor: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def remover_professor_turma(id_professor, id_turma):
    """Remove a associação de um professor com uma turma."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        cursor.execute(
            "DELETE FROM Professor_Turma WHERE idProfessor = %s AND idTurma = %s",
            (id_professor, id_turma)
        )
        connection.commit()
        print(f"Professor {id_professor} removido da turma {id_turma}")
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erro ao remover professor: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def matricular_aluno(id_aluno, id_turma):
    """Matricula um aluno em uma turma."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se o aluno já está matriculado
        cursor.execute(
            "SELECT 1 FROM Aluno_Turma WHERE idAluno = %s AND idTurma = %s",
            (id_aluno, id_turma)
        )
        if cursor.fetchone():
            print(f"Aluno {id_aluno} já está matriculado na turma {id_turma}")
            return True
        
        cursor.execute(
            "INSERT INTO Aluno_Turma (idAluno, idTurma) VALUES (%s, %s)",
            (id_aluno, id_turma)
        )
        connection.commit()
        print(f"Aluno {id_aluno} matriculado na turma {id_turma}")
        return True
    except Exception as e:
        connection.rollback()
        print(f"Erro ao matricular aluno: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)


def desmatricular_aluno(id_aluno, id_turma):
    """Desmatricula um aluno de uma turma."""
    connection = get_connection()
    if connection is None:
        return False
    cursor = connection.cursor()
    try:
        # Verifica se o aluno tem respostas para essa turma (se sim, não pode desmatricular)
        cursor.execute("""
            SELECT COUNT(*) 
            FROM Resposta r
            JOIN Formulario f ON r.idFormulario = f.ID
            WHERE r.idAluno = %s AND f.idTurma = %s
        """, (id_aluno, id_turma))
        if cursor.fetchone()[0] > 0:
            print(f"Erro: Aluno {id_aluno} já respondeu formulários nesta turma, não pode desmatricular.")
            return False
        
        cursor.execute(
            "DELETE FROM Aluno_Turma WHERE idAluno = %s AND idTurma = %s",
            (id_aluno, id_turma)
        )
        connection.commit()
        print(f"Aluno {id_aluno} desmatriculado da turma {id_turma}")
        return cursor.rowcount > 0
    except Exception as e:
        connection.rollback()
        print(f"Erro ao desmatricular aluno: {e}")
        return False
    finally:
        cursor.close()
        close_connection(connection)

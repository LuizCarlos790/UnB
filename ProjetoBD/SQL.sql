-- Drop para limpar e rodar do zero.
DROP TABLE IF EXISTS 
    Resposta,
    Modelo_Questao,
    Aluno_Turma,
    Professor_Turma,
    Admin_Turma,
    Formulario,
    Turma,
    Modelo,
    Questao,
    Aluno,
    Professor,
    Admin,
    Materia,
    Usuario,
    Departamento 
CASCADE;

CREATE TABLE "Materia" 
( 
 "id" SERIAL PRIMARY KEY,  
ALTER TABLE "Professor_Turma" ADD FOREIGN KEY("id_professor") REFERENCES "Professor" ("id_usuario");
ALTER TABLE "Professor_Turma" ADD FOREIGN KEY("id_turma") REFERENCES "Turma" ("id");
ALTER TABLE "Admin_Turma" ADD FOREIGN KEY("id_turma") REFERENCES "Turma" ("id");
ALTER TABLE "Admin_Turma" ADD FOREIGN KEY("id_admin") REFERENCES "Admin" ("id_usuario");

/*Registros*/

INSERT INTO Departamento (Codigo, Nome) VALUES
(1, 'Ciência da Computação'),
(2, 'Engenharia Civil'),
(3, 'Administração'),
(4, 'Design Gráfico'),
(5, 'Matemática Aplicada');

INSERT INTO Usuario (ID, Nome, Email, Senha, Status, idDepartamento) VALUES
(1, 'João Silva', 'joao.silva@email.com', 'senha123', 'Ativo', 1),
(2, 'Maria Santos', 'maria.santos@email.com', 'senha456', 'Ativo', 2),
(3, 'Carlos Lima', 'carlos.lima@email.com', 'senha789', 'Ativo', 3),
(4, 'Ana Pereira', 'ana.pereira@email.com', 'senhaabc', 'Inativo', 4),
(5, 'Pedro Costa', 'pedro.costa@email.com', 'senhaxyz', 'Ativo', 5),
(6, 'Prof. Carlos Silva', 'carlos.silva@instituicao.edu', 'hash_prof_123', 'Ativo', 1),
(7, 'Prof. Mariana Oliveira', 'mariana.oliveira@instituicao.edu', 'hash_prof_456', 'Ativo', 2),
(8, 'Prof. João Pereira', 'joao.pereira@instituicao.edu', 'hash_prof_789', 'Ativo', 1),
(9, 'Prof. Ana Costa', 'ana.costa@instituicao.edu', 'hash_prof_000', 'Ativo', 2);

INSERT INTO Admin (idUsuario, nv_acesso) VALUES
(6, 'Super'),
(7, 'Moderador'),
(8, 'Super'),
(9, 'Moderador');

INSERT INTO Professor (idUsuario, dt_contratação) VALUES
(6, '2020-01-15'),
(7, '2019-03-20'),
(8, '2021-06-10'),
(9, '2018-11-05');

INSERT INTO Aluno (idUsuario, Matricula, tipo_graduacao, semestre) VALUES
(1, '20210001', 'Bacharelado', '8'),
(2, '20210002', 'Licenciatura', '6'),
(3, '20210003', 'Bacharelado', '4'),
(4, '20210004', 'Tecnólogo', '2'),
(5, '20210005', 'Bacharelado', '10');

INSERT INTO Materia (ID, Nome, Codigo, semestre, idDepartamento) VALUES
(1, 'Algoritmos', 'ALG-101', '1', 1),
(2, 'Estruturas de Dados', 'EST-201', '2', 1),
(3, 'Cálculo I', 'CAL-101', '1', 5),
(4, 'Física I', 'FIS-101', '2', 2),
(5, 'Marketing Digital', 'MKT-201', '3', 3);

INSERT INTO Turma (ID, idMateria, Turno, Horario, codigo) VALUES
(1, 1, 'Manhã', '08:00-10:00', 101),
(2, 2, 'Tarde', '14:00-16:00', 102),
(3, 3, 'Manhã', '10:00-12:00', 103),
(4, 4, 'Noite', '19:00-21:00', 104),
(5, 5, 'Tarde', '16:00-18:00', 105);

INSERT INTO Questao (ID, enunciado, versao, atualizado_em, status, criado_em) VALUES
(1, 'A didática e a clareza do professor na exposição dos conteúdos são adequadas?', '1.0', '2026-01-15 10:30:00', 'Publicada', '2026-01-10 08:00:00'),
(2, 'Os materiais didáticos (slides, listas, livros) disponibilizados são suficientes para o aprendizado?', '2.1', '2026-01-16 14:20:00', 'Rascunho', '2026-01-12 09:30:00'),
(3, 'A coordenação do curso oferece suporte adequado para as dúvidas e necessidades dos alunos?', '1.2', '2026-01-14 11:15:00', 'Publicada', '2026-01-11 10:00:00'),
(4, 'A infraestrutura da sala de aula (climatização, iluminação, equipamentos) é satisfatória?', '1.0', '2026-01-13 16:45:00', 'Publicada', '2026-01-13 10:00:00'),
(5, 'A carga horária da disciplina é compatível com a profundidade do conteúdo ensinado?', '1.1', '2026-01-17 09:00:00', 'Rascunho', '2026-01-15 13:30:00');

INSERT INTO Modelo (ID, idAdmin, Nome, descricao, criado_em, atualizado_em, versao, status) VALUES
(1, 6, 'Avaliação de Desempenho Docente', 'Questionário focado na didática, interação e metodologia do professor.', '2026-01-10 08:00:00', '2026-01-10 08:00:00', '1.0', 'Ativo'),
(2, 7, 'Avaliação de Conteúdo e Material', 'Questionário focado no cumprimento do plano de ensino, material e critérios de avaliação.', '2026-01-12 10:00:00', '2026-01-15 14:00:00', '1.1', 'Ativo'),
(3, 8, 'Avaliação de Infraestrutura e Suporte','Questionário focado nas condições físicas, AVA e suporte da coordenação.', '2026-01-14 09:30:00', '2026-01-16 16:20:00', '2.0', 'Ativo'),
(4, 9, 'Questionário Rápido', 'Questionários de 5 perguntas', '2026-01-15 11:00:00', '2026-01-15 11:00:00', '1.0', 'Rascunho'),
(5, 6, 'Prova de Recuperação', 'Modelo para provas de recuperação', '2026-01-16 13:00:00', '2026-01-17 15:30:00', '1.0', 'Inativo');

INSERT INTO Formulario (ID, idModelo, status, data_inicio, data_fim, criado_em, titulo, instrucoes, destinatario, idProfessor, idTurma) VALUES
(1, 1, 'Aberto', '2026-01-20', '2026-01-27', '2026-01-19 10:00:00', 'Avaliação Docente - Cálculo I', 'Avalie a didática do Professor.', 'Alunos do 1º ano', 6, 1),
(2, 2, 'Fechado', '2026-01-15', '2026-01-22', '2026-01-14 09:00:00', 'Avaliação de Conteúdo - Física Geral', 'Avalie o material e cumprimento do plano de ensino.', 'Alunos do 2º ano', 9, 2),
(3, 3, 'Rascunho', '2026-01-25', '2026-02-01', '2026-01-24 14:30:00', 'Avaliação de Infraestrutura - Geral', 'Avalie as condições da sala e do AVA.', 'Alunos do 1º ano', 8, 3),
(4, 1, 'Aberto', '2026-01-18', '2026-01-25', '2026-01-17 11:15:00', 'Avaliação Docente - Marketing', 'Avalie a didática da Professora.', 'Alunos do 2º ano', 7, 4),
(5, 2, 'Agendado', '2026-07-06', '2026-07-10', '2026-01-20 16:00:00', 'Avaliação de Conteúdo - Bioestatística', 'Avalie a adequação do conteúdo e da carga horária.', 'Alunos do 3º ano', 6, 5);

INSERT INTO Resposta (ID, idAluno, idFormulario, conteudo, respondido_em, idQuestao) VALUES
(1, 1, 1, 'Sim, o professor explica de forma extremamente clara e utiliza exemplos práticos.', '2026-01-20 08:15:00', 1),
(2, 2, 1, 'A didática é boa, mas às vezes a velocidade da matéria é alta.', '2026-01-16 09:30:00', 2),
(3, 3, 2, 'Sim, todos os tópicos do plano de ensino foram dados.', '2026-01-25 10:20:00', 3),
(4, 4, 4, 'A didática da professora é dinâmica e envolvente.', '2026-01-18 14:45:00', 4),
(5, 5, 4, 'A coordenação demorou um pouco para resolver um problema de matrícula.', '2026-02-01 08:00:00', 5);

INSERT INTO Aluno_Turma (idTurma, idAluno) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

INSERT INTO Professor_Turma (idProfessor, idTurma) VALUES
(6, 1),
(7, 2),
(8, 3),
(9, 4),
(6, 5);

INSERT INTO Admin_Turma (idTurma, idAdmin) VALUES
(1, 6),
(2, 7),
(3, 8),
(4, 9),
(5, 6);

INSERT INTO Modelo_Questao (idQuestao, idModelo) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5);

/* Triggers
f = função
t = trigger
*/

CREATE OR REPLACE FUNCTION f_impedir_delete_formulario()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM Resposta WHERE idFormulario = OLD.ID) THEN
        RAISE EXCEPTION 'Não é possível deletar este formulário, pois ele já possui respostas.';
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER t_impedir_delete_formulario
BEFORE DELETE ON Formulario
FOR EACH ROW
EXECUTE FUNCTION f_impedir_delete_formulario();

CREATE OR REPLACE FUNCTION f_impedir_delete_professor()
RETURNS TRIGGER AS $$
BEGIN
   
    IF EXISTS (SELECT 1 FROM Professor_Turma WHERE idProfessor = OLD.idUsuario) THEN
        RAISE EXCEPTION 'Erro: Professor % está vinculado a turmas e não pode ser deletado.', OLD.idUsuario;
    END IF;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER t_impedir_delete_professor
BEFORE DELETE ON Professor
FOR EACH ROW
EXECUTE FUNCTION f_impedir_delete_professor();

CREATE OR REPLACE FUNCTION f_soft_delete_usuario()
RETURNS TRIGGER AS $$
BEGIN

    UPDATE Usuario 
    SET status = 'Inativo', 
        Senha = NULL, 
        Email = CONCAT('deleted_', OLD.ID, '_', OLD.Email)
    WHERE ID = OLD.ID;
    

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER t_soft_delete_usuario
BEFORE DELETE ON Usuario
FOR EACH ROW
EXECUTE FUNCTION f_soft_delete_usuario();

/* Procedures 
p = procedure
*/

CREATE OR REPLACE PROCEDURE p_abrir_formularios_agendados (
    INOUT mensagem TEXT DEFAULT ''
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_linhas_afetadas INT;
BEGIN
    START TRANSACTION;

    -- Atualiza formulários 'Agendados' com data_início <= hoje
    UPDATE Formulario 
    SET status = 'Aberto', atualizado_em = NOW()
    WHERE status = 'Agendado' AND data_inicio <= CURRENT_DATE;

    GET DIAGNOSTICS v_linhas_afetadas = ROW_COUNT;

    COMMIT;

    mensagem := CONCAT(v_linhas_afetadas, ' formulário(s) agendado(s) foram abertos/publicados.');
END;
$$;
-- Temos exatamento um formulário agendado nos registros para usar como exemplo
/*Codigo para usar:
CALL p_abrir_formularios_agendados(NULL);
*/

CREATE OR REPLACE PROCEDURE p_matricular_aluno (
    p_idAluno INT,
    p_idTurma INT,
    INOUT mensagem TEXT DEFAULT ''
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Valida se o aluno existe
    IF NOT EXISTS (SELECT 1 FROM Aluno WHERE idUsuario = p_idAluno) THEN
        mensagem := 'Erro: Aluno não encontrado.';
        RAISE EXCEPTION '%', mensagem;
    END IF;

    -- Valida se a turma existe
    IF NOT EXISTS (SELECT 1 FROM Turma WHERE ID = p_idTurma) THEN
        mensagem := 'Erro: Turma não encontrada.';
        RAISE EXCEPTION '%', mensagem;
    END IF;

    -- Valida se o aluno já está matriculado nesta turma
    IF EXISTS (SELECT 1 FROM Aluno_Turma WHERE idAluno = p_idAluno AND idTurma = p_idTurma) THEN
        mensagem := 'Aviso: Aluno já está matriculado nesta turma.';
        RETURN; 
    END IF;

    -- Insere a matrícula
    INSERT INTO Aluno_Turma (idTurma, idAluno) VALUES (p_idTurma, p_idAluno);
    
    mensagem := CONCAT('Sucesso! Aluno ', p_idAluno, ' matriculado na turma ', p_idTurma, '.');
    COMMIT;
END;
$$;
/* Codigo para usar:
CALL p_matricular_aluno(1, 2, NULL);
*/

CREATE OR REPLACE PROCEDURE p_finalizar_formularios_vencidos (
    INOUT mensagem TEXT DEFAULT ''
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_linhas_afetadas INT;
BEGIN
    START TRANSACTION;

    UPDATE Formulario 
    SET status = 'Finalizado', atualizado_em = NOW()
    WHERE status = 'Publicado' AND data_fim < CURRENT_DATE;

    GET DIAGNOSTICS v_linhas_afetadas = ROW_COUNT;

    COMMIT;

    mensagem := CONCAT(v_linhas_afetadas, ' formulário(s) finalizado(s) com sucesso.');
END;
$$;
-- Temos 2 formularios com data vencida para usar
/*Codigo para usar:
CALL p_finalizar_formularios_vencidos(NULL);
*/

/* Views
vw = view
*/

CREATE OR REPLACE VIEW vw_alunos_turmas AS
SELECT 
    u.ID AS id_usuario,
    u.Nome AS nome_aluno,
    a.Matricula,
    a.semestre AS semestre_aluno,
    t.ID AS id_turma,
    t.codigo AS codigo_turma,
    t.Turno,
    t.Horario,
    m.Nome AS nome_materia,
    m.Codigo AS codigo_materia,
    d.Nome AS nome_departamento
FROM Aluno a
INNER JOIN Usuario u ON a.idUsuario = u.ID
INNER JOIN Aluno_Turma at ON at.idAluno = a.idUsuario
INNER JOIN Turma t ON at.idTurma = t.ID
INNER JOIN Materia m ON t.idMateria = m.ID
INNER JOIN Departamento d ON m.idDepartamento = d.Codigo
ORDER BY u.Nome;

/*Codigo para usar:
SELECT * FROM vw_alunos_turmas WHERE nome_aluno LIKE 'Carlos%';
*/

CREATE OR REPLACE VIEW vw_formularios_detalhados AS
SELECT 
    f.ID AS id_formulario,
    f.titulo,
    f.status,
    f.data_inicio,
    f.data_fim,
    m.Nome AS nome_modelo,
    m.descricao AS descricao_modelo,
    u_prof.Nome AS nome_professor,
    t.codigo AS codigo_turma,
    mat.Nome AS nome_materia,
    COUNT(r.ID) AS total_respostas_recebidas
FROM Formulario f
INNER JOIN Modelo m ON f.idModelo = m.ID
INNER JOIN Professor p ON f.idProfessor = p.idUsuario
INNER JOIN Usuario u_prof ON p.idUsuario = u_prof.ID
INNER JOIN Turma t ON f.idTurma = t.ID
INNER JOIN Materia mat ON t.idMateria = mat.ID
LEFT JOIN Resposta r ON r.idFormulario = f.ID
GROUP BY f.ID, m.Nome, m.descricao, u_prof.Nome, t.codigo, mat.Nome
ORDER BY f.data_inicio DESC;

/*Codigo para usar:
SELECT * FROM vw_formularios_detalhados WHERE status = 'Aberto';
*/

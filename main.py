import streamlit as st
import json
import os
from datetime import date

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
# =====================================================================
st.set_page_config(page_title="🧸 Portal de Gestão da Educação Infantil", layout="wide", page_icon="🧸")

# ARQUIVOS DE BANCO DE DADOS LOCAL (JSON)
DB_FILE = "professores_db.json"
ALUNOS_FILE = "alunos_db.json"
ATAS_FILE = "atas_db.json"
PLAN_FILE = "planejamentos_db.json"
OCORRENCIAS_FILE = "ocorrencias_db.json"

# CONFIGURAÇÕES ESCOLARES SOLICITADAS
TURMAS_ESCOLARES = [
    "Berçário I", "Berçário II", "Maternal I", 
    "Maternal II - 1", "Maternal II - 2", 
    "1ª etapa - 1", "1ª etapa - 2", 
    "2ª etapa - 1", "2ª etapa - 2", "Geral"
]

MATERIAS_PLANEJAMENTO = [
    "Linguagem Verbal", "Linguagem Matemática", 
    "Indivíduo e Sociedade", "Cultura, Corpo e Movimento", 
    "Artes", "AEE"
]

# =====================================================================
# 2. SISTEMA DE CARGA E PERSISTÊNCIA DE DADOS
# =====================================================================
def carregar_dados():
    if not os.path.exists(DB_FILE):
        default_profs = {
            "789": {"nome": "Coordenação/Direção", "cargo": "Administrador", "turma": "Geral", "email": "direcao@escola.com"},
            "123": {"nome": "Regina Mello", "cargo": "Professor Regular", "turma": "Maternal I", "email": "regina@escola.com"},
            "456": {"nome": "Paula Souza", "cargo": "Professor AEE", "turma": "Geral", "email": "paula.aee@escola.com"},
            "000": {"nome": "Inspeção de Pátio", "cargo": "Monitor", "turma": "Plantão", "email": ""}
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_profs, f, ensure_ascii=False, indent=4)
            
    if not os.path.exists(ALUNOS_FILE):
        default_alunos = [
            {
                "id": "1", "nome": "Arthur Silva", "turma": "Maternal I", 
                "alergias": "Frutos do mar", "restricoes": "Intolerante a Lactose", 
                "retirada": "Pais (Marcos e Ana)", "contato": "(11) 98888-7777", 
                "relatorios_aee": "Apresenta boa evolução nas sessões de estimulação cognitiva.",
                "encaminhamentos": "Encaminhado para fonoaudiologia em Março/2026.",
                "terapias": "Terapia Ocupacional e Fonoaudiologia",
                "dias_horarios_terapias": "Terças e Quintas às 14:00",
                "foto": "👶", "faltas_consecutivas": 0
            }
        ]
        with open(ALUNOS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_alunos, f, ensure_ascii=False, indent=4)

    for f_path in [ATAS_FILE, PLAN_FILE, OCORRENCIAS_FILE]:
        if not os.path.exists(f_path):
            with open(f_path, "w", encoding="utf-8") as f: 
                json.dump([], f)

    with open(DB_FILE, "r", encoding="utf-8") as f: st.session_state.professores_db = json.load(f)
    with open(ALUNOS_FILE, "r", encoding="utf-8") as f: st.session_state.alunos_db = json.load(f)
    with open(ATAS_FILE, "r", encoding="utf-8") as f: st.session_state.atas_salvas = json.load(f)
    with open(PLAN_FILE, "r", encoding="utf-8") as f: st.session_state.planejamentos_salvos = json.load(f)
    with open(OCORRENCIAS_FILE, "r", encoding="utf-8") as f: st.session_state.ocorrencias_salvas = json.load(f)

def salvar_dados(chave, payload=None):
    if chave == "alunos":
        with open(ALUNOS_FILE, "w", encoding="utf-8") as f: json.dump(st.session_state.alunos_db, f, ensure_ascii=False, indent=4)
    elif chave == "db":
        with open(DB_FILE, "w", encoding="utf-8") as f: json.dump(st.session_state.professores_db, f, ensure_ascii=False, indent=4)
    elif chave == "ocorrencias":
        if payload: st.session_state.ocorrencias_salvas.append(payload)
        with open(OCORRENCIAS_FILE, "w", encoding="utf-8") as f: json.dump(st.session_state.ocorrencias_salvas, f, ensure_ascii=False, indent=4)
    elif chave == "plan":
        if payload: st.session_state.planejamentos_salvos.append(payload)
        with open(PLAN_FILE, "w", encoding="utf-8") as f: json.dump(st.session_state.planejamentos_salvos, f, ensure_ascii=False, indent=4)
    elif chave == "atas":
        if payload: st.session_state.atas_salvas.append(payload)
        with open(ATAS_FILE, "w", encoding="utf-8") as f: json.dump(st.session_state.atas_salvas, f, ensure_ascii=False, indent=4)

carregar_dados()

# =====================================================================
# 3. CONTROLE DE AUTENTICAÇÃO E BARRA LATERAL
# =====================================================================
st.sidebar.title("🔐 Acesso ao Portal")
matricula = st.sidebar.text_input("Digite sua Matrícula:", type="password")

usuario = None
if matricula in st.session_state.professores_db:
    usuario = st.session_state.professores_db[matricula]
    st.sidebar.success(f"Conectado: {usuario['nome']}")
    st.sidebar.info(f"Função: {usuario['cargo']}")
elif matricula:
    st.sidebar.error("Matrícula não cadastrada.")

# =====================================================================
# 4. EXECUÇÃO DE TELAS PEDAGÓGICAS
# =====================================================================
if usuario:
    st.title("🧸 Portal de Gestão da Educação Infantil")
    st.divider()

    # PERFIL: MONITORES
    if usuario['cargo'] == "Monitor":
        st.header("🚨 Carômetro de Segurança & Fichas Médicas")
        busca = st.text_input("🔍 Buscar Criança pelo Nome:")
        for aluno in st.session_state.alunos_db:
            if busca.lower() in aluno['nome'].lower():
                with st.expander(f"{aluno['foto']} {aluno['nome']} - {aluno['turma']}", expanded=True):
                    c1, c2 = st.columns(2)
                    c1.markdown(f"🔴 **Alergias:** {aluno['alergias']}\n\n🥛 **Restrições:** {aluno['restricoes']}")
                    c2.markdown(f"🪪 **Autorizados para Retirada:** {aluno['retirada']}\n\n📞 **Contato:** {aluno['contato']}")

    # PERFIL: PROFESSOR REGULAR
    elif usuario['cargo'] == "Professor Regular":
        st.subheader(f"Sala Virtual: {usuario['turma']}")
        menu_prof = st.selectbox("Selecione o Módulo de Trabalho:", ["📝 Diário & Chamada", "📅 Planejamento Quinzenal", "👶 Ocorrências da Rotina", "📋 Atas & Conselhos"])
        st.write("---")
        
        alunos_turma = [a for a in st.session_state.alunos_db if a['turma'] == usuario['turma']]

        if menu_prof == "📝 Diário & Chamada":
            st.header("📋 Chamada Diária e Controle de Frequência")
            with st.form("form_chamada"):
                lista_presenca = {}
                for aluno in alunos_turma:
                    lista_presenca[aluno['id']] = st.checkbox(f"👤 {aluno['nome']}", value=True)
                if st.form_submit_button("✅ Registrar Frequência"):
                    for aluno in st.session_state.alunos_db:
                        if aluno['id'] in lista_presenca:
                            if lista_presenca[aluno['id']]:
                                aluno['faltas_consecutivas'] = 0
                            else:
                                aluno['faltas_consecutivas'] += 1
                    salvar_dados("alunos")
                    st.success("Frequência gravada e enviada para conferência da direção!")
                    st.rerun()

        elif menu_prof == "📅 Planejamento Quinzenal":
            st.header("📅 Planejamento Pedagógico Quinzenal")
            with st.form("form_regular", clear_on_submit=True):
                mes = st.selectbox("Mês de Referência:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
                quinzena = st.radio("Quinzena:", ["1ª Quinzena", "2ª Quinzena"], horizontal=True)
                materia = st.selectbox("Área / Matéria:", MATERIAS_PLANEJAMENTO)
                atividades = st.text_area("Descrição Detalhada das Vivências Pedagógicas:")
                if st.form_submit_button("💾 Salvar e Enviar Cópia"):
                    salvar_dados("plan", {"professor": usuario['nome'], "turma": usuario['turma'], "mes": mes, "quinzena": quinzena, "materia": materia, "conteudo": atividades})
                    st.success(f"Plano quinzenal salvo! Uma cópia de segurança foi disparada para o e-mail: {usuario['email']}")

        elif menu_prof == "👶 Ocorrências da Rotina":
            st.header("🚨 Livro de Ocorrências Diárias")
            with st.form("form_ocorrencia", clear_on_submit=True):
                aluno_ocorrencia = st.selectbox("Criança envolvida:", [a['nome'] for a in alunos_turma])
                tipo_ocorrencia = st.selectbox("Tipo de Evento:", ["Mordida/Arranhão", "Queda/Escoriação", "Febre/Sintomas de Saúde", "Indisposição Alimentar", "Outros"])
                gravidade = st.select_slider("Classificação de Gravidade:", options=["Leve", "Média", "Alta"])
                detalhes = st.text_area("Descrição detalhada:")
                if st.form_submit_button("💾 Registrar Ocorrência"):
                    salvar_dados("ocorrencias", {"professor": usuario['nome'], "turma": usuario['turma'], "aluno": aluno_ocorrencia, "tipo": tipo_ocorrencia, "gravidade": gravidade, "detalhes": detalhes})
                    st.success("Ocorrência guardada! A coordenação já recebeu o alerta visual.")

        elif menu_prof == "📋 Atas & Conselhos":
            st.header("📋 Ata de Conselho de Classe")
            with st.form("form_ata", clear_on_submit=True):
                trimestre = st.selectbox("Trimestre de Avaliação", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
                deliberacoes = st.text_area("Parecer Coletivo e Deliberações:")
                if st.form_submit_button("📝 Registrar Ata"):
                    salvar_dados("atas", {"trimestre": trimestre, "turma": usuario['turma'], "conteudo": deliberacoes, "emissor": usuario['nome']})
                    st.success("Ata gravada!")
                    st.rerun()

            if st.session_state.atas_salvas:
                st.divider()
                ultima_ata = st.session_state.atas_salvas[-1]
                st.html("<div style='border: 2px solid #333; padding: 25px; background-color: #fff; color: #111; font-family: monospace; margin-bottom: 20px;'><h4 style='text-align: center;'>ATA OFICIAL DE CONSELHO PEDAGÓGICO</h4></div>")
                st.write(f"**Trimestre:** {ultima_ata['trimestre'].upper()} | **Turma:** {ultima_ata['turma'].upper()}")
                st.info(ultima_ata['conteudo'])
                st.write("Assinaturas de Todos os Professores Cadastrados (Pronto para Impressão):")
                for p_id, p_info in st.session_state.professores_db.items():
                    if p_info['cargo'] in ["Professor Regular", "Professor AEE"]:
                        st.write(f"✍️ {p_info['nome'].upper()} ({p_info['cargo']}) ________________________")

    # =====================================================================
    # PERFIL: PROFESSOR AEE
    # =====================================================================
    elif usuario['cargo'] == "Professor AEE":
        st.header("🧩 Atendimento Educacional Especializado (AEE)")
        menu_aee = st.selectbox("Selecione a Ação:", ["Lançar Prontuário/PDI", "Visualizar Fichas Completas"])
        
        if menu_aee == "Lançar Prontuário/PDI":
            with st.form("form_aee_pdi", clear_on_submit=True):
                aluno_aee = st.selectbox("Criança Atendida:", [a['nome'] for a in st.session_state.alunos_db])
                objetivos = st.text_area("Objetivos de Flexibilização Curricular:")
                recursos = st.text_area("Recursos Pedagógicos e Tecnologias Utilizadas:")
                if st.form_submit_button("💾 Salvar Dados AEE"):
                    for a in st.session_state.alunos_db:
                        if a['nome'] == aluno_aee:
                            a['relatorios_aee'] = f"Objetivos: {objetivos} | Recursos: {recursos}"
                    salvar_dados("alunos")
                    st.success("Dados salvos e injetados diretamente na ficha global do aluno!")

        elif menu_aee == "Visualizar Fichas Completas":
            aluno_sel = st.selectbox("Selecione o Aluno:", [a['nome'] for a in st.session_state.alunos_db])
            for a in st.session_state.alunos_db:
                if a['nome'] == aluno_sel:
                    st.markdown(f"### Ficha do Aluno: {a['nome']}")
                    st.write(f"🧩 **Relatório AEE:** {a.get('relatorios_aee', 'Nenhum lançado')}")
                    st.write(f"Fono/TO/Psicologia (Terapias Externas): {a.get('terapias', 'Nenhuma')}")
                    st.write(f"Dias/Horários de Terapias: {a.get('dias_horarios_terapias', 'Não informado')}")

    # =====================================================================
    # PERFIL: ADMINISTRADOR (DIREÇÃO)
    # =====================================================================
    elif usuario['cargo'] == "Administrador":
        st.header("⚙️ Painel de Controle da Direção e Coordenação")
        
        # 1. CENTRAL DE ALERTAS DE EVASÃO ESCOLAR
        st.subheader("🚨 Central de Alertas Críticos (Faltas Consecutivas >= 3)")
        alertas_ativos = False
        for aluno in st.session_state.alunos_db:
            if aluno['faltas_consecutivas'] >= 3:
                alertas_ativos = True
                st.error(f"⚠️ **ALERTA CRÍTICO:** A criança **{aluno['nome']}** da turma **{aluno['turma']}** faltou {aluno['faltas_consecutivas']} dias seguidos! Contato dos Pais: {aluno['contato']}")
        if not alertas_ativos: 
            st.success("✅ Nenhuma evasão detectada nas turmas.")
            
        st.divider()
        
        # 2. ABAS DE CONTROLE GERAL DA DIREÇÃO
        maba1, maba2, maba3, maba4 = st.tabs(["👥 Gerenciar Professores", "👶 Gerenciar Alunos", "📅 Ver Planejamentos", "📋 Histórico de Ocorrências"])
        
        with maba1:
            st.subheader("Gerenciamento de Funcionários")
            acao_p = st.radio("Operação (Professores):", ["Cadastrar Novo", "Editar Perfil", "Excluir Registro"], horizontal=True)
            if acao_p == "Cadastrar Novo":
                with st.form("add_prof", clear_on_submit=True):
                    mat_n = st.text_input("Nova Matrícula (Código de Acesso):")
                    nome_p = st.text_input("Nome Completo:")
                    cargo_p = st.selectbox("Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"])
                    turma_p = st.selectbox("Turma Atribuída:", TURMAS_ESCOLARES)
                    email_p = st.text_input("E-mail para envio de Planos:")
                    if st.form_submit_button("➕ Salvar Funcionário"):
                        if mat_n and nome_p:
                            st.session_state.professores_db[mat_n] = {"nome": nome_p, "cargo": cargo_p, "turma": turma_p, "email": email_p}
                            salvar_dados("db")
                            st.success(f"{nome_p} cadastrado!")
                            st.rerun()
                            
            elif acao_p == "Editar Perfil":
                p_sel = st.selectbox("Selecione para Edit:", list(st.session_state.professores_db.keys()), format_func=lambda x: f"{st.session_state.professores_db[x]['nome']} ({x})")
                with st.form("edit_prof"):
                    nome_e = st.text_input("Alterar Nome:", value=st.session_state.professores_db[p_sel]['nome'])
                    cargo_e = st.selectbox("Alterar Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"], index=["Professor Regular", "Professor AEE", "Monitor", "Administrador"].index(st.session_state.professores_db[p_sel]['cargo']))
                    turma_e = st.selectbox("Alterar Turma:", TURMAS_ESCOLARES, value=st.session_state.professores_db[p_sel]['turma'])
                    email_e = st.text_input("Alterar E-mail:", value=st.session_state.professores_db[p_sel].get('email', ''))
                    if st.form_submit_button("💾 Atualizar Dados"):
                        st.session_state.professores_db[p_sel] = {"nome": nome_e, "cargo": cargo_e, "turma": turma_e, "email": email_e}
                        salvar_dados("db")
                        st.success("Dados updated!")
                        st.rerun()
                        
            elif acao_p == "Excluir Registro":
                p_del = st.selectbox("Selecione para Deletar:", list(st.session_state.professores_db.keys()), format_func=lambda x: f"{st.session_state.professores_db[x]['nome']} ({x})")
                if st.button("❌ Confirmar Exclusão Definitiva"):
                    if p_del == matricula: st.error("Você não pode deletar sua própria conta activa.")
                    else:
                        del st.session_state.professores_db[p_del]
                        salvar_dados("db")
                        st.success("Removido!")
                        st.rerun()

        with maba2:
            st.subheader("Gerenciamento Geral de Matrículas")
            acao_a = st.radio("Operação (Alunos):", ["Cadastrar Novo Aluno", "Editar Ficha de Saúde & Terapias", "Excluir Aluno"], horizontal=True)
            
            if acao_a == "Cadastrar Novo Aluno":
                with st.form("add_aluno", clear_on_submit=True):
                    nome_n = st.text_input("Nome Completo do Aluno:")
                    turma_n = st.selectbox("Turma Escolar:", TURMAS_ESCOLARES)
                    alergias_n = st.text_input("Alergias:", value="Nenhuma")
                    rest_n = st.text_input("Restrições Alimentares:", value="Nenhuma")
                    retirada_n = st.text_input("Autorizados para Retirada:")
                    contato_n = st.text_input("Contatos de Emergência (Telefone):")
                    terapias_n = st.text_input("Faz terapias externas? Se sim, quais:", value="Nenhuma")
                    horario_t = st.text_input("Dias e Horários das Terapias:", value="Não informado")
                    if st.form_submit_button("➕ Registrar Criança"):
                        if nome_n:
                            novo_a = {
                                "id": str(len(st.session_state.alunos_db)+1), "nome": nome_n, "turma": turma_n, 
                                "alergias": alergias_n, "restricoes": rest_n, "retirada": retirada_n, "contato": contato_n, 
                                "relatorios_aee": "Nenhum lançado", "encaminhamentos": "Nenhum lançado",
                                "terapias": terapias_n, "dias_horarios_terapias": horario_t,
                                "foto": "👶", "faltas_consecutivas": 0
                            }
                            st.session_state.alunos_db.append(novo_a)
                            salvar_dados("alunos")
                            st.success(f"{nome_n} matriculado com ficha completa!")
                            st.rerun()
                            
            elif acao_a == "Editar Ficha de Saúde & Terapias":
                a_sel_idx = st.selectbox("Selecione a Criança:", range(len(st.session_state.alunos_db)), format_func=lambda x: st.session_state.alunos_db[x]['nome'])
                aluno_e = st.session_state.alunos_db[a_sel_idx]
                with st.form("edit_aluno"):
                    nome_ae = st.text_input("Nome:", value=aluno_e['nome'])
                    turma_ae = st.selectbox("Turma:", TURMAS_ESCOLARES, index=TURMAS_ESCOLARES.index(aluno_e['turma']) if aluno_e['turma'] in TURMAS_ESCOLARES else 0)
                    alergias_ae = st.text_input("Alergias:", value=aluno_e['alergias'])
                    rest_ae = st.text_input("Restrições:", value=aluno_e['restricoes'])
                    retirada_ae = st.text_input("Retirada:", value=aluno_e['retirada'])
                    contato_ae = st.text_input("Contatos:", value=aluno_e['contato'])
                    rel_aee = st.text_area("Relatórios / PDI do AEE:", value=aluno_e.get('relatorios_aee', ''))
                    encam_ae = st.text_area("Encaminhamentos Clínicos:", value=aluno_e.get('encaminhamentos', ''))
                    ter_ae = st.text_input("Terapias Externas:", value=aluno_e.get('terapias', ''))
                    hor_ae = st.text_input("Dias/Horários de Terapias:", value=aluno_e.get('dias_horarios_terapias', ''))
                    
                    if st.form_submit_button("💾 Salvar Alterações Globais"):
                        st.session_state.alunos_db[a_sel_idx] = {
                            "id": aluno_e['id'], "nome": nome_ae, "turma": turma_ae, "alergias": alergias_ae, 
                            "restricoes": rest_ae, "retirada": retirada_ae, "contato": contato_ae, 
                            "relatorios_aee": rel_aee, "encaminhamentos": encam_ae, "terapias": ter_ae, 
                            "dias_horarios_terapias": hor_ae, "foto": aluno_e['foto'], "faltas_consecutivas": aluno_e['faltas_consecutivas']
                        }
                        salvar_dados("alunos")
                        st.success("Ficha escolar updated!")
                        st.rerun()

            elif acao_a == "Excluir Aluno":
                a_del_idx = st.selectbox("Selecione o Aluno para Remover:", range(len(st.session_state.alunos_db)), format_func=lambda x: f"{st.session_state.alunos_db[x]['nome']} ({st.session_state.alunos_db[x]['turma']})")
                if st.button("❌ Confirmar Exclusão do Aluno"):
                    st.session_state.alunos_db.pop(a_del_idx)
                    salvar_dados("alunos")
                    st.success("Removido!")
                    st.rerun()
# =====================================================================
# PERFIL: PROFESSOR AEE (Inclusão, Histórico de PDI/PEI e Exportação)
# =====================================================================
def tela_professor_aee(usuario):
    st.header("🧩 Atendimento Educacional Especializado (AEE)")
    menu_aee = st.selectbox("Selecione a Ação:", ["Lançar Prontuário / PDI / PEI", "Visualizar e Exportar Histórico"])
    
    if menu_aee == "Lançar Prontuário / PDI / PEI":
        with st.form("form_aee_pdi", clear_on_submit=True):
            aluno_aee = st.selectbox("Criança Atendida:", [a['nome'] for a in st.session_state.alunos_db])
            periodo_ano = st.selectbox("Período do Relatório:", ["1º Trimestre / PEI", "2º Trimestre / PEI", "3º Trimestre / PEI", "Relatório de Evolução Anual"])
            objetivos = st.text_area("Objetivos de Flexibilização Curricular (PDI):")
            recursos = st.text_area("Recursos Pedagógicos e Tecnologias Assistivas Utilizadas:")
            
            if st.form_submit_button("💾 Salvar Parecer Pedagógico"):
                # Inicializa o histórico de relatórios na ficha se não existir
                for a in st.session_state.alunos_db:
                    if a['nome'] == aluno_aee:
                        if 'historico_aee' not in a or isinstance(a['historico_aee'], str):
                            a['historico_aee'] = []
                        
                        # Adiciona o novo relatório sem apagar os anteriores do ano
                        a['historico_aee'].append({
                            "periodo": periodo_ano,
                            "data_registro": date.today().strftime("%d/%m/%Y"),
                            "objetivos": objetivos,
                            "recursos": recursos,
                            "professor": usuario['nome']
                        })
                salvar_dados("alunos")
                st.success(f"Documento do {periodo_ano} para {aluno_aee} arquivado no sistema!")

    elif menu_aee == "Visualizar e Exportar Histórico":
        aluno_sel = st.selectbox("Selecione o Aluno para Ver Ficha Completa:", [a['nome'] for a in st.session_state.alunos_db])
        for a in st.session_state.alunos_db:
            if a['nome'] == aluno_sel:
                st.markdown(f"### Prontuário Clínico-Pedagógico: {a['nome']}")
                st.write(f"🩺 **Terapias Externas:** {a.get('terapias', 'Nenhuma registrada')}")
                st.write(f"⏱️ **Horários Clínicos:** {a.get('dias_horarios_terapias', 'Não informado')}")
                st.write(f"📋 **Encaminhamentos:** {a.get('encaminhamentos', 'Nenhum lançado')}")
                
                st.divider()
                st.subheader("📚 Histórico de PDI / PEI deste Ano")
                
                historico = a.get('historico_aee', [])
                if not historico:
                    st.info("Nenhum relatório trimestral lançado para esta criança ainda.")
                else:
                    for idx, rel in enumerate(historico):
                        with st.container(border=True):
                            st.markdown(f"#### 🧩 {rel['periodo']} — Gravado em {rel['data_registro']}")
                            st.markdown(f"**Professor Responsável:** {rel['professor']}")
                            st.write(f"**Objetivos e Metas:** {rel['objetivos']}")
                            st.write(f"**Recursos Utilizados:** {rel['recursos']}")
                            
                            # Monta o texto limpo para exportar
                            texto_documento = f"RELATÓRIO DE INCLUSÃO - Ary Levy\nAluno: {a['nome']}\nTurma: {a['turma']}\nDocumento: {rel['periodo']}\nData: {rel['data_registro']}\n\nOBJETIVOS:\n{rel['objetivos']}\n\nRECURSOS:\n{rel['recursos']}"
                            
                            # Botão nativo para baixar como arquivo compatível com Word (.doc)
                            st.download_button(
                                label="📥 Baixar este Relatório para o Word",
                                data=texto_documento.encode('utf-8'),
                                file_name=f"Relatorio_{rel['periodo'].replace(' ', '_')}_{a['nome'].replace(' ', '_')}.doc",
                                mime="application/msword",
                                key=f"down_{idx}"
                            )

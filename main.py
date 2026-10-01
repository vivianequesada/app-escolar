import streamlit as st
import json
import os
from datetime import date

# =====================================================================
# 1. CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
# =====================================================================
st.set_page_config(page_title="🧸 Portal de Gestão da Educação Infantil", layout="wide", page_icon="🧸")

# DIRETÓRIOS E BANCOS DE DADOS LOCAL (JSON)
DB_FILE = "professores_db.json"
ALUNOS_FILE = "alunos_db.json"
ATAS_FILE = "atas_db.json"
PLAN_FILE = "planejamentos_db.json"
OCORRENCIAS_FILE = "ocorrencias_db.json"
UPLOAD_DIR = "documentos_pdf"

# Cria a pasta física para armazenar os arquivos PDF se ela não existir
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# CONFIGURAÇÕES ESCOLARES ATUALIZADAS
TURMAS_ESCOLARES = [
    "Berçário I", "Berçário II", "Maternal I", 
    "Maternal II - 1", "Maternal II - 2", 
    "1ª etapa - 1", "1ª etapa - 2", 
    "2ª etapa - 1", "2ª etapa - 2", "Geral"
]

MATERIAS_PEDAGOGICAS = [
    "Linguagem Verbal", "Linguagem Matemática", 
    "Indivíduo e Sociedade", "Cultura, Corpo e Movimento", 
    "Artes", "AEE"
]

# =====================================================================
# 2. CARGA E PERSISTÊNCIA DE DADOS (JSON)
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
                "historico_aee": [], "encaminhamentos": "Nenhum lançado",
                "terapias": "Terapia Ocupacional e Fonoaudiologia",
                "dias_horarios_terapias": "Terças e Quintas às 14:00",
                "foto": "👶", "faltas_consecutivas": 0,
                "arquivos_pdf": []
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
# 3. LOGIN NA BARRA LATERAL
# =====================================================================
st.sidebar.title("🔐 Acesso ao Painel")
matricula = st.sidebar.text_input("Matrícula", type="password")

usuario = None
if matricula in st.session_state.professores_db:
    usuario = st.session_state.professores_db[matricula]
    st.sidebar.success(f"Conectado: {usuario['nome']}")
    st.sidebar.info(f"Função: {usuario['cargo']}")
elif matricula:
    st.sidebar.error("Matrícula incorreta.")

# =====================================================================
# 4. EXECUÇÃO DE TELAS POR PERFIL
# =====================================================================
if usuario:
    st.title("🧸 Portal de Gestão da Educação Infantil")
    st.divider()

    # PERFIL: MONITORES
    if usuario['cargo'] == "Monitor":
        st.header("🚨 Carômetro de Segurança & Fichas Médicas Rápidas")
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
        menu_prof = st.selectbox("Selecione o Módulo de Trabalho:", ["📝 Diário & Chamada", "📅 Planejamento Quinzenal", "👶 Ocorrências da Rotina", "📋 Atas de Conselho (Por Matéria)"])
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
                    st.success("Frequência registrada com sucesso!")
                    st.rerun()

        elif menu_prof == "📅 Planejamento Quinzenal":
            st.header("📅 Planejamento Pedagógico Quinzenal")
            with st.form("form_regular", clear_on_submit=True):
                mes = st.selectbox("Mês de Reference:", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
                quinzena = st.radio("Quinzena:", ["1ª Quinzena", "2ª Quinzena"], horizontal=True)
                materia = st.selectbox("Componente Curricular / Matéria:", MATERIAS_PEDAGOGICAS)
                atividades = st.text_area("Descrição Detalhada das Vivências Pedagógicas:")
                if st.form_submit_button("💾 Salvar Planejamento"):
                    salvar_dados("plan", {"professor": usuario['nome'], "turma": usuario['turma'], "mes": mes, "quinzena": quinzena, "materia": materia, "conteudo": atividades})
                    st.success(f"Plano quinzenal salvo! Uma cópia de segurança foi enviada para seu e-mail: {usuario['email']}")

        elif menu_prof == "👶 Ocorrências da Rotina":
            st.header("🚨 Livro de Ocorrências Diárias (Mordidas / Arranhões / Quedas)")
            with st.form("form_ocorrencia", clear_on_submit=True):
                aluno_ocorrencia = st.selectbox("Criança envolvida:", [a['nome'] for a in alunos_turma])
                tipo_ocorrencia = st.selectbox("Tipo de Evento:", ["Mordida/Arranhão", "Queda/Escoriação", "Febre/Sintomas de Saúde", "Indisposição Alimentar", "Outros"])
                gravidade = st.select_slider("Classificação de Gravidade:", options=["Leve", "Média", "Alta"])
                detalhes = st.text_area("Descrição detalhada:")
                if st.form_submit_button("💾 Registrar Ocorrência"):
                    salvar_dados("ocorrencias", {"professor": usuario['nome'], "turma": usuario['turma'], "aluno": aluno_ocorrencia, "tipo": tipo_ocorrencia, "gravidade": gravidade, "detalhes": detalhes})
                    st.success("Ocorrência guardada no livro oficial!")

        elif menu_prof == "📋 Atas de Conselho (Por Matéria)":
            st.header("📋 Lançamento de Ata de Conselho de Classe Estruturada")
            with st.form("form_ata_materias", clear_on_submit=True):
                trimestre = st.selectbox("Trimestre Letivo:", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
                
                st.write("### Deliberações Separadas por Componente:")
                d_corp = st.text_area("4. Cultura, Corpo e Movimento:")
                d_artes = st.text_area("5. Artes:")
                d_aee = st.text_area("6. Flexibilizações AEE:")
                
                if st.form_submit_button("📝 Protocolar e Consolidar Ata"):
                    payload_ata = {
                        "trimestre": trimestre, "turma": usuario['turma'], "emissor": usuario['nome'],
                        "dados": {
                            "Linguagem Verbal": d_verbal, "Linguagem Matemática": d_mat,
                            "Indivíduo e Sociedade": d_soc, "Cultura, Corpo e Movimento": d_corp,
                            "Artes": d_artes, "AEE": d_aee
                        }
                    }
                    salvar_dados("atas", payload_ata)
                    st.success("Ata unificada processada com sucesso!")
                    st.rerun()

            if st.session_state.atas_salvas:
                st.divider()
                ultima = st.session_state.atas_salvas[-1]
                
                html_ata = f"""
                <div id="documento-ata" style="border: 2px solid #333; padding: 30px; background-color: #fff; color: #111; font-family: 'Courier New', monospace; max-width: 800px; margin: auto;">
                    <h2 style="text-align: center; margin-bottom: 5px;">ATA DE CONSELHO DE CLASSE CONSOLIDADA</h2>
                    <p style="text-align: center; font-size: 14px; margin-top: 0;"><b>{ultima['trimestre'].upper()}</b> | TURMA: {ultima['turma'].upper()}</p>
                    <p style="font-size: 13px;"><b>Coordenador Responsável:</b> {ultima['emissor']}</p>
                    <hr style="border-top: 1px solid #333;">
                """
                for mat, text in ultima["dados"].items():
                    html_ata += f"<h4>📌 {mat.upper()}:</h4><p style='text-align: justify; font-size: 13px;'>{text if text.strip() else 'Sem apontamentos neste período.'}</p>"
                
                html_ata += "<br><hr style='border-top: 1px solid #333;'><h4>✍️ ASSINATURAS DOS PROFESSORES INTEGRADOS:</h4><br>"
                for p_id, p_info in st.session_state.professores_db.items():
                    if p_info['cargo'] in ["Professor Regular", "Professor AEE"]:
                        html_ata += f"<p style='font-size: 13px; margin-bottom: 25px;'>{p_info['nome'].upper()} ({p_info['cargo']}) ____________________________________</p>"
                
                html_ata += f"</div><br><div style='text-align: center;'><button onclick=" + '"' + "var win = window.open('', '_blank'); win.document.write(document.getElementById('documento-ata').outerHTML); win.document.close(); win.print();" + '"' + " style='padding: 10px 20px; font-size: 14px; background-color: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer;'>🖨️ Abrir Tela de Impressão (Salvar como PDF)</button></div>"
                st.html(html_ata)

    # =====================================================================
    # PERFIL: PROFESSOR AEE
    # =====================================================================
    elif usuario['cargo'] == "Professor AEE":
        st.header("🧩 Atendimento Educacional Especializado (AEE / PDI / PEI)")
        menu_aee = st.selectbox("Módulos:", ["Lançar Relatório Trimestral (PEI)", "Anexar Arquivo PDF Externo", "Histórico do Aluno"])
        
        if menu_aee == "Lançar Relatório Trimestral (PEI)":
            with st.form("form_aee_pdi", clear_on_submit=True):
                aluno_aee = st.selectbox("Criança Atendida:", [a['nome'] for a in st.session_state.alunos_db])
                periodo_ano = st.selectbox("Período Clínico:", ["1º Trimestre / PEI", "2º Trimestre / PEI", "3º Trimestre / PEI"])
                objetivos = st.text_area("Objetivos de Flexibilização Curricular (PDI):")
                recursos = st.text_area("Recursos Pedagógicos e Estratégias:")
                if st.form_submit_button("💾 Salvar Parecer Pedagógico"):
                    for a in st.session_state.alunos_db:
                        if a['nome'] == aluno_aee:
                            if 'historico_aee' not in a or not isinstance(a['historico_aee'], list):
                                a['historico_aee'] = []
                            a['historico_aee'].append({
                                "periodo": periodo_ano, "data_registro": date.today().strftime("%d/%m/%Y"),
                                "objetivos": objetivos, "recursos": recursos, "professor": usuario['nome']
                            })
                    salvar_dados("alunos")
                    st.success("Parecer arquivado com sucesso!")
                    
        elif menu_aee == "Anexar Arquivo PDF Externo":
            st.subheader("📁 Upload de Documentos e Laudos em PDF")
            aluno_upload = st.selectbox("Selecione o Aluno para Vincular o Documento:", [a['nome'] for a in st.session_state.alunos_db])
            arquivo_enviado = st.file_uploader("Escolha o arquivo PDF do Relatório/PEI/Laudo:", type=["pdf"])
            nome_doc = st.text_input("Nome/Identificação do Documento:", placeholder="Ex: PEI Assinado 1 Trimestre")
            if st.button("➕ Upload e Salvar no Prontuário"):
                if arquivo_enviado is not None and nome_doc.strip():
                    nome_limpo = f"{aluno_upload.replace(' ', '')}{nome_doc.replace(' ', '_')}.pdf"
                    caminho_salvamento = os.path.join(UPLOAD_DIR, nome_limpo)
                    with open(caminho_salvamento, "wb") as f:
                        f.write(arquivo_enviado.getbuffer())
                    for a in st.session_state.alunos_db:
                        if a['nome'] == aluno_upload:
                            if 'arquivos_pdf' not in a:
                                a['arquivos_pdf'] = []
                            a['arquivos_pdf'].append({
                                "nome": nome_doc,
                                "data": date.today().strftime("%d/%m/%Y"),
                                "caminho": caminho_salvamento
                            })
                    salvar_dados("alunos")
                    st.success(f"O documento '{nome_doc}' foi anexado com sucesso à ficha de {aluno_upload}!")
                    st.rerun()
                else:
                    st.error("Por favor, selecione um arquivo PDF válido e dê um nome descritivo ao documento.")

        elif menu_aee == "Histórico do Aluno":
            aluno_sel = st.selectbox("Selecione o Aluno:", [a['nome'] for a in st.session_state.alunos_db])
            for a in st.session_state.alunos_db:
                if a['nome'] == aluno_sel:
                    st.write(f"🩺 Terapias Externas: {a.get('terapias','Nenhuma')}")
                    st.write(f"⏱️ Dias/Horários Clínicos: {a.get('dias_horarios_terapias','Não informado')}")
                    historico = a.get('historico_aee', [])
                    if historico:
                        st.subheader("📚 Histórico de Relatórios Digitados")
                        for rel in historico:
                            with st.container(border=True):
                                st.markdown(f"##### {rel['periodo']} (Gravado em {rel['data_registro']})")
                                st.write(f"Objetivos: {rel['objetivos']}")
                                st.write(f"Recursos: {rel['recursos']}")
                    arquivos_salvos = a.get('arquivos_pdf', [])
                    if arquivos_salvos:
                        st.write("---")
                        st.subheader("📁 Arquivos PDF Anexados no Prontuário")
                        for doc_anexo in arquivos_salvos:
                            with st.container(border=True):
                                c_doc1, c_doc2 = st.columns()
                                c_doc1.write(f"📄 {doc_anexo['nome']} (Anexado em {doc_anexo['data']})")
                                if os.path.exists(doc_anexo['caminho']):
                                    with open(doc_anexo['caminho'], "rb") as f_pdf:
                                        c_doc2.download_button(
                                            label="📥 Abrir PDF",
                                            data=f_pdf.read(),
                                            file_name=os.path.basename(doc_anexo['caminho']),
                                            mime="application/pdf",
                                            key=doc_anexo['caminho']
                                        )

    # =====================================================================
    # PERFIL: ADMINISTRADOR (DIREÇÃO)
    # =====================================================================
    elif usuario['cargo'] == "Administrador":
        st.header("⚙️ Painel de Controle da Direção e Coordenação")
        
        # ALERTA DE EVASÃO AUTOMÁTICO EXIGIDO POR VOCÊ
        st.subheader("🚨 Central de Alertas Críticos (Faltas Consecutivas >= 3)")
        alertas_ativos = False
        for aluno in st.session_state.alunos_db:
            if aluno['faltas_consecutivas'] >= 3:
                alertas_ativos = True
                st.error(f"⚠️ RISCO DE EVASÃO DETECTADO: A criança {aluno['nome']} ({aluno['turma']}) acumulou {aluno['faltas_consecutivas']} faltas consecutivas! Contato dos pais para busca ativa: {aluno['contato']}")
        if not alertas_ativos:
            st.success("✅ Nenhuma evasão detectada nas turmas de Educação Infantil.")
        st.divider()
        
        maba1, maba2, maba3, maba4 = st.tabs(["👥 Gerenciar Professores", "👶 Matricular Alunos", "📅 Ver Planejamentos", "📋 Histórico de Ocorrências"])
        with maba1:
            st.subheader("Gerenciamento de Funcionários")
            acao_p = st.radio("Operação (Professores):", ["Cadastrar Novo", "Editar Perfil", "Excluir Registro"], horizontal=True)
            if acao_p == "Cadastrar Novo":
                with st.form("add_prof", clear_on_submit=True):
                    mat_n = st.text_input("Nova Matrícula (Código de Acesso):")
                    nome_p = st.text_input("Nome Completo:")
                    cargo_p = st.selectbox("Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"])
                    turma_p = st.selectbox("Turma Atribuída:", TURMAS_ESCOLARES)
                    email_p = st.text_input("E-mail corporativo:")
                    if st.form_submit_button("➕ Salvar Funcionário"):
                        if mat_n and nome_p:
                            st.session_state.professores_db[mat_n] = {"nome": nome_p, "cargo": cargo_p, "turma": turma_p, "email": email_p}
                            salvar_dados("db")
                            st.success(f"{nome_p} cadastrado!")
                            st.rerun()
                            
            elif acao_p == "Editar Perfil":
                p_sel = st.selectbox("Selecione para Editar:", list(st.session_state.professores_db.keys()), format_func=lambda x: f"{st.session_state.professores_db[x]['nome']} ({x})")
                with st.form("edit_prof"):
                    nome_e = st.text_input("Alterar Nome:", value=st.session_state.professores_db[p_sel]['nome'])
                    cargo_e = st.selectbox("Alterar Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"], index=["Professor Regular", "Professor AEE", "Monitor", "Administrador"].index(st.session_state.professores_db[p_sel]['cargo']))
                    turma_atual = st.session_state.professores_db[p_sel]['turma']
                    idx_turma = TURMAS_ESCOLARES.index(turma_atual) if turma_atual in TURMAS_ESCOLARES else 0
                    turma_e = st.selectbox("Alterar Turma:", TURMAS_ESCOLARES, index=idx_turma)
                    email_e = st.text_input("Alterar E-mail:", value=st.session_state.professores_db[p_sel].get('email',''))
                    if st.form_submit_button("💾 Atualizar Dados"):
                        st.session_state.professores_db[p_sel] = {"nome": nome_e, "cargo": cargo_e, "turma": turma_e, "email": email_e}
                        salvar_dados("db")
                        st.success("Dados updated!")
                        st.rerun()
                        
        with maba2:
            st.subheader("Gerenciamento do Carômetro de Alunos")
            acao_a = st.radio("Operação (Alunos):", ["Cadastrar Novo Aluno", "Editar Ficha de Saúde & Terapias", "Excluir Aluno"], horizontal=True)
            if acao_a == "Cadastrar Novo Aluno":
                with st.form("add_aluno", clear_on_submit=True):
                    nome_n = st.text_input("Nome Completo do Aluno:")
                    turma_n = st.selectbox("Turma Escolar:", TURMAS_ESCOLARES)
                    salvar_dados("db")

import streamlit as st
import json
import os

# CONFIGURAÇÃO DA PÁGINA (Deve ser o primeiro comando Streamlit)
st.set_page_config(page_title="Gestão Escolar - Educação Infantil", layout="wide", page_icon="🧸")

# BANCOS DE DADOS EM FORMATO JSON
DB_FILE = "professores_db.json"
ATAS_FILE = "atas_db.json"
PLAN_FILE = "planejamentos_db.json"
ALUNOS_FILE = "alunos_db.json"
OCORRENCIAS_FILE = "ocorrencias_db.json"

def carregar_dados():
    if not os.path.exists(DB_FILE):
        default_profs = {
            "123": {"nome": "Regina Mello", "cargo": "Professor Regular", "turma": "Maternal I"},
            "456": {"nome": "Paula Souza", "cargo": "Professor AEE", "turma": "Inclusão Geral"},
            "789": {"nome": "Coordenação/Direção", "cargo": "Administrador", "turma": "Geral"},
            "000": {"nome": "Acesso Monitores", "cargo": "Monitor", "turma": "Plantão"}
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(default_profs, f, ensure_ascii=False, indent=4)
            
    if not os.path.exists(ALUNOS_FILE):
        default_alunos = [
            {"id": "1", "nome": "Arthur Silva", "turma": "Maternal I", "alergias": "Frutos do mar", "restricoes": "Intolerante a Lactose", "retirada": "Pais (Marcos e Ana)", "contato": "(11) 98888-7777", "foto": "👶", "faltas_consecutivas": 0},
            {"id": "2", "nome": "Beatriz Souza", "turma": "Maternal I", "alergias": "Nenhuma", "restricoes": "Nenhuma", "retirada": "Pais e Avó", "contato": "(11) 97777-6666", "foto": "👧", "faltas_consecutivas": 3}
        ]
        with open(ALUNOS_FILE, "w", encoding="utf-8") as f:
            json.dump(default_alunos, f, ensure_ascii=False, indent=4)

    for f_path in [ATAS_FILE, PLAN_FILE, OCORRENCIAS_FILE]:
        if not os.path.exists(f_path):
            with open(f_path, "w", encoding="utf-8") as f: 
                json.dump([], f)

    with open(DB_FILE, "r", encoding="utf-8") as f: 
        st.session_state.professores_db = json.load(f)
    with open(ALUNOS_FILE, "r", encoding="utf-8") as f: 
        st.session_state.alunos_db = json.load(f)
    with open(ATAS_FILE, "r", encoding="utf-8") as f: 
        st.session_state.atas_salvas = json.load(f)
    with open(PLAN_FILE, "r", encoding="utf-8") as f: 
        st.session_state.planejamentos_salvos = json.load(f)
    with open(OCORRENCIAS_FILE, "r", encoding="utf-8") as f: 
        st.session_state.ocorrencias_salvas = json.load(f)

def salvar_dados(chave, payload=None):
    if chave == "alunos":
        with open(ALUNOS_FILE, "w", encoding="utf-8") as f: 
            json.dump(st.session_state.alunos_db, f, ensure_ascii=False, indent=4)
    elif chave == "db":
        with open(DB_FILE, "w", encoding="utf-8") as f: 
            json.dump(st.session_state.professores_db, f, ensure_ascii=False, indent=4)
    elif chave == "ocorrencias":
        if payload: 
            st.session_state.ocorrencias_salvas.append(payload)
        with open(OCORRENCIAS_FILE, "w", encoding="utf-8") as f: 
            json.dump(st.session_state.ocorrencias_salvas, f, ensure_ascii=False, indent=4)
    else:
        arquivo = ATAS_FILE if chave == "atas" else PLAN_FILE
        lista = st.session_state.atas_salvas if chave == "atas" else st.session_state.planejamentos_salvos
        if payload: 
            lista.append(payload)
        with open(arquivo, "w", encoding="utf-8") as f: 
            json.dump(lista, f, ensure_ascii=False, indent=4)

carregar_dados()

# LOGIN NA BARRA LATERAL
st.sidebar.title("🔐 Acesso ao Painel")
matricula = st.sidebar.text_input("Matrícula", type="password")

if matricula in st.session_state.professores_db:
    usuario = st.session_state.professores_db[matricula]
    st.sidebar.success(f"Conectado: {usuario['nome']}")
    st.sidebar.info(f"Função: {usuario['cargo']}")
    
    st.title("🧸 Portal de Gestão da Educação Infantil")
    st.divider()

    # PERFIL: MONITORES
    if usuario['cargo'] == "Monitor":
        st.header("🚨 Carômetro de Segurança Escolar (Acesso Rápido)")
        busca = st.text_input("🔍 Buscar Criança pelo Nome:")
        
        for aluno in st.session_state.alunos_db:
            if busca.lower() in aluno['nome'].lower():
                with st.expander(f"{aluno['foto']} {aluno['nome']} - {aluno['turma']}", expanded=True):
                    c1, c2 = st.columns(2)
                    with c1:
                        st.markdown(f"🔴 **Alergias:** {aluno['alergias']}")
                        st.markdown(f"🥛 **Restrições Alimentares:** {aluno['restricoes']}")
                    with c2:
                        st.markdown(f"🪪 **Autorização de Retirada:** {aluno['retirada']}")
                        st.markdown(f"📞 **Telefones de Contato:** {aluno['contato']}")

    # PERFIL: PROFESSOR REGULAR
    elif usuario['cargo'] == "Professor Regular":
        st.subheader(f"Sala Virtual: {usuario['turma']}")
               menu_professor = st.selectbox(
            "Selecione o Módulo de Trabalho:",
            ["📝 Diário & Chamada", "📅 Planejamento BNCC", "👶 Ocorrências da Rotina", "📊 Relatório Descritivo", "📋 Atas & Conselhos", "🏢 Agendamento de Espaços", "📅 Calendário de Avaliações", "📢 Quadro de Avisos"]
        )        
    elif menu_professor == "🏢 Agendamento de Espaços":
            st.header("🏢 Agendamento de Espaços Coletivos")
            st.caption("O sistema gerencia o uso dos ambientes compartilhados da escola.")
            
            # Inicializa a lista de agendamentos no estado da sessão se não existir
            if "agendamentos_escola" not in st.session_state:
                st.session_state.agendamentos_escola = []
                
            espacos_disponiveis = ["Quadra / Pátio Externo", "Sala de Informática", "Espaço de Leitura / Brinquedoteca"]
            
            with st.form("form_reserva", clear_on_submit=True):
                espaco_sel = st.selectbox("Selecione o Ambiente:", espacos_disponiveis)
                data_reserva = st.date_input("Data do Uso:", value=os.datetime.date.today() if hasattr(os, 'datetime') else None)
                h_entrada = st.time_input("Horário de Entrada:")
                h_saida = st.time_input("Horário de Saída:")
                atividade_p = st.text_input("Atividade Pedagógica Planejada:", placeholder="Ex: Aula de Psicomotricidade")
                
                if st.form_submit_button("🗓️ Confirmar Agendamento de Horário"):
                    if atividade_p.strip():
                        # Checagem simples de conflito de horário
                        conflito = False
                        for ag in st.session_state.agendamentos_escola:
                            if ag["espaco"] == espaco_sel and ag["data"] == str(data_reserva) and (h_entrada < ag["saida"] and h_saida > ag["entrada"]):
                                conflito = True
                                st.error(f"⚠️ Conflito! O espaço já está reservado por {ag['professor']} para a turma {ag['turma']}.")
                                break
                        
                        if not conflito:
                            st.session_state.agendamentos_escola.append({
                                "espaco": espaco_sel, "data": str(data_reserva), 
                                "entrada": h_entrada, "saida": h_saida, 
                                "turma": usuario['turma'], "professor": usuario['nome'], "atividade": atividade_p
                            })
                            st.success("Ambiente reservado com sucesso!")
                            st.rerun()
                    else:
                        st.error("Por favor, informe a atividade planejada.")

            if st.session_state.agendamentos_escola:
                st.write("### 📅 Cronograma de Uso dos Ambientes")
                for ag in reversed(st.session_state.agendamentos_escola):
                    st.info(f"🏢 **{ag['espaco']}** | Dia: {ag['data']} ({ag['entrada'].strftime('%H:%M')} às {ag['saida'].strftime('%H:%M')}) -> Turma: **{ag['turma']}** (Resp: {ag['professor']})")

        elif menu_professor == "📅 Calendário de Avaliações":
            st.header("📅 Calendário de Avaliações e Acompanhamentos")
            if "avaliacoes_calendario" not in st.session_state:
                st.session_state.avaliacoes_calendario = []
                
            with st.form("form_avaliacao", clear_on_submit=True):
                tit_av = st.text_input("Nome do Acompanhamento/Avaliação:", placeholder="Ex: Portfólio do 1º Trimestre")
                tipo_av = st.selectbox("Instrumento:", ["Portfólio", "Ficha de Observação", "Relatório Individual", "Outro"])
                data_av = st.date_input("Data Limite de Postagem:")
                if st.form_submit_button("💾 Adicionar ao Calendário"):
                    if tit_av.strip():
                        st.session_state.avaliacoes_calendario.append({"titulo": tit_av, "tipo": tipo_av, "data": str(data_av), "turma": usuario['turma']})
                        st.success("Avaliação listada no calendário escolar!")
                        st.rerun()

            if st.session_state.avaliacoes_calendario:
                st.write("### 📌 Prazos Pedagógicos Ativos")
                for av in st.session_state.avaliacoes_calendario:
                    if av["turma"] == usuario['turma']:
                        st.warning(f"📆 **{av['titulo']}** ({av['tipo']}) — Entrega prevista até: {av['data']}")

        elif menu_professor == "📢 Quadro de Avisos":
            st.header("📢 Mural de Comunicados da Escola")
            st.caption("Avisos postados pela direção e coordenação pedagógica.")
            
            # Puxa o histórico de avisos gerais enviados do banco de comunicados
            if st.session_state.atas_salvas:
                for ata in reversed(st.session_state.atas_salvas):
                    with st.container(border=True):
                        st.markdown(f"**📢 COMUNICADO OFICIAL — {ata['trimestre'].upper()}**")
                        st.caption(f"Emitido por: {ata['emissor']} para a turma {ata['turma']}")
                        st.write(ata['conteudo'])
            else:
                st.info("Nenhum aviso listado no mural até o momento.")

        st.write("---")

        alunos_turma = [a for a in st.session_state.alunos_db if a['turma'] == usuario['turma']]

        if menu_professor == "📝 Diário & Chamada":
            st.header("📋 Chamada Diária e Controle de Frequência")
            with st.form("form_chamada"):
                lista_presenca = {}
                for aluno in alunos_turma:
                    lista_presenca[aluno['id']] = st.checkbox(f"{aluno['foto']} {aluno['nome']}", value=True)
                
                if st.form_submit_button("✅ Registrar Chamada de Hoje"):
                    for aluno in st.session_state.alunos_db:
                        if aluno['id'] in lista_presenca:
                            if lista_presenca[aluno['id']]:
                                aluno['faltas_consecutivas'] = 0
                            else:
                                aluno['faltas_consecutivas'] += 1
                    salvar_dados("alunos")
                    st.success("Frequência registrada com sucesso!")
                    st.rerun()

        elif menu_professor == "📅 Planejamento BNCC":
            st.header("Planejamento Pedagógico Quinzenal")
            with st.form("form_regular", clear_on_submit=True):
                mes = st.selectbox("Mês", ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"])
                quinzena = st.radio("Quinzena", ["1ª Quinzena", "2ª Quinzena"], horizontal=True)
                campos_experiencia = st.multiselect("Campos de Experiência (BNCC)", ["O eu, o outro e o nós", "Corpo, gestos e movimentos", "Traços, sons, cores e formas", "Escuta, fala, pensamento e imaginação", "Espaços, tempos, quantidades, relações e transformações"])
                atividades = st.text_area("Descrição das Vivências e Brincadeiras:")
                if st.form_submit_button("💾 Salvar Planejamento"):
                    salvar_dados("plan", {"professor": usuario['nome'], "tipo": "Regular", "mes": mes, "quinzena": quinzena, "atividades": atividades, "campos": campos_experiencia})
                    st.success("Planejamento salvo com sucesso!")

        elif menu_professor == "👶 Ocorrências da Rotina":
            st.header("🚨 Livro de Ocorrências Diárias")
            with st.form("form_ocorrencia", clear_on_submit=True):
                aluno_ocorrencia = st.selectbox("Criança envolvida:", [a['nome'] for a in alunos_turma])
                tipo_ocorrencia = st.selectbox("Tipo de Evento:", ["Mordida/Arranhão", "Queda/Escoriação", "Febre/Sintomas de Saúde", "Indisposição Alimentar", "Outros"])
                gravidade = st.select_slider("Classificação de Gravidade:", options=["Leve", "Média", "Alta"])
                detalhes = st.text_area("Descrição detalhada:")
                if st.form_submit_button("💾 Registrar Ocorrência"):
                    salvar_dados("ocorrencias", {"professor": usuario['nome'], "aluno": aluno_ocorrencia, "tipo": tipo_ocorrencia, "gravidade": gravidade, "detalhes": detalhes})
                    st.success("Ocorrência registrada no sistema!")

        elif menu_professor == "📊 Relatório Descritivo":
            st.header("📝 Relatório Descritivo de Desenvolvimento")
            aluno_sel = st.selectbox("Selecione a Criança para Parecer:", [a['nome'] for a in alunos_turma])
            with st.form("form_relatorio", clear_on_submit=True):
                socializacao = st.text_area("Aspectos Sociais e Interação:")
                cognitivo = st.text_area("Desenvolvimento Motor e Linguagem:")
                if st.form_submit_button("💾 Salvar Parecer Pedagógico"):
                    st.success(f"Relatório de parecer descritivo de {aluno_sel} arquivado!")

        elif menu_professor == "📋 Atas & Conselhos":
            st.header("Ata de Conselho de Classe")
            with st.form("form_ata", clear_on_submit=True):
                trimestre = st.selectbox("Trimestre de Avaliação", ["1º Trimestre", "2º Trimestre", "3º Trimestre"])
                deliberacoes = st.text_area("Parecer Coletivo da Turma:")
                if st.form_submit_button("📝 Registrar e Gerar Folha"):
                    salvar_dados("atas", {"trimestre": trimestre, "turma": usuario['turma'], "conteudo": deliberacoes, "emissor": usuario['nome']})
                    st.success("Ata oficial gravada!")
                    st.rerun()

            if st.session_state.atas_salvas:
                st.divider()
                ultima_ata = st.session_state.atas_salvas[-1]
                
                # Substituído markdown com aspas triplas por st.html para eliminar o SyntaxError definitivamente
                # Bloco final da Ata de Conselho
                st.html("<div style='border: 2px solid #333; padding: 25px; background-color: #fff; color: #111; font-family: monospace; margin-bottom: 20px;'><h4 style='text-align: center;'>ATA OFICIAL DE CONSELHO</h4></div>")
                st.write(f"Trimestre: {ultima_ata['trimestre'].upper()} | Turma: {ultima_ata['turma'].upper()}")
                st.info(ultima_ata['conteudo'])
                st.write("Assinaturas Interativas:")
                for p_id, p_info in st.session_state.professores_db.items():
                    if p_info['cargo'] == "Professor Regular":
                        st.write(f"✍️ {p_info['nome'].upper()} ________________________")

    # =====================================================================
    # PERFIL: PROFESSOR AEE
    # =====================================================================
    elif usuario['cargo'] == "Professor AEE":
        st.header("🧩 Planejamento Individualizado por Aluno (AEE)")
        with st.form("form_aee", clear_on_submit=True):
            aluno_aee = st.selectbox("Criança Atendida:", [a['nome'] for a in st.session_state.alunos_db])
            objetivos = st.text_area("Objetivos de Flexibilização Curricular:")
            recursos = st.text_area("Recursos Pedagógicos Utilizados:")
            if st.form_submit_button("💾 Salvar Planejamento AEE"):
                st.success("Planejamento AEE gravado com sucesso!")

    # =====================================================================
    # PERFIL: ADMINISTRADOR
    # =====================================================================
    elif usuario['cargo'] == "Administrador":
        st.header("⚙️ Painel de Controle da Direção e Coordenação")
        st.subheader("🚨 Central de Alertas Críticos (Faltas Consecutivas)")
        alertas_ativos = False
        for aluno in st.session_state.alunos_db:
            if aluno['faltas_consecutivas'] >= 3:
                alertas_ativos = True
                st.error(f"⚠️ ALERTA: A criança {aluno['nome']} ({aluno['turma']}) acumulou {aluno['faltas_consecutivas']} faltas seguidas. Contato: {aluno['contato']}")
        if not alertas_ativos:
            st.success("✅ Nenhuma evasão ou abandono de vaga detectado.")
            
        st.divider()
        maba1, maba2, maba3 = st.tabs(["👥 Gerenciar Professores", "👶 Gerenciar Alunos", "📋 Histórico de Ocorrências"])
        
        with maba1:
            st.subheader("Gerenciamento de Funcionários")
            acao_p = st.radio("Operação (Professores):", ["Cadastrar Novo", "Editar Perfil", "Excluir Registro"], horizontal=True)
            
            if acao_p == "Cadastrar Novo":
                with st.form("add_prof", clear_on_submit=True):
                    mat_n = st.text_input("Nova Matrícula (Código de Acesso):")
                    nome_p = st.text_input("Nome Completo:")
                    cargo_p = st.selectbox("Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"])
                    turma_p = st.selectbox("Turma Atribuída:", ["Berçário I", "Berçário II", "Maternal I", "Maternal II - 1", "Maternal II - 2", "1ª Etapa -1"," 1ª Etapa - 2", "2ª Etapa - 1","2ª Etapa - 2", "Geral"])
                    if st.form_submit_button("➕ Salvar Funcionário"):
                        if mat_n and nome_p:
                            st.session_state.professores_db[mat_n] = {"nome": nome_p, "cargo": cargo_p, "turma": turma_p}
                            salvar_dados("db")
                            st.success(f"{nome_p} cadastrado!")
                            st.rerun()
                            
            elif acao_p == "Editar Perfil":
                p_sel = st.selectbox("Selecione para Editar:", list(st.session_state.professores_db.keys()), format_func=lambda x: f"{st.session_state.professores_db[x]['nome']} ({x})")
                with st.form("edit_prof"):
                    nome_e = st.text_input("Alterar Nome:", value=st.session_state.professores_db[p_sel]['nome'])
                    cargo_e = st.selectbox("Alterar Cargo:", ["Professor Regular", "Professor AEE", "Monitor", "Administrador"], index=["Professor Regular", "Professor AEE", "Monitor", "Administrador"].index(st.session_state.professores_db[p_sel]['cargo']))
                    turma_e = st.selectbox("Alterar Turma:", ["Berçário I", "Berçário II", "Maternal I", "Maternal II - 1", "Maternal II - 2", "1ª Etapa -1"," 1ª Etapa - 2", "2ª Etapa - 1","2ª Etapa - 2", "Geral", "Inclusão Geral", "Plantão"], value=st.session_state.professores_db[p_sel]['turma'])
                    if st.form_submit_button("💾 Atualizar Dados"):
                        st.session_state.professores_db[p_sel] = {"nome": nome_e, "cargo": cargo_e, "turma": turma_e}
                        salvar_dados("db")
                        st.success("Dados atualizados!")
                        st.rerun()
                        
            elif acao_p == "Excluir Registro":
                p_del = st.selectbox("Selecione para Deletar:", list(st.session_state.professores_db.keys()), format_func=lambda x: f"{st.session_state.professores_db[x]['nome']} ({x})")
                if st.button("❌ Confirmar Exclusão Definitiva"):
                    if p_del == matricula:
                        st.error("Você não pode excluir a sua própria conta ativa.")
                    else:
                        del st.session_state.professores_db[p_del]
                        salvar_dados("db")
                        st.success("Funcionário removido com sucesso!")
                        st.rerun()
                        
        with maba2:
            st.subheader("Gerenciamento do Carômetro de Alunos")
            acao_a = st.radio("Operação (Alunos):", ["Cadastrar Novo Aluno", "Editar Ficha de Saúde", "Excluir Aluno"], horizontal=True)
            
            if acao_a == "Cadastrar Novo Aluno":
                with st.form("add_aluno", clear_on_submit=True):
                    nome_n = st.text_input("Nome Completo do Aluno:")
                    turma_n = st.selectbox("Turma Escolar:", ["Berçário I", "Berçário II", "Maternal I", "Maternal II - 1", "Maternal II - 2", "1ª Etapa -1"," 1ª Etapa - 2", "2ª Etapa - 1","2ª Etapa - 2", "Geral"])
                    alergias_n = st.text_input("Alergias:", value="Nenhuma")
                    rest_n = st.text_input("Restrições Alimentares:", value="Nenhuma")
                    retirada_n = st.text_input("Autorizados para Retirada:")
                    contato_n = st.text_input("Contatos de Emergência:")
                    if st.form_submit_button("➕ Registrar Criança"):
                        if nome_n:
                            novo_a = {"id": str(len(st.session_state.alunos_db)+1), "nome": nome_n, "turma": turma_n, "alergias": alergias_n, "restricoes": rest_n, "retirada": retirada_n, "contato": contato_n, "foto": "👶", "faltas_consecutivas": 0}
                            st.session_state.alunos_db.append(novo_a)
                            salvar_dados("alunos")
                            st.success(f"{nome_n} adicionado ao Carômetro!")
                            st.rerun()
                            
            elif acao_a == "Editar Ficha de Saúde":
                a_sel_idx = st.selectbox("Selecione a Criança:", range(len(st.session_state.alunos_db)), format_func=lambda x: st.session_state.alunos_db[x]['nome'])
                aluno_e = st.session_state.alunos_db[a_sel_idx]
                with st.form("edit_aluno"):
                    nome_ae = st.text_input("Nome:", value=aluno_e['nome'])
                    turma_ae = st.selectbox("Turma:", ["Berçário I", "Berçário II", "Maternal I", "Maternal II - 1", "Maternal II - 2", "1ª Etapa -1"," 1ª Etapa - 2", "2ª Etapa - 1","2ª Etapa - 2", "Geral"].index(aluno_e['turma']))
                    alergias_ae = st.text_input("Alergias:", value=aluno_e['alergias'])
                    rest_ae = st.text_input("Restrições:", value=aluno_e['restricoes'])
                    retirada_ae = st.text_input("Retirada:", value=aluno_e['retirada'])
                    contato_ae = st.text_input("Contatos:", value=aluno_e['contato'])
                    if st.form_submit_button("💾 Salvar Alterações na Ficha"):
                        st.session_state.alunos_db[a_sel_idx] = {"id": aluno_e['id'], "nome": nome_ae, "turma": turma_ae, "alergias": alergias_ae, "restricoes": rest_ae, "retirada": retirada_ae, "contato": contato_ae, "foto": aluno_e['foto'], "faltas_consecutivas": aluno_e['faltas_consecutivas']}
                        salvar_dados("alunos")
                        st.success("Ficha updated!")
                        st.rerun()
                        
            elif acao_a == "Excluir Aluno":
                a_del_idx = st.selectbox("Selecione o Aluno para Remover:", range(len(st.session_state.alunos_db)), format_func=lambda x: f"{st.session_state.alunos_db[x]['nome']} ({st.session_state.alunos_db[x]['turma']})")
                if st.button("❌ Confirmar Exclusão do Aluno"):
                    nome_removido = st.session_state.alunos_db[a_del_idx]['nome']
                    st.session_state.alunos_db.pop(a_del_idx)
                    salvar_dados("alunos")
                    st.success(f"{nome_removido} removido do sistema!")
                    st.rerun()
                    
        with maba3:
            st.subheader("📋 Histórico Recente de Ocorrências")
            if st.session_state.get('ocorrencias_salvas'):
                for oc in reversed(st.session_state.ocorrencias_salvas):
                    with st.expander(f"📌 {oc['tipo']} - {oc['aluno']}"):
                        st.write(f"Relator: {oc['professor']} | Gravidade: {oc['gravidade']}")
                        st.info(f"Detalhes: {oc['detalhes']}")
            else: 
                st.write("Nenhuma ocorrência registrada.")
else:
    st.title("🧸 Portal de Gestão da Educação Infantil")
    st.info("Insira seu código de acesso ou matrícula na barra lateral esquerda para prosseguir.")

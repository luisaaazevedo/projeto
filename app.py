import streamlit as st
import os

def lu(caminho='usuarios.txt'):
    if not os.path.exists(caminho):
        return[]
    with open(caminho, 'r', encoding='utf-8') as f:
        return [linha.strip() for linha in f if linha.strip()]

def salvartarefa(usuario, descricao, prioridade, caminho='tarefas.txt'):
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(f"{usuario}|{descricao}|{prioridade}\n")

def lt(caminho='tarefas.txt'):
    if not os.path.exists(caminho):
        return()
    tarefas = []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            partes = linha.strip().split('|')
            if len(partes) >= 3:
                usuario, descricao, prioridade = partes[:3]
                tarefas.append({
                    'usuario': usuario,
                    'descricao': descricao,
                    'prioridade': prioridade
                })
    return tarefas

def stc(tarefa, caminho="tarefas_concluidas.txt"):
    with open(caminho, 'a', encoding='utf-8') as f:
        f.write(f"{tarefa['usuario']}|{tarefa['descricao']}|{tarefa['prioridade']}\n")

def remover(tarefa_para_remover, caminho ='tarefas.txt'):
    tarefas = lt(caminho)
    tarefas_restantes = [
        t for t in tarefas if not(
            t['usuario'] == tarefa_para_remover['usuario'] and
            t['descricao'] == tarefa_para_remover['descricao'] and
            t['prioridade'] == tarefa_para_remover['prioridade'] 
        )
    ]
    with open(caminho, 'w', encoding='utf-8' ) as f:
        for t in tarefas_restantes:
            f.write(f"{t['usuario']}|{t['descricao']}|{t['prioridade']}\n")
def fil(usuario, tarefas):
    return [t for t in tarefas if t['usuario'] == usuario]

def ler(caminho='tarefas_concluidas.txt'):
    if not os.path.exists(caminho):
        return []
    tarefas = []
    with open(caminho, 'r', encoding='utf-8') as f:
        for linha in f:
            partes = linha.strip().split('|')
            if len(partes) >= 3:
                usuario, descricao, prioridade = partes[:3]
                tarefas.append({
                    'usuario': usuario,
                    'descricao': descricao,
                    'prioridade': prioridade
                })
    return tarefas

st.set_page_config(page_title="Sistema de tarefas", layout="centered")
st.sidebar.title("Menu")
opcao = st.sidebar.radio("Escolha uma opção",[
    "Cadastrar tarefa",
    "Visualizar tarefas",
    "Tarefas concluídas"
])

usuarios = lu()

if not usuarios:
    st.warning("nenhum usuário encontrado em 'usuarios.txt'. Adicione no arquivo!")
else:
    if opcao == "Cadastrar tarefa":
        st.title("Cadastrar nova tarefa")
        usuario = st.selectbox("Usuário", usuarios)
        descricao = st.text_area("Descrição da tarefa")
        prioridade = st.selectbox("prioridade", ["Alta", "Média", "Baixa"] )
        
        if st.button("Salvar tarefa"):
            if descricao.strip():
                salvartarefa(usuario, descricao.strip(), prioridade)
                st.success("tarefa salva com sucesso!!")
            else:
                st.warning("A descrição esta vazia!!")
    elif opcao == "Visualizar tarefas":
        st.title("Visualizar tarefas")
        usse = st.selectbox("Selecione o usuário", usuarios)
        tarefas = fil(usse, lt())

        prioridade = ["Alta", "Média", "Baixa"]
        for p in prioridade:
            st.subheader(f"Tarefas com prioridade {p}")
            ttf = [t for t in tarefas if t ['prioridade'] == p]
            if ttf:
                for i, t in enumerate(ttf):
                    col1, col2 = st.columns([0.90, 0.20])
                    with col1:
                        st.write(f"-{t['descricao']}")
                    with col2:
                        if st.button("CONCLUIR", key=f"{p}_{i}"):
                            st.experimental_rerun()
                            
            else:
               st.write("Nenhuma Tarefa com essa prioridade.")

        st.markdown("----")
        if st.button("Limpar todas as tarefas"):
            tarefas_restantes = [t for t in lt() if t['usuario'] != usse]
            with open('tarefas.txt', 'w', encoding='utf-8') as f:
                for t in tarefas_restantes:
                    f.write(f"{t['usuario']}|{t['descricao']}|{t['prioridade']}\n")
            st.success("todas as tarefas do usuario foram removidas.")
            st.experimental_rerun()

    elif opcao == "Tarefas concluídas":
        st.title("Tarefas concluídas")
        usse = st.selectbox("Selecione o usuário", usuarios)
        concluidas = fil(usse, ler())   
         
        if concluidas:
            for p in ['Alta', 'Média', "Baixa"]:
                st.subheader(f"Tarefa com prioridades {p}")
                for t in [x for x in concluidas if x['prioridade'] == p]:
                    st.write(f"-{t['descricao']}")
        else:
            st.info("nenhuma tarefa concluida para este usuário.")


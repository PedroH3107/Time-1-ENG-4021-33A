import re
from datetime import date, timedelta

import app as aplicacao
from conftest import buscar, entrar
from match import calcular_compatibilidade


def texto(resposta):
    return resposta.get_data(as_text=True)


def id_proposta(nome_artistico):
    linha = buscar(
        "SELECT pr.id FROM propostas pr JOIN artistas a ON a.id = pr.artista_id "
        "WHERE a.nome_artistico = %s", (nome_artistico,)
    )
    return str(linha["id"])


def id_contrato(username, nome_artistico):
    linha = buscar(
        "SELECT c.id FROM contratos c JOIN profiles p ON p.id = c.cliente_id "
        "JOIN artistas a ON a.id = c.artista_id WHERE p.username = %s AND a.nome_artistico = %s",
        (username, nome_artistico),
    )
    return str(linha["id"])


def id_pedido(username):
    linha = buscar(
        "SELECT po.id FROM pedidos_orcamento po JOIN eventos e ON e.id = po.evento_id "
        "JOIN profiles p ON p.id = e.cliente_id WHERE p.username = %s", (username,)
    )
    return str(linha["id"])


# ---------------------------------------------------------------
# Rotas que já existiam
# ---------------------------------------------------------------
def test_home_lista_artistas(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == 200
    assert "Selva Ritmo" in texto(resposta)


def test_perfil_do_artista(cliente):
    artista = buscar("SELECT id FROM artistas WHERE nome_artistico = 'Coletivo Maré'")
    resposta = cliente.get("/artistas/" + str(artista["id"]))
    assert resposta.status_code == 200
    assert "Coletivo Maré" in texto(resposta)


def test_artista_com_id_invalido_nao_da_erro_500(cliente):
    resposta = cliente.get("/artistas/nao-e-um-id", follow_redirects=True)
    assert resposta.status_code == 200
    assert "Artista não encontrado" in texto(resposta)


def test_painel_exige_login(cliente):
    resposta = cliente.get("/painel")
    assert resposta.status_code == 302
    assert "/login" in resposta.headers["Location"]


def test_login_com_senha_errada(cliente):
    resposta = cliente.post("/login", data={"username": "luiz", "password": "errada"})
    assert resposta.status_code == 401


def test_login_leva_cada_papel_ao_seu_painel(cliente):
    assert entrar(cliente, "luiz").headers["Location"].endswith("/painel")
    cliente.get("/logout")
    assert entrar(cliente, "selvaritmo").headers["Location"].endswith("/artista/painel")
    cliente.get("/logout")
    assert entrar(cliente, "admin").headers["Location"].endswith("/admin")


def test_cadastro_de_cliente(cliente):
    dados = {"tipo": "contratante", "username": "maria", "nome": "Maria Lima", "email": "maria@x.com",
             "cidade": "Niterói", "senha": "12345678", "confirmar": "12345678", "termos": "on"}
    resposta = cliente.post("/cadastro", data=dados)
    assert resposta.status_code == 302
    assert buscar("SELECT papel FROM profiles WHERE username = 'maria'")["papel"] == "cliente"


def test_cadastro_de_artista_com_preco_invalido_nao_cria_conta(cliente):
    dados = {"tipo": "artista", "username": "novo_dj", "nome": "Novo DJ", "email": "dj@x.com",
             "cidade": "Rio de Janeiro", "categoria": "3", "preco": "abc",
             "senha": "12345678", "confirmar": "12345678", "termos": "on"}
    resposta = cliente.post("/cadastro", data=dados)
    assert resposta.status_code == 400
    assert buscar("SELECT id FROM profiles WHERE username = 'novo_dj'") is None

    # corrigindo o preço, o mesmo usuário consegue se cadastrar
    dados["preco"] = "1500"
    resposta = cliente.post("/cadastro", data=dados)
    assert resposta.status_code == 302
    artista = buscar("SELECT a.preco_minimo FROM artistas a JOIN profiles p ON p.id = a.user_id "
                     "WHERE p.username = 'novo_dj'")
    assert float(artista["preco_minimo"]) == 1500


def test_cadastro_duplicado(cliente):
    dados = {"tipo": "contratante", "username": "luiz", "nome": "Outro Luiz", "email": "outro@x.com",
             "cidade": "Rio", "senha": "12345678", "confirmar": "12345678", "termos": "on"}
    resposta = cliente.post("/cadastro", data=dados)
    assert resposta.status_code == 400
    assert "já está cadastrado" in texto(resposta)


def test_pedido_de_orcamento(cliente):
    entrar(cliente, "helena")
    amanha = (date.today() + timedelta(days=30)).isoformat()
    dados = {"tipo_evento": "aniversario", "categoria": "2", "data": amanha, "horario": "18:00",
             "duracao": "2", "convidados": "40", "local": "Rua das Flores, 10"}
    resposta = cliente.post("/orcamento", data=dados)
    assert resposta.status_code == 302
    total = buscar("SELECT COUNT(*) AS n FROM pedidos_orcamento po JOIN eventos e ON e.id = po.evento_id "
                   "JOIN profiles p ON p.id = e.cliente_id WHERE p.username = 'helena'")
    assert total["n"] == 2


def test_listagem_de_usuarios_so_para_admin(cliente):
    entrar(cliente, "luiz")
    assert cliente.get("/usuarios").status_code == 302
    cliente.get("/logout")
    entrar(cliente, "admin")
    assert cliente.get("/usuarios").status_code == 200


def test_exclusao_bloqueada_com_pagamento_retido(cliente):
    entrar(cliente, "luiz")
    dados = {"password": "artconnect123", "confirm_text": "EXCLUIR", "confirm_check": "on"}
    resposta = cliente.post("/conta/excluir", data=dados)
    assert "pagamento retido" in texto(resposta)
    assert buscar("SELECT id FROM profiles WHERE username = 'luiz'") is not None


# ---------------------------------------------------------------
# Match de compatibilidade
# ---------------------------------------------------------------
def test_regras_de_pontuacao():
    artista = {"preco_minimo": 1800, "cidade": "Rio de Janeiro", "nota_media": 4.0}
    # todos os critérios: 35 (preço) + 25 (cidade) + 25 (livre) + 12 (nota 4) = 97 de 100
    assert calcular_compatibilidade(artista, "Rio de Janeiro", 2000, True, False) == 97
    # 20% acima do orçamento vale 15; ocupado na data vale 0: 15 + 25 + 0 + 12 = 52
    assert calcular_compatibilidade(artista, "rio de janeiro", 1600, True, True) == 52
    # sem avaliação conta metade da nota (7,5 de 15): só nota informada = 50%
    novo = {"preco_minimo": 500, "cidade": "Recife", "nota_media": None}
    assert calcular_compatibilidade(novo, "", None, False, False) == 50


def test_busca_ordena_por_compatibilidade(cliente):
    resposta = cliente.get("/?cidade=Rio+de+Janeiro&orcamento=2000")
    pagina = texto(resposta)
    assert "Mais compatíveis com seu evento" in pagina
    porcentagens = re.findall(r"(\d+)% compatível", pagina)
    numeros = []
    for valor in porcentagens:
        numeros.append(int(valor))
    assert len(numeros) == 11
    assert numeros == sorted(numeros, reverse=True)
    # o primeiro resultado é do Rio e cabe no orçamento
    assert pagina.index("Coletivo Maré") < pagina.index("Chef Raiz")


def test_busca_marca_artista_ocupado_na_data(cliente):
    resposta = cliente.get("/?categoria=3&data=2026-12-05")
    pagina = texto(resposta)
    assert "ocupado na data" in pagina
    assert pagina.index("Neon Sombra") < pagina.index("Selva Ritmo")


def test_busca_com_orcamento_invalido(cliente):
    resposta = cliente.get("/?orcamento=muito")
    assert resposta.status_code == 200
    assert "só com números" in texto(resposta)


# ---------------------------------------------------------------
# Agenda (tabela disponibilidade)
# ---------------------------------------------------------------
def test_artista_marca_e_remove_data(cliente):
    entrar(cliente, "coletivomare")
    data = (date.today() + timedelta(days=40)).isoformat()
    cliente.post("/artista/agenda", data={"data": data, "status": "ocupado", "observacao": "Turnê"})
    linha = buscar("SELECT status FROM disponibilidade d JOIN artistas a ON a.id = d.artista_id "
                   "WHERE a.nome_artistico = 'Coletivo Maré' AND d.data = %s", (data,))
    assert linha["status"] == "ocupado"

    cliente.post("/artista/agenda", data={"data": data, "acao": "remover"})
    linha = buscar("SELECT 1 FROM disponibilidade d JOIN artistas a ON a.id = d.artista_id "
                   "WHERE a.nome_artistico = 'Coletivo Maré' AND d.data = %s", (data,))
    assert linha is None


def test_agenda_nao_aceita_data_passada(cliente):
    entrar(cliente, "coletivomare")
    resposta = cliente.post("/artista/agenda", data={"data": "2020-01-01", "status": "ocupado"},
                            follow_redirects=True)
    assert "a partir de hoje" in texto(resposta)


# ---------------------------------------------------------------
# Painel do artista: aceite, recusa e contraproposta
# ---------------------------------------------------------------
def test_cliente_nao_acessa_painel_do_artista(cliente):
    entrar(cliente, "luiz")
    assert cliente.get("/artista/painel").status_code == 302


def test_painel_do_artista_mostra_pedidos_da_categoria(cliente):
    entrar(cliente, "selvaritmo")
    pagina = texto(cliente.get("/artista/painel"))
    assert "Rooftop Centro" in pagina              # pedido de DJ do rafael
    assert "Salão Vila Madalena" not in pagina     # pedido de cantor, outra categoria
    assert "Casa de Festas Lagoa" not in pagina    # pedido que ele já respondeu
    assert "agenda está marcada como ocupada" in pagina


def test_artista_envia_proposta(cliente):
    entrar(cliente, "neonsombra")
    resposta = cliente.post("/artista/pedidos/" + id_pedido("rafael") + "/responder",
                            data={"acao": "proposta", "valor": "3300", "mensagem": "Set de 5h"})
    assert resposta.status_code == 302
    pedido = buscar("SELECT status FROM pedidos_orcamento WHERE id = %s", (id_pedido("rafael"),))
    assert pedido["status"] == "com_propostas"


def test_proposta_bloqueada_quando_agenda_ocupada_e_contraproposta_liberada(cliente):
    entrar(cliente, "selvaritmo")
    url = "/artista/pedidos/" + id_pedido("rafael") + "/responder"
    resposta = cliente.post(url, data={"acao": "proposta", "valor": "2500"}, follow_redirects=True)
    assert "Envie uma contraproposta" in texto(resposta)

    cliente.post(url, data={"acao": "contraproposta", "valor": "2500", "data_sugerida": "2026-12-06"})
    proposta = buscar("SELECT data_sugerida FROM propostas WHERE pedido_id = %s", (id_pedido("rafael"),))
    assert proposta["data_sugerida"] == date(2026, 12, 6)


def test_artista_recusa_pedido(cliente):
    entrar(cliente, "neonsombra")
    cliente.post("/artista/pedidos/" + id_pedido("rafael") + "/responder", data={"acao": "recusar"})
    proposta = buscar("SELECT status FROM propostas WHERE pedido_id = %s", (id_pedido("rafael"),))
    assert proposta["status"] == "declinada"
    assert "Rooftop Centro" not in texto(cliente.get("/artista/painel"))


def test_artista_nao_responde_duas_vezes(cliente):
    entrar(cliente, "neonsombra")
    url = "/artista/pedidos/" + id_pedido("rafael") + "/responder"
    cliente.post(url, data={"acao": "recusar"})
    resposta = cliente.post(url, data={"acao": "proposta", "valor": "100"}, follow_redirects=True)
    assert "já respondeu" in texto(resposta)


def test_cliente_aceita_proposta_e_gera_contrato(cliente):
    entrar(cliente, "luiz")
    resposta = cliente.post("/propostas/" + id_proposta("Selva Ritmo") + "/aceitar")
    assert resposta.status_code == 302

    contrato = buscar("SELECT c.valor_total, c.data_evento, pg.status FROM contratos c "
                      "JOIN pagamentos pg ON pg.contrato_id = c.id WHERE c.proposta_id = %s",
                      (id_proposta("Selva Ritmo"),))
    assert float(contrato["valor_total"]) == 2800
    assert contrato["status"] == "pendente"
    assert buscar("SELECT status FROM propostas WHERE id = %s", (id_proposta("Neon Sombra"),))["status"] == "recusada"
    assert buscar("SELECT status FROM pedidos_orcamento WHERE id = %s", (id_pedido("luiz"),))["status"] == "fechado"
    agenda = buscar("SELECT d.status FROM disponibilidade d JOIN artistas a ON a.id = d.artista_id "
                    "WHERE a.nome_artistico = 'Selva Ritmo' AND d.data = %s", (contrato["data_evento"],))
    assert agenda["status"] == "ocupado"


def test_aceitar_contraproposta_usa_a_data_sugerida(cliente):
    entrar(cliente, "luiz")
    cliente.post("/propostas/" + id_proposta("Neon Sombra") + "/aceitar")
    contrato = buscar("SELECT data_evento FROM contratos WHERE proposta_id = %s", (id_proposta("Neon Sombra"),))
    assert contrato["data_evento"] == date(2026, 12, 13)


def test_cliente_nao_aceita_proposta_de_outra_pessoa(cliente):
    entrar(cliente, "helena")
    resposta = cliente.post("/propostas/" + id_proposta("Selva Ritmo") + "/aceitar", follow_redirects=True)
    assert "Proposta não encontrada" in texto(resposta)
    assert buscar("SELECT status FROM propostas WHERE id = %s", (id_proposta("Selva Ritmo"),))["status"] == "enviada"


# ---------------------------------------------------------------
# Confirmação do evento e avaliação
# ---------------------------------------------------------------
def test_confirmar_evento_libera_pagamento(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Selva Ritmo")
    cliente.post("/contratos/" + contrato + "/confirmar")
    linha = buscar("SELECT c.status, pg.status AS pagamento FROM contratos c "
                   "JOIN pagamentos pg ON pg.contrato_id = c.id WHERE c.id = %s", (contrato,))
    assert linha["status"] == "concluido"
    assert linha["pagamento"] == "liberado"


def test_nao_confirma_evento_futuro(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Neon Sombra")
    resposta = cliente.post("/contratos/" + contrato + "/confirmar", follow_redirects=True)
    assert "depois da data do evento" in texto(resposta)


def test_avaliar_contrato_concluido_atualiza_nota(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Estúdio Lume")
    resposta = cliente.post("/contratos/" + contrato + "/avaliar",
                            data={"nota": "4", "comentario": "Fotos lindas, entregaram em uma semana."})
    assert resposta.status_code == 302
    artista = buscar("SELECT nota_media, total_avaliacoes FROM vw_artistas WHERE nome_artistico = 'Estúdio Lume'")
    assert float(artista["nota_media"]) == 4.0
    assert artista["total_avaliacoes"] == 1


def test_nao_avalia_duas_vezes(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Estúdio Lume")
    cliente.post("/contratos/" + contrato + "/avaliar", data={"nota": "5"})
    resposta = cliente.post("/contratos/" + contrato + "/avaliar", data={"nota": "1"}, follow_redirects=True)
    assert "já avaliou" in texto(resposta)


def test_nao_avalia_evento_nao_concluido(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Neon Sombra")
    resposta = cliente.get("/contratos/" + contrato + "/avaliar", follow_redirects=True)
    assert "depois que o evento for concluído" in texto(resposta)


def test_nota_fora_do_intervalo(cliente):
    entrar(cliente, "luiz")
    contrato = id_contrato("luiz", "Estúdio Lume")
    resposta = cliente.post("/contratos/" + contrato + "/avaliar", data={"nota": "9"})
    assert resposta.status_code == 400


# ---------------------------------------------------------------
# Recuperação de senha
# ---------------------------------------------------------------
def test_recuperacao_de_senha_completa(cliente, monkeypatch):
    enviados = []

    def falso_enviar(destinatario, assunto, corpo):
        enviados.append(corpo)

    monkeypatch.setattr(aplicacao, "enviar_email", falso_enviar)
    cliente.post("/senha/esqueci", data={"email": "luiz@exemplo.com"})
    assert len(enviados) == 1
    caminho = re.search(r"/senha/redefinir/\S+", enviados[0]).group(0)

    assert cliente.get(caminho).status_code == 200
    cliente.post(caminho, data={"senha": "novasenha99", "confirmar": "novasenha99"})
    resposta = cliente.post("/login", data={"username": "luiz", "password": "novasenha99"})
    assert resposta.status_code == 302

    # o link não pode ser usado de novo
    resposta = cliente.get(caminho, follow_redirects=True)
    assert "inválido ou expirado" in texto(resposta)


def test_email_desconhecido_recebe_a_mesma_mensagem(cliente, monkeypatch):
    enviados = []
    monkeypatch.setattr(aplicacao, "enviar_email", lambda d, a, c: enviados.append(c))
    resposta = cliente.post("/senha/esqueci", data={"email": "ninguem@x.com"}, follow_redirects=True)
    assert "Se esse e-mail estiver cadastrado" in texto(resposta)
    assert len(enviados) == 0


def test_token_expirado_nao_funciona(cliente):
    usuario = buscar("SELECT id FROM profiles WHERE username = 'luiz'")
    aplicacao.db.executar(
        "INSERT INTO tokens_senha (user_id, token_hash, expira_em) VALUES (%s, %s, now() - INTERVAL '1 minute')",
        (usuario["id"], aplicacao.hash_token("token-velho")),
    )
    resposta = cliente.get("/senha/redefinir/token-velho", follow_redirects=True)
    assert "inválido ou expirado" in texto(resposta)


# ---------------------------------------------------------------
# Dashboard administrativo
# ---------------------------------------------------------------
def test_dashboard_admin(cliente):
    entrar(cliente, "admin")
    resposta = cliente.get("/admin")
    pagina = texto(resposta)
    assert resposta.status_code == 200
    assert "Dashboard da plataforma" in pagina
    assert "Demanda por categoria" in pagina
    assert "Risada Tardia" in pagina


def test_dashboard_bloqueado_para_cliente(cliente):
    entrar(cliente, "luiz")
    assert cliente.get("/admin").status_code == 302

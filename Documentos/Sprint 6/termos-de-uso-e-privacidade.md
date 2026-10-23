# Termos de uso e política de privacidade (LGPD)

Versão 1.0 · outubro de 2026 · ArtConnect, projeto acadêmico da disciplina ENG4021 da PUC-Rio.

## Parte 1 · Termos de uso

### 1. O que é o ArtConnect

O ArtConnect é uma plataforma que conecta pessoas e empresas que organizam eventos ("clientes") a artistas e prestadores de serviços culturais ("artistas"). O ArtConnect intermedeia o contato, o orçamento e o pagamento, mas não é o prestador do serviço contratado.

### 2. Cadastro

- É preciso ter 18 anos ou mais para criar uma conta.
- Os dados informados precisam ser verdadeiros e atualizados.
- O usuário é responsável por manter a senha em segredo. Em caso de suspeita de uso indevido, ele deve trocar a senha pela opção "Esqueci a senha".
- Cada pessoa pode ter uma conta de cliente e uma de artista, sem contas falsas ou duplicadas.

### 3. Regras para clientes

- Descrever o evento com honestidade no pedido de orçamento (data, local, número de convidados).
- Pagar pelos meios da plataforma. Pagamentos combinados por fora não têm a proteção do valor retido.
- Confirmar no painel que o evento aconteceu, ou contestar em até 48 horas após a data do evento.

### 4. Regras para artistas

- Manter a agenda atualizada e só enviar propostas para datas em que pode comparecer.
- Cumprir o que foi combinado na proposta aceita (horário, duração, estrutura).
- Não pedir ao cliente que pague fora da plataforma.

### 5. Pagamento retido

O valor pago pelo cliente fica retido pela plataforma e só é liberado ao artista depois que o cliente confirma a realização do evento, ou 48 horas após a data do evento sem contestação. Cancelamentos e reembolsos seguem a Política de Cancelamento e Reembolso.

### 6. Avaliações

- Só quem contratou e teve o evento concluído pode avaliar, uma única vez por contrato.
- As avaliações devem ser honestas e respeitosas. Ofensas, dados pessoais de terceiros e conteúdo discriminatório podem ser removidos.
- Artistas não podem oferecer vantagens em troca de notas.

### 7. Condutas proibidas

Usar a plataforma para fraude, assédio, discriminação, divulgação de conteúdo ilegal, coleta de dados de outros usuários ou para tentar burlar a segurança do sistema. O descumprimento pode levar à suspensão ou exclusão da conta.

### 8. Limitação de responsabilidade

O ArtConnect se esforça para manter o serviço disponível e os perfis confiáveis, mas não garante o resultado artístico do serviço contratado. Problemas entre cliente e artista devem ser comunicados pela plataforma, que fará a mediação.

### 9. Alterações

Estes termos podem mudar. Mudanças importantes serão avisadas por e-mail ou no painel com pelo menos 15 dias de antecedência.

## Parte 2 · Política de privacidade

### 10. Quais dados coletamos

| Dado | Quando | Por quê |
|---|---|---|
| Nome, usuário, e-mail, telefone, cidade | No cadastro | Identificar a conta e permitir o contato entre cliente e artista |
| Senha | No cadastro | Acesso à conta. Guardamos só o hash da senha, nunca a senha em si |
| Categoria, preço "a partir de", descrição, agenda | Perfil do artista | Exibir o artista na busca e calcular a compatibilidade |
| Pedidos, propostas, contratos, mensagens | Durante o uso | Executar a contratação |
| Status dos pagamentos | Durante o uso | Controlar o valor retido e os repasses. Dados de cartão ficam com o processador de pagamento, não com o ArtConnect |
| Avaliações | Após o evento | Reputação dos artistas |
| Cookie de sessão | Ao entrar | Manter o usuário logado. Não usamos cookies de publicidade |

### 11. Bases legais (art. 7º da LGPD)

- **Execução de contrato (inciso V):** cadastro, pedidos, propostas, contratos, pagamentos e mensagens.
- **Legítimo interesse (inciso IX):** estatísticas agregadas de uso e prevenção de fraude.
- **Cumprimento de obrigação legal (inciso II):** registros que a lei exija guardar.
- **Consentimento (inciso I):** envio de novidades por e-mail, que pode ser retirado a qualquer momento.

### 12. Com quem compartilhamos

- **Entre cliente e artista:** antes do aceite, o artista vê só o primeiro nome do cliente e os dados do evento. Depois que a proposta é aceita, os dois veem o nome completo um do outro para combinar os detalhes.
- **Processador de pagamento:** só o necessário para processar a cobrança.
- **Autoridades:** quando houver ordem judicial ou obrigação legal.

Não vendemos dados pessoais.

### 13. Por quanto tempo guardamos

Enquanto a conta estiver ativa. Quando o usuário exclui a conta, os dados de perfil são apagados, e o perfil público do artista é desativado. Registros que a lei obrigue a manter são guardados pelo prazo legal, com acesso restrito.

### 14. Direitos do titular (art. 18 da LGPD)

O usuário pode, a qualquer momento:

- confirmar se tratamos seus dados e acessá-los;
- corrigir dados incompletos ou desatualizados (tela "Perfil");
- pedir a exclusão (tela "Excluir conta");
- pedir a portabilidade dos dados;
- revogar o consentimento para comunicações.

Os pedidos que não podem ser feitos pelas próprias telas devem ser enviados ao encarregado de dados.

### 15. Segurança

- Senhas guardadas com hash (werkzeug.security).
- Consultas ao banco com parâmetros, o que evita SQL injection.
- Links de recuperação de senha com token aleatório, guardado só como hash, válido por 30 minutos e de uso único.
- Acesso a dados restrito por papel: o cliente só vê os próprios pedidos, o artista só os pedidos da sua categoria, e o administrador vê as estatísticas.

### 16. Encarregado de dados (DPO)

Contato: [e-mail do grupo] · Em caso de incidente de segurança que possa causar risco aos usuários, os titulares e a ANPD serão comunicados.

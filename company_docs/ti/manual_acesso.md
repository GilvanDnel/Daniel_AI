# MANUAL DE SEGURANÇA DA INFORMAÇÃO, ACESSOS E DIRETRIZES TÉCNICAS (SOP)

## DNEL SOM SOLUÇÕES DIGITAIS

---

### ÍNDICE

1. [Propósito e Princípios Gerais](#1-propósito-e-princípios-gerais)
2. [Hierarquia e Matriz de Acessos Lógicos](#2-hierarquia-e-matriz-de-acessos-lógicos)
3. [Segurança Física das Instalações e Oficina](#3-segurança-física-das-instalações-e-oficina)
4. [Política de Senhas, Credenciais e MFA](#4-política-de-senhas-credenciais-e-mfa)
5. [Diretrizes de Governança do Agente Daniel](#5-diretrizes-de-governança-do-agente-daniel)
6. [Segurança de Redes, Wi-Fi e Acesso Remoto](#6-segurança-de-redes-wi-fi-e-acesso-remoto)
7. [Conformidade com a LGPD e Proteção de Dados](#7-conformidade-com-a-lgpd-e-proteção-de-dados)
8. [Planos de Contingência, Backup e Resposta a Incidentes](#8-planos-de-contingência-backup-e-resposta-a-incidentes)
9. [Responsabilidades e Termo de Compromisso](#9-responsabilidades-e-termo-de-compromisso)
10. [Anexo I – Ficha de Auditoria e Controle de Acessos](#10-anexo-i)

---

### 1. PROPÓSITO E PRINCÍPIOS GERAIS

O presente documento estabelece as diretrizes de funcionamento, segurança e governança de dados da **Dnel Som soluções digitais**. Ele atua como o manual oficial de procedimentos para garantir a integridade dos sistemas digitais, a proteção física da loja e da oficina de instalação de som, o controle rígido de credenciais e a conformidade total com a Lei Geral de Proteção de Dados (LGPD).

A nossa operação é híbrida, integrando serviços físicos de instalação de som automotivo e residencial de alto padrão a soluções digitais complexas (presets de equalização, consultoria acústica e e-commerce). A segurança e a rapidez no processamento de informações são os nossos maiores diferenciais competitivos.

#### Nossos Princípios Fundamentais:

- **Privacidade por Padrão (Privacy by Design):** Toda nova ferramenta ou processo de faturamento e suporte já deve nascer adaptado às restrições da LGPD.
- **Princípio do Menor Privilégio:** Cada colaborador terá acesso exclusivamente aos sistemas e pastas necessários para o cumprimento de suas tarefas diárias.
- **Rastreabilidade Operacional:** Toda alteração de sistema, exclusão de dados ou movimentação financeira deve deixar logs claros e auditáveis.
- **Sinergia Humano-Cognitiva:** O **Agente Daniel** é o assistente virtual de inteligência artificial da empresa, projetado para auxiliar clientes e operadores de forma segura, sem nunca ultrapassar os limites de autonomia definidos pela diretoria.

---

### 2. HIERARQUIA E MATRIZ DE ACESSOS LÓGICOS

Para evitar sobreposição de comandos, vazamento de credenciais e uso inadequado de privilégios de sistema, fica estabelecida a seguinte matriz de níveis de acesso para os colaboradores da **Dnel Som soluções digitais**:

| Nível  | Cargo / Função                        | Sistemas Habilitados                                                                                                                         | Escopo de Acesso de Dados                                                                                                     |
| :----: | :------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------- |
| **L1** | **Diretoria Executiva**               | ERP Geral, Gateway de Pagamento, Servidor Cloud, Banco de Dados, Painel de Afiliados, CFTV e Controle de Logs.                               | Acesso irrestrito a todas as pastas, relatórios de faturamento, faturamento bruto e dados sensíveis.                          |
| **L2** | **Administrativo / Financeiro**       | ERP (Faturamento/Contabilidade), Gateway de Pagamento (Visualização e Estorno), Painel de Afiliados (Aprovação de saques) e Suporte Técnico. | Visualização de notas fiscais, faturamento diário, dados fiscais de afiliados e histórico de conciliação.                     |
| **L3** | **Técnicos de Instalação (Físico)**   | ERP (Módulo de Ordem de Serviço/Estoque de Equipamentos de Som) e Aplicativo de Checklists.                                                  | Visualização das especificações técnicas do veículo do cliente, fiação de som e equipamentos alocados para a OS do dia.       |
| **L4** | **Suporte Digital e Vendas (Online)** | Plataforma de Atendimento, E-commerce (Checkout e Rastreamento) e Painel do Agente Daniel.                                                   | Visualização de chamados de suporte, dados cadastrais mínimos de entrega de som e interações de clientes com a IA.            |
| **L5** | **Agente Daniel (Agente Cognitivo)**  | API de Integração, Banco de Dados RAG (Somente Leitura) e Banco de Conhecimento (`company_docs`).                                            | Leitura e interpretação de políticas de garantia, tabelas de frete, guias de reembolso e catálogos para responder a chamados. |

#### Regras de Atribuição e Revogação:

1.  **Criação de Acessos:** A criação de qualquer usuário no ERP, gateway ou banco de dados exige requisição formal por escrito enviada ao setor administrativo e validação da diretoria.
2.  **Desligamento de Colaboradores:** No momento de rescisão contratual, o setor administrativo deve revogar todas as senhas, logins de e-mail corporativo, acessos ao gateway de pagamentos e chaves de servidores em até **no máximo 1 hora** após o comunicado de desligamento, emitindo o relatório de auditoria correspondente.

---

### 3. SEGURANÇA FÍSICA DAS INSTALAÇÕES E OFICINA

A proteção do patrimônio físico (alto-falantes, amplificadores de alto valor, ferramentas de calibração, automóveis de clientes na oficina) e dos servidores locais exige disciplina diária em checklists rígidos.

#### 3.1 Procedimento Padrão de Abertura (08:00h)

1.  **Desativação do Alarme:** O encarregado do turno deve desativar o alarme perimetral inserindo sua senha individual no teclado de controle em até **15 segundos** após abrir a porta de serviço lateral.
2.  **Inspeção Visual:** Verificar se há marcas de arrombamento, infiltrações ou falhas físicas na oficina e no rack de servidores locais.
3.  **Ligar Sistemas:** Ligar a iluminação da loja, os terminais de atendimento físico e colocar os computadores da oficina em operação segura.
4.  **Liberação do Pátio:** Abrir o portão principal da oficina para a entrada de veículos de clientes agendados para a instalação de som automotivo.

#### 3.2 Procedimento Padrão de Fechamento (22:00h)

1.  **Organização Geral e ESD:** Limpar todas as bancadas eletrônicas, organizar as ferramentas de som, recolher fios e sobras de cabos, e certificar-se de que os tapetes e pulseiras antiestática (ESD) estão desligados e guardados.
2.  **Fechamento Físico de Veículos:** Garantir que todos os carros de clientes que permanecerão na oficina para serviços de som de múltiplos dias estejam trancados, com as chaves guardadas no cofre de segurança interna.
3.  **Travamento de Portas:** Trancar todas as portas secundárias, janelas, portão principal da oficina e a sala de servidores/estoque físico de equipamentos de som de alto valor.
4.  **Ativação do Alarme e CFTV:** Ativar o sistema de alarme perimetral e certificar-se de que o sistema de monitoramento de câmeras (CFTV) está operando no modo noturno de alta definição, registrando em nuvem.
5.  **Registro de Ocorrências:** Anotar em livro de ocorrências digital qualquer anormalidade técnica ou de infraestrutura física identificada no fechamento.

#### 3.3 Gestão e Proteção das Câmeras (CFTV)

- **Posicionamento Estratégico:** As câmeras de monitoramento 24h devem focar de forma permanente nas seguintes áreas: Entrada Principal, Portão da Oficina, Bancadas de Instalação de Som, Caixa Físico, Sala de Servidores/Estoque de Equipamentos e Escritório Administrativo.
- **Sigilo das Imagens:** As gravações do CFTV são de uso estritamente interno e confidencial da diretoria. É proibido qualquer colaborador baixar, filmar com celular ou compartilhar trechos de gravações sem autorização judicial expressa ou determinação direta da diretoria.
- **LGPD Física:** Placas de veículos de clientes ou rostos de terceiros capturados pelas câmeras não devem ser expostos publicamente, sob pena de demissão por justa causa.

---

### 4. POLÍTICA DE SENHAS, CREDENCIAIS E MFA

O acesso a todos os ambientes digitais da **Dnel Som soluções digitais** deve seguir padrões internacionais de criptografia e segurança cibernética para neutralizar invasões, vazamentos de dados ou sequestro de sistemas (Ransomware).

#### 4.1 Padrão de Complexidade de Senhas

Toda senha de sistema (ERP, e-mail corporativo, painel de controle e servidores) deve ser redefinida obrigatoriamente a cada **90 dias** e cumprir com os seguintes requisitos mínimos:

- Mínimo de **12 caracteres** de comprimento.
- Pelo menos uma letra **maiúscula** (A-Z).
- Pelo menos uma letra **minúscula** (a-z).
- Pelo menos um caractere **numérico** (0-9).
- Pelo menos um caractere **especial** (ex: `@`, `#`, `$`, `&`, `*`).
- Proibição do uso de dados pessoais (datas de nascimento, nomes de familiares, placas de veículos) ou do nome da empresa.
- Proibição de repetir as últimas 5 senhas utilizadas anteriormente.

#### 4.2 Autenticação de Múltiplos Fatores (MFA)

O uso de **Autenticação de Duplo Fator (MFA/2FA)** é de caráter **obrigatório e inegociável** em todos os sistemas críticos que contenham dados de faturamento, transações financeiras e dados pessoais de clientes de acordo com a LGPD:

1.  **Acesso ao ERP e Checkout do E-commerce:** Exigência de MFA via aplicativo autenticador oficial (Google Authenticator ou Microsoft Authenticator).
2.  **Gateways de Pagamento (PIX, Crédito, Boletos):** Confirmação de segurança via token dinâmico adicional gerado no dispositivo móvel corporativo cadastrado da diretoria.
3.  **E-mails Corporativos:** Todo acesso fora da rede local da empresa exige validação de dispositivo via notificação push.

#### 4.3 Compartilhamento de Credenciais

- **Regra de Ouro:** Fica terminantemente **proibido o compartilhamento de credenciais (usuários e senhas)** entre colaboradores. Cada funcionário responderá individual e legalmente por qualquer ação executada sob o seu respectivo login em auditorias de logs internos.
- Se um técnico ou analista de suporte precisar realizar uma ação em nome de outro setor, a permissão deve ser concedida via alteração temporária de perfil de acesso nos termos do Nível de Acesso (Seção 2), e nunca através da divisão de senhas particulares.

---

### 5. DIRETRIZES DE GOVERNANÇA DO AGENTE DANIEL

O **Agente Daniel** é o nosso agente cognitivo integrado ao ecossistema da **Dnel Som soluções digitais**. Ele utiliza inteligência artificial avançada e processamento de linguagem natural grounded (baseado na base de conhecimento `company_docs`) para automatizar o atendimento a clientes, consultar a validade de garantias, orientar sobre prazos de reembolsos e emitir relatórios de faturamento.

Para garantir que a inteligência artificial opere com segurança operacional e jurídica, as seguintes diretrizes técnicas e éticas de acesso devem ser estritamente seguidas:

#### 5.1 Nível de Autonomia e Tomada de Decisão

- **Garantia e Pós-Venda:** O **Agente Daniel** tem autonomia para realizar triagens, validar documentos de compra enviados por clientes e classificar se um caso é elegível ou não à cobertura de garantia. No entanto, o agente **não pode aprovar ou processar estornos financeiros diretamente**. A validação financeira final e a transferência de valores de reembolso são exclusivas de operadores humanos L2 ou L1.
- **Consultas de Status de Envio:** O agente tem acesso L5 direto às APIs das transportadoras para informar o cliente sobre rastreamento em tempo real de equipamentos de som físicos e links de download ativos para presets digitais.
- **Tom de Voz:** O agente deve sempre manter uma postura profissional, de alta capacidade técnica em som automotivo e acústica, agilidade operacional, cortesia comercial e transparência legal.

#### 5.2 Segurança Lógica da Inteligência Artificial (Segurança do Daniel)

1.  **Grupamento de RAG Segregado (Sandboxing de Conhecimento):** O **Agente Daniel** somente terá acesso lógico de leitura à pasta `/workspace/knowledge/` e `/workspace/artifacts/`. Sob nenhuma circunstância ele poderá ler pastas confidenciais de banco de dados internos de senhas ou códigos-fonte principais do ERP da empresa.
2.  **Proteção contra Engenharia de Prompt e Injeção de Instruções (Prompt Injection):** A arquitetura do sistema do agente deve possuir filtros semânticos avançados na entrada (input) para barrar comandos que tentem forçar o agente a:
    - Revelar regras de faturamento internas que não pertençam ao FAQ público.
    - Inventar preços falsos, conceder cupons de desconto absurdos ou alterar alíquotas do Programa de Afiliados.
    - Adotar personas inadequadas ou desferir discursos ofensivos.
3.  **Tratamento de Dados Pessoais Sensíveis:** Se um cliente enviar dados sensíveis (fotos de documentos pessoais para estorno) no chat, o **Agente Daniel** deve processar a triagem e acionar imediatamente a rotina de exclusão temporária desses arquivos após o encerramento do chamado de atendimento, transferindo as informações de faturamento relevantes para o ERP com criptografia forte de ponta a ponta.
4.  **Auditoria de Conversas e Logs:** Todas as interações mantidas com o **Agente Daniel** serão gravadas em banco de dados seguro de logs de auditoria e revisadas periodicamente pela diretoria para aprimoramento contínuo das respostas baseadas na base de conhecimento.

---

### 6. SEGURANÇA DE REDES, WI-FI E ACESSO REMOTO

A infraestrutura de redes de dados da **Dnel Som soluções digitais** está dividida em camadas físicas e lógicas isoladas para impedir que acessos de clientes na oficina física afetem os sistemas de faturamento e os bancos de dados dos serviços digitais.

#### 6.1 Isolamento de Redes Sem Fio (Wi-Fi)

A nossa rede Wi-Fi na oficina física e showroom está dividida em duas redes independentes:

1.  **Rede Corporativa (`DnelSom_Corp`):** Exclusiva para uso em notebooks administrativos, tablets de checklists físicos dos instaladores e servidores de som. Possui ocultação de SSID (rede invisível de busca comum), criptografia WPA3, controle de acesso baseado em endereço físico de placa de rede (MAC Address) dos dispositivos autorizados e MFA obrigatório no login.
2.  **Rede de Clientes/Visitantes (`DnelSom_Clientes`):** Rede de acesso aberto ou por meio de portal de cadastro simplificado (Hotspot social em conformidade com a LGPD e Marco Civil da Internet). Esta rede é completamente isolada por VLAN dedicada de modo a impedir qualquer comunicação de rede ou acesso a pastas compartilhadas do setor administrativo ou do **Agente Daniel**.

#### 6.2 Acesso Remoto de Desenvolvedores e Suporte (VPN)

- **Acesso Seguro:** Qualquer acesso remoto à infraestrutura em nuvem, repositório de códigos de som digital ou painel administrativo do ERP da empresa por parte de desenvolvedores, engenheiros de som externos ou suporte administrativo em home office exige conexão obrigatória por canal criptografado de **Rede Virtual Privada (VPN)** corporativa com criptografia IPSec/OpenVPN.
- **Dispositivo Seguro:** Fica proibido acessar a VPN da empresa utilizando computadores públicos de lan houses ou lan offices. É obrigatório o uso de antivírus ativo e atualizado no computador pessoal autorizado do colaborador remoto.

---

### 7. CONFORMIDADE COM A LGPD E PROTEÇÃO DE DADOS

A conformidade com a Lei Geral de Proteção de Dados (Lei nº 13.709/2018) é um requisito essencial para a operação da **Dnel Som soluções digitais**, garantindo o respeito à privacidade dos nossos clientes físicos e digitais.

#### 7.1 Regras de Coleta e Consentimento

- **Minimização de Dados:** Somente coletaremos os dados estritamente necessários para o faturamento fiscal (Nota Fiscal), envio logístico de equipamentos físicos de som, suporte técnico do **Agente Daniel** e pagamento de comissões aos Afiliados autorizados.
- **Consentimento Expresso:** Toda compra física, contratação de projetos digitais de som ou cadastro de afiliados exige o aceite expresso e de livre vontade dos Termos de Uso e Política de Privacidade da marca, com registro de log da data e hora do consentimento.

#### 7.2 Regras de Conduta Prática LGPD dos Colaboradores

1.  **Bloqueio Automático de Estações:** Toda estação de trabalho, computador administrativo ou terminal de checkout na oficina deve possuir bloqueio automático de tela em caso de inatividade superior a **2 minutos**. É dever do colaborador realizar o bloqueio imediato (`Win + L` no Windows) ao se levantar do terminal.
2.  **Proibição de Equipamentos Pessoais:** É proibido processar, copiar ou extrair dados cadastrais de clientes ou ordens de serviço de som automotivo para mídias físicas pessoais (pendrives, HDs externos, contas particulares em nuvem ou celulares pessoais dos instaladores).
3.  **Proibição de Captura não Autorizada:** Conforme descrito no Código de Conduta, é proibido tirar fotografias ou vídeos dos veículos de clientes que exponham placas de automóveis, rostos ou dados pessoais sensíveis sem documento formal de autorização e consentimento de imagem assinado pelo cliente.
4.  **Descarte de Dados de Consumo:** Sempre que houver necessidade de dar manutenção física ou técnica em processadores de som digital (DSPs), módulos amplificadores com processamento ou centrais multimídia de clientes na oficina, o instalador chefe deve proceder com o **Reset de Fábrica (Wipe/Format)** do aparelho de áudio antes de liberar o equipamento, eliminando senhas e conexões Bluetooth de terceiros salvas na memória para total proteção de privacidade.

---

### 8. PLANOS DE CONTINGÊNCIA, BACKUP E RESILIÊNCIA

Em casos de desastres naturais, falhas severas de infraestrutura de rede, queda prolongada de fornecimento de energia elétrica ou vazamentos de dados, a empresa adotará planos de contingência padronizados para garantir a continuidade dos negócios (SLA) e a integridade de dados fiscais e operacionais.

#### 8.1 Contingência de Queda de Energia Elétrica e Geradores

Como a nossa oficina realiza instalações físicas de som e testes eletrônicos contínuos e o suporte digital opera com clientes online:

1.  **Sala de Servidores:** Possui fontes de alimentação ininterruptas (No-breaks/UPS) com autonomia mínima de **30 minutos** para manter os bancos de dados lógicos de projetos e o **Agente Daniel** funcionando sem desligamentos abruptos.
2.  **Acionamento do Gerador:** Em caso de interrupção de energia da concessionária que ultrapasse 5 minutos, o operador sênior deve conferir as travas de segurança eletrônica física e acionar o gerador de energia a diesel auxiliar localizado no recuo externo da loja em conformidade técnica.
3.  **Equipamentos Sensíveis:** Desligar da tomada osciloscópios, RTA (analisadores de espectro acústico) e módulos de calibração que não estejam em uso imediato para evitar picos de alta tensão no retorno da energia da rede pública.

#### 8.2 Política de Backup de Dados em Nuvem (Cloud) e Físico

Para prevenir perda permanente de dados de clientes, projetos de equalização de áudio e arquivos de faturamento:

- **Backup do Banco de Dados Geral (ERP e Afiliados):** Realizado de forma automática a cada **4 horas**, com sincronização criptografada e cópias armazenadas em pelo menos duas regiões geográficas distintas de servidores cloud (Multicloud Redundancy).
- **Backup Físico Mensal (Off-line):** No último dia útil de cada mês, o financeiro administrativo realizará a extração e a gravação de um backup criptografado off-line (Cold Backup) de todas as notas fiscais emitidas e dos arquivos de presets digitais de som desenvolvidos. Este dispositivo físico (HD de segurança com biqueira e blindagem eletrostática) deve ser mantido trancado em cofre físico externo na posse da diretoria.

#### 8.3 Contingência para Incidentes de Segurança e Resposta a Vazamento de Dados

Caso seja detectado qualquer indício de ataque hacker, intrusão lógica de terceiros ou suspeita de vazamento de dados de faturamento/clientes:

1.  **Isolamento Imediato:** O setor técnico administrativo deve isolar imediatamente os servidores ou servidores cloud comprometidos da rede de dados pública para barrar a exfiltração lógica de informações.
2.  **Redefinição Geral:** Forçar a alteração de senhas corporativas e tokens MFA de todas as credenciais administrativas em nuvem e servidores locais.
3.  **Investigação de Causa Raiz:** Auditar logs de sistema para identificar a causa raiz, o ponto de intrusão, o volume de dados comprometido e as respectivas contas de usuários logadas no momento da violação.
4.  **Notificação e Transparência Legal (LGPD):** Se houver risco aos titulares dos dados, a diretoria providenciará em conformidade com o prazo legal estabelecido pela Autoridade Nacional de Proteção de Dados (ANPD) a comunicação transparente do evento de segurança cibernética aos clientes afetados, informando detalhadamente as medidas de segurança mitigadoras tomadas.

---

### 9. RESPONSABILIDADES E TERMO DE COMPROMISSO

A segurança da informação e a proteção física das instalações da **Dnel Som soluções digitais** dependem do esforço conjunto, disciplina e responsabilidade individual de cada colaborador corporativo.

O descumprimento de qualquer política de segurança de dados descrita neste manual, compartilhamento de credenciais individuais sensíveis, vazamento intencional de projetos e presets de som digitais, exposição de placas de veículos de clientes sem consentimento formal ou desvio intencional de chamados lógicos do **Agente Daniel** sujeitará o funcionário envolvido a sanções disciplinares severas:

- **Infração Leve:** Advertência Verbal com anotação em registro e ficha funcional.
- **Infração Média:** Advertência por Escrito com Ficha de Ocorrência assinada em duas vias.
- **Infração Grave:** Suspensão imediata de 1 a 3 dias úteis sem remuneração e suspensão total de acessos lógicos.
- **Infração Gravíssima:** Demissão por Justa Causa fundamentada nos termos do Artigo 482 da Consolidação das Leis do Trabalho (CLT), acompanhada de abertura de inquérito e ação legal de responsabilidade civil/penal em caso de danos reputacionais ou financeiros intencionais causados à empresa.

---

### 10. ANEXO I – FICHA DE AUDITORIA E CONTROLE DE ACESSOS

#### DNEL SOM SOLUÇÕES DIGITAIS

**FICHA DE AUDITORIA DE SEGURANÇA E ACESSOS Nº: ****\_\_\_\_******

- **Data da Auditoria:** \_**\_/\_\_**/**\_\_** **Horário:** **\_\_**:**\_\_**
- **Responsável pelo Registro Técnico:** ******************\_\_\_******************
- **Setor Auditado:** ( ) Administrativo ( ) TI/Infraestrutura ( ) Oficina Física ( ) Suporte Digital

#### Itens Críticos de Segurança Verificados:

1.  **Políticas de Senhas Ativas:** ( ) Em Conformidade ( ) Não Conforme (Necessita de Reset Preventivo)
2.  **Duplo Fator (MFA) nos Gateways:** ( ) Confirmado ( ) Falha Técnica Detectada
3.  **Logs de Acesso do Agente Daniel:** ( ) Auditados sem Anomalias ( ) Tentativa de Injeção Registrada
4.  **Backup off-line Mensal Executado:** ( ) Sim (Data: \_**\_/\_\_**/\_\_\_\_) ( ) Pendente de Gravação Física
5.  **Isolamento da Rede Wi-Fi de Clientes:** ( ) Em Conformidade ( ) Vazamento de Pacotes Detectado
6.  **Câmeras de Segurança Operando 100%:** ( ) Sim ( ) Falha de Gravação Físico/Nuvem no Setor: ****\_\_\_****

#### Descrição Detalhada de Anomalias ou Correções de Acesso Aplicadas:

---

---

---

---

#### Assinaturas Técnicas de Validação:

---

**Encarregado de TI e Segurança da Informação**

---

**Gerência / Diretoria Administrativa (Ciência e Validação)**

---

Eu, ************************\_\_\_\_************************, portador do CPF **********\_\_**********, declaro na data de hoje que li, recebi e compreendi integralmente as regras operacionais de acessos corporativos, política de senhas, governança com o **Agente Daniel** e conformidade LGPD descritas neste manual oficial, assumindo integral responsabilidade jurídica e operacional no cumprimento de minhas funções diárias na **Dnel Som soluções digitais**.

São Paulo, \_**\_ de ****\_\_\_\_****** de 20\_\_.

---

**Assinatura do Colaborador Executante**

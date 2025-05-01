from faker import Faker 
import pandas as pd
from datetime import datetime, timedelta
import uuid
import random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import base64
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from decimal import Decimal

fake = Faker(locale='pt_BR')  # Configuração Local 

def get_valid_aes_key(key: str) -> bytes:
    """Gera uma chave de 32 bytes a partir de uma string qualquer."""
    return SHA256.new(key.encode()).digest()

chave_base = "Chavesecreta1234" 
chave_criptografia = get_valid_aes_key(chave_base)

def encrypt_data(data):
    cipher = AES.new(chave_criptografia, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode('utf-8'))
    
    # Concatenar nonce + tag + ciphertext e codificar em base64 para facilitar armazenamento
    encrypted_blob = cipher.nonce + tag + ciphertext
    return base64.b64encode(encrypted_blob).decode('utf-8')

def decrypt_data(encrypted_base64):
    encrypted_blob = base64.b64decode(encrypted_base64)
    
    # Extrair nonce, tag e ciphertext
    nonce = encrypted_blob[:16]
    tag = encrypted_blob[16:32]
    ciphertext = encrypted_blob[32:]
    
    cipher = AES.new(chave_criptografia, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data.decode('utf-8')

class Planos:
    def __init__(self,tipo_plano,espera_pagamento_dias,valor_plano,quant_conexao_mes,taxa_aplicada):
        self.tipo_plano = tipo_plano
        self.espera_pagamento_dias = espera_pagamento_dias
        self.valor_plano = valor_plano
        self.quant_conexao_mes = quant_conexao_mes
        self.taxa_aplicada = taxa_aplicada

class Banco:
    def __init__(self, nome, codigo, numero_conta, numero_agencia, codigo_carteira_boleto, digito_verificador = None):
        self.nome = nome
        self.codigo = codigo
        self.numero_conta = numero_conta 
        self.numero_agencia = numero_agencia
        self.codigo_carteira_boleto = codigo_carteira_boleto
        self.digito_verificador = digito_verificador

def Gerar_codigo_aleatorio():
    return str(random.randint(1, 100))

GeradorBancos_Brasileiros = [
    Banco(nome="Banco do Brasil", codigo="001", numero_conta=8, numero_agencia=4, codigo_carteira_boleto="17", digito_verificador=1),
    Banco(nome="Caixa Econômica Federal", codigo="104", numero_conta=11, numero_agencia=4, codigo_carteira_boleto="14", digito_verificador=1),
    Banco(nome="Bradesco", codigo="237", numero_conta=7, numero_agencia=4, codigo_carteira_boleto="09", digito_verificador=1),
    Banco(nome="Itaú Unibanco", codigo="341", numero_conta=5, numero_agencia=4, codigo_carteira_boleto="109", digito_verificador=1),
    Banco(nome="Santander", codigo="033", numero_conta=8, numero_agencia=4, codigo_carteira_boleto="101", digito_verificador=1),
    Banco(nome="Nubank", codigo="260", numero_conta=7, numero_agencia=4, codigo_carteira_boleto="21", digito_verificador=0),
    Banco(nome="Inter", codigo="077", numero_conta=8, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=0),
    Banco(nome="BTG Pactual", codigo="208", numero_conta=6, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="Safra", codigo="422", numero_conta=9, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="C6 Bank", codigo="336", numero_conta=7, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=0),
    Banco(nome="Banrisul", codigo="041", numero_conta=8, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="Sicoob", codigo="756", numero_conta=10, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="Sicredi", codigo="748", numero_conta=5, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="Original", codigo="212", numero_conta=7, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=1),
    Banco(nome="PagBank", codigo="290", numero_conta=8, numero_agencia=4, codigo_carteira_boleto=Gerar_codigo_aleatorio(), digito_verificador=0),
]

metodo_pagamento = [1,2,3,4,5]

tipo = ['Cliente','Freelancer','Administrador','Suporte']

status = ['ativo','Banido','Excluído',]

status_projetos = ['Aberto a Propostas','Projeto em Execução','Projeto Concluído','Projeto Cancelado']
def create_usuarios(num_usuarios):
    usuarios_list = []
    
    for i in range(1,num_usuarios + 1):
        usuario = {}
        usuario['id'] = i 
        usuario['nome_completo'] = fake.name()
        usuario['email'] = fake.email()
        usuario['senha_hash'] = encrypt_data(fake.password())
        usuario['tipo'] = random.choices(tipo, weights=[50,30,10,10])[0]
        usuario['telefone_formatado'] = fake.phone_number()
        usuario['ultimo_login'] = fake.date_time_this_year(before_now=True) if random.random() > 0.2 else None

        if usuario['tipo'] in ('Administrador', 'Suporte'):
            status_usuario = random.choices(['ativo', 'Excluído'], weights=[80, 20])[0]
        else:
            status_usuario = random.choices(status, weights=[70, 15, 15])[0]
            
        usuario['status_usuario'] = status_usuario
        usuarios_list.append(usuario)
    return pd.DataFrame(usuarios_list)

data_usuario = create_usuarios(10000)
data_usuario = data_usuario.drop_duplicates(subset=['email','telefone_formatado'])

try:
    data_usuario.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/usuario.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_funcionarios(data_usuario):
    funcionarios_list = []
       
    usuarios_funcionarios = data_usuario[
    data_usuario['tipo'].isin(['Administrador', 'Suporte'])
    ]

    for i , (_, row) in enumerate(usuarios_funcionarios.iterrows(),start=1):
        funcionario = {}
        funcionario['id'] = i
        funcionario['id_usuario'] = row['id']
        funcionario['id_cargo'] = 1 if row['tipo'] == 'Administrador' else 2
        funcionario['cpf'] = fake.cpf()
        funcionario['matricula'] = f"MAT{datetime.now().year}{str(i).zfill(4)}"
        funcionario['data_admissao'] = fake.date_between(start_date='-5y', end_date='today')
        funcionario['foto_perfil'] = fake.image_url()
        funcionario['ativo'] = random.choice([1,0])
        funcionarios_list.append(funcionario)
    return pd.DataFrame(funcionarios_list)

data_funcionarios = create_funcionarios(data_usuario)
data_funcionarios = data_funcionarios.drop_duplicates(subset=['cpf','foto_perfil'])

try:
    data_funcionarios.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/funcionarios.csv', index=False)
except FileNotFoundError:
   print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_usuarios_excluidos(data_usuario):
    usuarios_excluidos_list = []
    usuario_exc = data_usuario[
    (data_usuario['status_usuario'] == 'Excluído') &
    (data_usuario['tipo'].isin(['Freelancer','Cliente']))
        ] 
    for i, (_, row) in enumerate(usuario_exc.iterrows(),start=1):
        usuario_excluido = {}
        usuario_excluido['id_usuario'] = row['id']
        usuario_excluido['motivo_exclusão'] = fake.random_element(elements=(      
                "Solicitação do usuário",
                "Conta duplicada",
                "Inatividade prolongada",
                "Solicitação via e-mail",
                "Problemas com verificação de identidade",
                "Migração para outro sistema",
                "Erro no cadastro"))
        usuario_excluido['data_exclusao'] = fake.date_time_between(start_date=datetime.now() - timedelta(days=5*365), end_date=datetime.now())
        usuarios_excluidos_list.append(usuario_excluido)
    return pd.DataFrame(usuarios_excluidos_list)

data_excluidos = create_usuarios_excluidos(data_usuario)
data_excluidos = data_excluidos.drop_duplicates(subset=('id_usuario'))

try:
    data_excluidos.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/excluidos.csv',index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_usuarios_banidos(data_usuario,data_funcionarios):
    usuarios_banidos_list = []
    usuario_ban = data_usuario[(data_usuario['status_usuario'] == 'Banido') &
    (data_usuario['tipo'].isin(['Cliente','Freelancer']))]

    administradores = data_funcionarios[data_funcionarios['id_cargo'] == 2]
    for i, (_, row) in enumerate(usuario_ban.iterrows(),start=1):
        usuario_banido = {}
        usuario_banido['id_usuario'] = row['id']
        admin = administradores.sample(n=1).iloc[0]
        usuario_banido['id_funcionario'] = admin['id']
        usuario_banido['motivo_banimento'] = fake.random_element(elements=(    
                "Violação dos termos de uso",
                "Atividade suspeita detectada",
                "Fraude confirmada",
                "Uso de linguagem ofensiva",
                "Comportamento abusivo com outros usuários",
                "Spam repetido",
                "Tentativa de invasão"))
        usuarios_banidos_list.append(usuario_banido)    
    return pd.DataFrame(usuarios_banidos_list)
    
data_banidos = create_usuarios_banidos(data_usuario,data_funcionarios)
try:
    data_banidos.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/banidos.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_clientes(data_usuario):
    clientes_list = []
    cliente_usuario = data_usuario[data_usuario['tipo'].isin(['Cliente'])]
    for i ,(_, row) in enumerate(cliente_usuario.iterrows(),start=1):
        cliente = {}
        cliente['id'] = i
        cliente['id_usuario'] = row['id']
        cliente['empresa'] = fake.random_element(elements=(    
                "Empresa 101",
                "Companhia 202",
                "Serviços 303",
                "Grupo 404",
                "Negócios 505",
                "Corporation 606",
                "Soluções 707",
                "Tech 808",
                "Industria 909",
                "Agência 010",
                "Holding 111",
                "Digital 222",
                "Consultoria 333",
                "Inovação 444",
                "Freelas 555",
                "Desenvolve 666",
                "Start 777",
                "Connect 888",
                "Power 999",
                "Cria 000"))
        cliente['cpf_cnpj'] = fake.random_element(elements=[fake.cpf(), fake.cnpj()])
        cliente["foto_perfil"] = fake.image_url()
        cliente["localizacao"] = fake.address()
        clientes_list.append(cliente)
    return pd.DataFrame(clientes_list)

data_clientes = create_clientes(data_usuario)
data_clientes = data_clientes.drop_duplicates(subset=['id_usuario','cpf_cnpj'])
try:
    data_clientes.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/clientes.csv' ,index=False)
except FileNotFoundError:
   print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_freelancers(data_usuario):
    freelancers_list = []

    freelancer_usuario = data_usuario[data_usuario['tipo'].isin(['Freelancer'])]
    for i, (_,row) in enumerate(freelancer_usuario.iterrows(),start=1):
        freelancer = {}
        freelancer['id'] = i
        freelancer['id_usuario'] = row['id']
        freelancer['id_plano'] = fake.random_element(elements=(1,2,3))
        freelancer['drescrição'] = fake.text(max_nb_chars=500)
        freelancer['cpf_cnpj'] = fake.random_element(elements=[fake.cpf(), fake.cnpj()])
        freelancer['idiomas'] = fake.random_elements(elements=(
                "Português",
                "Inglês",
                "Espanhol",
                "Francês",
                "Alemão",
                "Italiano",
                "Chinês",
                "Japonês",
                "Coreano",
                "Russo",
                "Árabe",
                "Hindi",
                "Turco",
                "Polonês",
                "Holandês",
                "Sueco",
                "Norueguês",
                "Tailandês",
                "Grego",
                "Hebraico",
                "Romeno",
                "Tcheco",
                "Vietnamita",
                "Ucraniano",
                "Indonésio"))
        freelancer["foto_perfil"] = fake.image_url()
        freelancers_list.append(freelancer)
    return pd.DataFrame(freelancers_list)

data_freelancers = create_freelancers(data_usuario)
data_freelancers = data_freelancers.drop_duplicates(subset=['id_usuario','cpf_cnpj'])

try:
    data_freelancers.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/freelancers.csv' ,index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_freelancer_especialidades(data_freelancers):
    freelancer_especialidades_list = []

    especialidades_ids = list(range(1, 15))
    ids_escolhidos = fake.random_elements(elements=especialidades_ids, unique=True, length=random.randint(1, 5))

    for i, (_,row) in enumerate(data_freelancers.iterrows(),start=1):
        freelancer_especialidade = {}
        freelancer_especialidade['id_freelancer'] = row['id']
        freelancer_especialidade['id_especialidade'] = ids_escolhidos
        freelancer_especialidade['nivel_proeficiencia'] = fake.random_element(elements=('Iniciante', 'Intermediário', 'Avançado', 'Especialista'))
        freelancer_especialidades_list.append(freelancer_especialidade)
    return pd.DataFrame(freelancer_especialidades_list)

data_freelancer_especialidades = create_freelancer_especialidades(data_freelancers)
data_freelancer_especialidades = data_freelancer_especialidades.drop_duplicates(subset=["id_freelancer"])

try:
    data_freelancer_especialidades.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/freelancer_especialidades.csv' ,index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_projetos(data_clientes):
    projetos_list = []

    for i, (_, row) in enumerate(data_clientes.iterrows(), start=1):
        projeto = {}
        projeto['id'] = i
        projeto['id_cliente'] = row['id']
        projeto['id_categoria'] = fake.random_int(min=1,max=10)
        projeto['status_projeto'] = random.choices(status_projetos, weights=[35, 20, 35,10])[0]
        projeto['titulo'] = f"{fake.word().title()} {fake.word().title()} {fake.random_element(elements=['Projeto', 'Sistema', 'Plataforma', 'Solução'])}"
        projeto['descricao'] = fake.text(max_nb_chars=200)
        projeto['orcamento'] = fake.pydecimal(
                left_digits=6,  # Parte inteira max 999999
                right_digits=2,  # 2 Casas decimais
                positive=True,
                min_value=10,
                max_value=1000
            )
        projetos_list.append(projeto)
    return pd.DataFrame(projetos_list)

data_projetos = create_projetos(data_clientes)
data_projetos = data_projetos.drop_duplicates(subset=['id_cliente'])

try:
    data_projetos.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/projetos.csv', index=False)
except FileNotFoundError:
        print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_propostas(data_projetos,data_freelancers):
    propostas_list = []
    
    for i,(_ ,row)in enumerate(data_projetos.iterrows(),start=1):
        proposta = {}
        proposta['id'] = i
        proposta['id_projeto'] = row['id']
        proposta['id_freelancer'] = fake.random_element(elements=data_freelancers['id'].tolist())
        status_projeto = row['status_projeto'] 

        if status_projeto  == 'Aberto a Propostas':
            status_proposta = random.choice(['Pendente','Recusada'])

        elif status_projeto  == 'Projeto em Execução':
            status_proposta = 'Aceita/Em Andamento'

        elif status_projeto  == 'Projeto Concluído':
            status_proposta = 'Aceita/Finalizada'

        elif status_projeto  == 'Projeto Cancelado':
            status_proposta = 'Cancelada'
        else:
            return 1
        proposta['status_proposta'] = status_proposta
        proposta['valor_proposta'] = fake.pydecimal(
            right_digits=2,
            left_digits=6,
            positive=True,
            max_value=10000,
            min_value=10
        )
        proposta['prazo_entrega'] = fake.date_time_between(
                    start_date=timedelta(days=7),
                    end_date=timedelta(days=20)
            )
        proposta['descricao'] = fake.text(max_nb_chars=350)
        propostas_list.append(proposta)
    return pd.DataFrame(propostas_list)

data_propostas = create_propostas(data_projetos,data_freelancers)

try:
    data_propostas.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/propostas.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_pagamentos_clientes(data_propostas,data_projetos):
    pagamentos_clientes_list = []

    projeto_para_cliente = dict(zip(data_projetos['id'], data_projetos['id_cliente']))

    metodo_escolhido = random.choice(metodo_pagamento)

    projetos_concluidos = data_projetos[data_projetos['status_projeto'] == 'Projeto Concluído']
    propostas_validas = data_propostas[
        (data_propostas['status_proposta'] == 'Aceita/Finalizada') &
        (data_propostas['id_projeto'].isin(projetos_concluidos['id']))
    ]

    for i, (_,row) in enumerate(propostas_validas.iterrows(),start=1):
        pagamento_cliente = {}
        pagamento_cliente['id'] = i
        pagamento_cliente['id_metodo_pagamento'] = metodo_escolhido
        pagamento_cliente['id_proposta'] = row['id']
        pagamento_cliente['id_cliente'] = projeto_para_cliente.get(row['id_projeto'])
        pagamento_cliente['status_pagamento'] = random.choice(('Pendente','Processando', 'Concluído', 'Falhou', 'Estornado'))
        pagamento_cliente['valor_bruto'] = round(row['valor_proposta'],2)
        pagamento_cliente['data_pagamento'] = None
         
        if pagamento_cliente['status_pagamento'] == 'Concluído':
            data_registro_fake = fake.date_time_between(start_date='-6M', end_date='now')
            pagamento_cliente['data_pagamento'] = fake.date_time_between(start_date=data_registro_fake,end_date='now')
        pagamentos_clientes_list.append(pagamento_cliente)
    return pd.DataFrame(pagamentos_clientes_list)
    
data_pagamentos_clientes = create_pagamentos_clientes(data_propostas,data_projetos)
data_pagamentos_clientes = data_pagamentos_clientes.drop_duplicates(subset=(['id_proposta']))

try:
    data_pagamentos_clientes.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/pagamentos_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_info_bancaria_freelancers(data_freelancers):
    bancaria_freelancers_list = []

    for i,(_, row) in enumerate(data_freelancers.iterrows(),start=1):
        banco_freelancer = {}
        banco_freelancer['id'] = i
        banco_freelancer['id_freelancer'] = row['id']
        
        banco_escolhido = random.choice (GeradorBancos_Brasileiros)

        banco_freelancer['banco'] = banco_escolhido.nome
        banco_freelancer['codigo_banco'] = encrypt_data(banco_escolhido.codigo)
        banco_freelancer['agencia'] =  encrypt_data(str(fake.random_number(digits=banco_escolhido.numero_agencia, fix_len=True)))
        banco_freelancer['numero_conta'] = encrypt_data(str(fake.random_number(digits=banco_escolhido.numero_conta, fix_len=True)))
        banco_freelancer['digito'] = encrypt_data(str(fake.random_number(digits=banco_escolhido.digito_verificador, fix_len=True)) if banco_escolhido.digito_verificador > 0 else '')
        banco_freelancer['tipo_conta'] = fake.random_element(elements=(['Corrente','Poupança','Pagamento']))
        bancaria_freelancers_list.append(banco_freelancer)
    return pd.DataFrame(bancaria_freelancers_list)

data_bancaria_freelancer = create_info_bancaria_freelancers(data_freelancers)
data_bancaria_freelancer = data_bancaria_freelancer.drop_duplicates(subset=('id_freelancer'))

try:
    data_bancaria_freelancer.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/info_bancaria_freelancer.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_pagamentos_freelancers(data_pagamentos_clientes,data_bancaria_freelancer,data_propostas,data_freelancers):
    pagamento_freelancers_list = []

    pagamentos_concluidos = data_pagamentos_clientes[data_pagamentos_clientes['status_pagamento'] == 'Concluído']
    ids_propostas_concluidas = pagamentos_concluidos['id_proposta'].tolist()

    ids_propostas_concluidas_freelancer = data_propostas[data_propostas['id'].isin(ids_propostas_concluidas)]
    ids_freelancers = ids_propostas_concluidas_freelancer['id_freelancer'].tolist()
    ids_propostas_info_freelancer = data_bancaria_freelancer [data_bancaria_freelancer['id_freelancer'].isin(ids_freelancers)]
    
    freelancer_plano = dict(zip(data_freelancers['id'], data_freelancers['id_plano']))

    for i, (_,row) in enumerate(pagamentos_concluidos.iterrows(),start=1):
        pagamento_freelancer = {}
        pagamento_freelancer['id_'] = i
        pagamento_freelancer['id_pagamento_cliente'] = row['id']

        id_freelancer = data_propostas.loc[data_propostas['id'] == row['id_proposta'], 'id_freelancer'].values[0]
        info_bancaria = ids_propostas_info_freelancer[ids_propostas_info_freelancer['id_freelancer'] == id_freelancer]
        pagamento_freelancer['id_info_bancaria_freelancer'] = info_bancaria['id'].values[0] 

        id_plano = freelancer_plano.get(id_freelancer)

        valor_bruto = row['valor_bruto']

        if id_plano == 1:
            valor_liquido  = round(valor_bruto * Decimal('0.80'),2)
            taxa_aplicada = 20
            espera_dias = 6
        elif id_plano == 2:
            valor_liquido  = round(valor_bruto * Decimal('0.85'),2)
            taxa_aplicada = 15
            espera_dias = 5
        elif id_plano == 3:
            valor_liquido  = round(valor_bruto * Decimal('0.90'),2)
            taxa_aplicada = 10
            espera_dias = 2
        else : 
            return 1

        pagamento_freelancer['valor_liquido'] = valor_liquido
        pagamento_freelancer['taxa_aplicada'] = taxa_aplicada
        data_registro = datetime.now()
        data_pagamento = data_registro + timedelta(days=espera_dias)
        pagamento_freelancer['data_pagamento'] = fake.date_time_between(start_date=data_pagamento)
        pagamento_freelancers_list.append(pagamento_freelancer)

    return pd.DataFrame(pagamento_freelancers_list)

data_pagamentos_freelancers = create_pagamentos_freelancers(data_pagamentos_clientes,data_bancaria_freelancer,data_propostas,data_freelancers)
data_pagamentos_freelancers = data_pagamentos_freelancers.drop_duplicates(subset=(['id_pagamento_cliente']))
try:
    data_pagamentos_freelancers.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/pagamento_freelancers.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_cartao_credito_clientes(data_pagamentos_clientes):    
                                            
    info_credito_clientes_list = []
    
    banco_escolhido = random.choice(GeradorBancos_Brasileiros)

    for i, (_,row) in enumerate(data_pagamentos_clientes.iterrows(),start=1):
        credito_cliente = {}
        credito_cliente['id_pagamento_cliente'] = row['id']
        credito_cliente['nome_titular'] = encrypt_data(fake.name())
        credito_cliente['instituicao'] = banco_escolhido.nome
        credito_cliente['ultimos_digitos'] = encrypt_data(fake.credit_card_number()[-4:])
        credito_cliente['validade_mes'] = encrypt_data(str(random.randint(1, 12)).zfill(2))
        credito_cliente['validade_ano'] = encrypt_data(str(random.randint(26,31)).zfill(2))
        credito_cliente['cvv'] = fake.credit_card_security_code()
        credito_cliente['token_gateway'] = encrypt_data(str(uuid.uuid4()))
        credito_cliente["ativo"]= random.choice([0, 1])
        info_credito_clientes_list.append(credito_cliente)
    return pd.DataFrame(info_credito_clientes_list)

data_credito_cliente = create_cartao_credito_clientes(data_pagamentos_clientes)

data_credito_cliente = data_credito_cliente.drop_duplicates(subset=[    
    'id_pagamento_cliente',
    'instituicao',
    'ultimos_digitos',
    'validade_mes',
    'validade_ano',
    'cvv',
    'token_gateway'
    ])

try :
    data_credito_cliente.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/credito_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_pix_clientes(data_pagamentos_clientes):
    pix_clientes_list = []

    banco_escolhido = random.choice(GeradorBancos_Brasileiros)
    for i,(_,row) in enumerate(data_pagamentos_clientes.iterrows(), start=1):
        pix = {}
        pix['id_pagamento_cliente'] = row['id']
        pix['chave_pix_paga'] = encrypt_data(str(uuid.uuid4()).replace(" - ", " ").upper()[:32])
        pix['nome_titular'] = encrypt_data(fake.name())
        pix['instituicao'] = banco_escolhido.nome
        pix_clientes_list.append(pix)
    return pd.DataFrame(pix_clientes_list)
data_pix_clientes = create_pix_clientes(data_pagamentos_clientes)
data_pix_clientes = data_pix_clientes.drop_duplicates(subset=['id_pagamento_cliente'])

try:
    data_pix_clientes.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/pix_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_boletos_clientes(data_pagamentos_clientes):
    info_boleto_list = []
    
    for i,(_,row) in enumerate(data_pagamentos_clientes.iterrows(),start=1):
        boleto = {}
        boleto['id_pagamento_cliente'] = row['id']
        boleto['codigo_barras'] = fake.numerify(text='###############################')
        boleto['linha_digitavel'] = fake.numerify(text='#####.##### #####.###### #####.###### # ##############')
        boleto['data_vencimento'] = fake.date_time_between(start_date='now', end_date=timedelta(days=2))
        boleto['url_boleto'] = encrypt_data(fake.url())
        boleto['ativo'] = random.choice([0,1])
        info_boleto_list.append(boleto)
    return pd.DataFrame(info_boleto_list)
data_boleto = create_boletos_clientes(data_pagamentos_clientes)
data_boleto = data_boleto.drop_duplicates(subset=['id_pagamento_cliente'])

try:
    data_boleto.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/boletos_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_ted_clientes(data_pagamentos_clientes):
    ted_clientes_list = []
    banco_escolhido = random.choice(GeradorBancos_Brasileiros)

    for i,(_,row) in enumerate(data_pagamentos_clientes.iterrows(),start=1):
        ted = {}
        ted['id_pagamento_cliente'] = row['id']
        ted['nome_titular'] = encrypt_data(fake.name())
        ted['banco'] = banco_escolhido.nome
        ted['agencia'] = encrypt_data(str(fake.random_number(digits=banco_escolhido.numero_agencia, fix_len=True)))
        ted['numero_conta'] = encrypt_data(str(fake.random_number(digits=banco_escolhido.numero_conta, fix_len=True)))
        ted['tipo_conta'] = fake.random_element(elements=[1,2,3,4])
        ted_clientes_list.append(ted)
    return pd.DataFrame(ted_clientes_list)
data_ted = create_ted_clientes(data_pagamentos_clientes)
data_ted = data_ted.drop_duplicates(subset=['id_pagamento_cliente'])

try:
    data_ted.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/ted_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')
    
def create_avaliacoes_projetos_freelancers(data_projetos,data_freelancers):
    avaliacoes_freelancer_list = []

    for i, (_, row) in enumerate(data_projetos.iterrows(),start=1):
        avaliacao = {}
        avaliacao['id_projeto'] = row['id']
        avaliacao['id_freelancer'] = fake.random_element(elements=data_freelancers['id'].tolist())
        avaliacao['nota']  = fake.random_int(min=1, max=5)
        avaliacao['comentario'] = fake.text(max_nb_chars=300)
        avaliacoes_freelancer_list.append(avaliacao)
    return pd.DataFrame(avaliacoes_freelancer_list)

data_avaliacoes_projetos_freelacers = create_avaliacoes_projetos_freelancers(data_projetos, data_freelancers)
data_avaliacoes_projetos_freelacers = data_avaliacoes_projetos_freelacers.drop_duplicates(subset=['id_projeto', 'id_freelancer'])

try:
    data_avaliacoes_projetos_freelacers.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/avaliacoes_freelacers.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')

def create_avaliacoes_projetos_clientes(data_projetos,data_clientes):
    avaliacoes_cliente_list = []

    for i, (_, row) in enumerate(data_projetos.iterrows(),start=1):
        avaliacao = {}
        avaliacao['id_projeto'] = row['id']
        avaliacao['id_cliente'] = fake.random_element(elements=data_clientes['id'].tolist())
        avaliacao['nota']  = fake.random_int(min=1, max=5)
        avaliacao['comentario'] = fake.text(max_nb_chars=300)
        avaliacoes_cliente_list.append(avaliacao)
    return pd.DataFrame(avaliacoes_cliente_list)

data_avaliacoes_projetos_clientes = create_avaliacoes_projetos_clientes(data_projetos,data_clientes)
data_avaliacoes_projetos_clientes = data_avaliacoes_projetos_clientes.drop_duplicates(subset=['id_projeto', 'id_cliente'])

try:
    data_avaliacoes_projetos_clientes.to_csv('C:/Users/USER/Desktop/CODE_IBM/Project_Complete_DE/csv_files/avaliacoes_clientes.csv', index=False)
except FileNotFoundError:
    print('Error 404 - Falha ao encontrar o caminho a ser enviado, verifique se o caminho está correto')
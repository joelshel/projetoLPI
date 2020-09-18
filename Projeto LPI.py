#!/usr/bin/env python
# coding: utf-8

# In[3]:


from datetime import datetime
import json
try:
    import modsim 
except ImportError:
    get_ipython().system('pip install modsimpy')
    get_ipython().system('pip install pint')
    import modsim

def menu_principal():
    print('-'*7,'MENU PRINCIPAL','-'*7)
    while True:
        print('''1 – Introduzir novo doente
2 – Modificar sintomas
3 – Testar doente
4 – Remover doente
5 – Consultar sistema
6 – Gravar dados
7 - Carregar dados
8 – Simulação de ocupação UCI
0 – Sair''')
        print()
        try:
            opcao = int(input('O que deseja fazer? ').strip())
            if opcao not in (1,2,3,4,5,6,7,8,0):
                raise ValueError
            break
        except ValueError:
            print('Erro! Digite uma das seguintes opções: ')
        print()
    return opcao


def try_catch(mensagem='', condicao=False, mensagem_erro='', tamanho=1):
    while True:
        try:
            if condicao == False: # condicao == False é para validar strings
                dado = str(input(mensagem).strip().title())
                if dado[0].isnumeric():
                    raise ValueError
                if len(dado) == 0:
                    raise ValueError
            else:    # condicao == True (else) é para validar números (com um tamanho específico)
                dado = int(input(mensagem).strip().title())
                if len(str(dado)) != tamanho:
                    raise ValueError
            return dado
        except ValueError:
            print(mensagem_erro)


def menu_novo_doente(dados):
    print('-'*13,'NOVO DOENTE','-'*13)
    nome = try_catch('Insira o nome: ', False, 'Erro! Digite um nome válido!')
    telefone = try_catch('Insira nº telefone (9 dígitos): ', True, 'Erro! Digite um número de telefone válido!', 9)
    morada = try_catch('Insira a morada: ', False, 'Erro! Digite uma morada válida!')
    CC = try_catch('Insira o CC (8 dígitos): ', True, 'Erro! Digite um número de CC válido!', 8)
    while True:
        try:
            data_de_nascimento = datetime.strptime(input('Insira a data de nascimento (dd-mm-aaaa): ').strip(),'%d-%m-%Y')
            data_de_nascimento = data_de_nascimento.date()
            ano_atual = datetime.now().date()
            idade = int(str((ano_atual - data_de_nascimento)).split()[0]) 
            if idade < 0:
                raise ValueError
            idade = idade/365
            break
        except ValueError:
            print('Erro! Digite uma data de nascimento válida! ')

    total_etaria = 25702 # soma de todos os valores da figura 2 do enunciado
    if idade <= 9:
        prob_etaria = 436/total_etaria    # sem sintomas e com idade mínima a probabilidade é 0,42%
    elif 9 < idade <= 19:
        prob_etaria = 774/total_etaria    # cada número representa cada valor individual na figura 2
    elif 19 < idade <= 29:
        prob_etaria = 2994/total_etaria
    elif 29 < idade <= 39:
        prob_etaria = 3615/total_etaria
    elif 39 < idade <= 49:
        prob_etaria = 4276/total_etaria
    elif 49 < idade <= 59:
        prob_etaria = 4343/total_etaria
    elif 59 < idade <= 69:
        prob_etaria = 2955/total_etaria
    elif 69 < idade <= 79:
        prob_etaria = 2264/total_etaria
    else:
        prob_etaria = 4045/total_etaria
    prob_etaria *= 0.25 # a idade só influência em 25% na probabilidade do paciente ter covid-19
    
    sintomas = menu_sintomas()
    sintomas,  prob_sintomas = sintomas[:6], sintomas[6] # os sintomas em si só vão até á posição 5 da lista,
    prob_total_abs = (prob_etaria + prob_sintomas)*100   # o outro valor é os 75% que faltam da probabilidade (sintomas).
    prob_total_rel = prob_total_relativa(prob_total_abs) # converter a probabilidade de número para string (texto)
    dados_doente = [telefone, morada, CC, str(data_de_nascimento), sintomas, prob_total_abs, prob_total_rel, prob_etaria]
    dados[nome] = dados_doente
    print('Doente adicionado com sucesso!')
    print()
    return dados


def prob_total_relativa(prob_total_abs):
    if 0 < prob_total_abs <= 30: # nunca toca no 0
        prob_total_rel = 'Sem Risco'
    elif 30 < prob_total_abs <= 50:
        prob_total_rel = 'Baixo Risco'
    elif 50 < prob_total_abs <= 75:
        prob_total_rel = 'Medio Risco'
    elif 75 < prob_total_abs <= 100:
        prob_total_rel = 'Alto Risco'
    return prob_total_rel


def menu_sintomas():
    tosse = trycatch_s_n('Tosse? (s/n): ', True, 7968)
    temperatura = trycatch_s_n('Temperatura superior 37.8? (s/n): ', True, 11052)
    dores = trycatch_s_n('Dores musculares? (s/n): ', True, 5654)
    cefaleias = trycatch_s_n('Cefaleias? (s/n): ', True, 5140)
    fraqueza = trycatch_s_n('fraqueza? (s/n): ', True, 4112)
    dificuldade_respiratoria = trycatch_s_n('Dificuldade respiratória? (s/n): ', True, 3341)
    temp_sintomas = [tosse, temperatura, dores, cefaleias, fraqueza, dificuldade_respiratoria]
    prob_sintomas = 0
    for c in temp_sintomas:
         prob_sintomas += c[1] # o valor da posição 1 que a função retorna é que é para cálculo
    prob_sintomas *= 0.75 # os 75% que pertencem á probabilidade do paciente ter covid-19 (sintomas)
    sintomas = [tosse[0], temperatura[0], dores[0], cefaleias[0], fraqueza[0], dificuldade_respiratoria[0], prob_sintomas]
    return sintomas


def trycatch_s_n(frase='', quer_calculo=False, valor=1):
    while True:
        try:
            condicao = input(frase).strip().lower()[0]
            if condicao not in 'sn':
                raise ValueError
            if quer_calculo:
                if condicao == 's':
                    total_sintomas = 37267 # soma de todos os valores da figura 3 do enunciado
                    prob_sintomas = valor/total_sintomas # o valor é cada valor individual na figura 3
                    return condicao, prob_sintomas
                else:
                    return condicao, 0
            return condicao
        except ValueError:
            print('Erro! Digite "s" ou "n"!')

        
def trycatch_dados(dados, nome):
    if len(dados) == 0: # ou seja está vazio
        print('Não existe dados no sistema...')
    try:
        dados[nome] # se não existir dá erro
        return 0 
    except KeyError:
        print('Erro - doente não existe. Crie primeiro uma entrada…')



def menu_testar_doente(dados):
    while True:
        print('-'*9,'TESTAR DOENTE','-'*9)
        while True:
            nome = str(input('Insira o nome do Doente que pretende testar: ')).title().strip()
            continuar = trycatch_dados(dados, nome)
            if continuar == 0:
                break
            else:
                return
        probabilidade_de_covid  = dados[nome][5]
        print(f'O teste concluiu que existe {probabilidade_de_covid:.2f}% de probabilidade de covid-19.')
        estado_do_doente = dados[nome][6]
        print(f'O estado do doente foi alterado para: {estado_do_doente}.\n')
        continuar = trycatch_s_n('Testar outro doente? (s/n) ')
        print()
        if continuar == 'n':
            break


def menu_remover_doente(dados):
    while True:
        print('-'*10,'REMOVER DOENTE', '-'*10)
        while True:
            nome = str(input('Insira o nome do doente: ')).title().strip()
            continuar = trycatch_dados(dados, nome)
            if continuar == 0:
                break
            else:
                return
        while True:
            try:
                motivo = str(input('Insira o motivo: ')).strip()
                for c in motivo:
                    if c.isnumeric():
                        raise ValueError
                break
            except ValueError:
                print('Erro! Digite um motivo válido!')
        del dados[nome]
        print('Doente removido com sucesso!')
        continuar = trycatch_s_n('Remover outro doente? (s/n) ')
        print()
        if continuar in 'n':
            break


def menu_consultar_doentes():
    while True:
        print('-'*10,'CONSULTAR DOENTES','-'*10)
        print('''1 – Consultar sistema por doente
2 – Consultar sistema por estado
3 – Ver todos os doentes
0 – Voltar''')
        print()
        try:
            opcao = int(input('O que deseja fazer? ').strip())
            if opcao not in (1,2,3,0):
                raise ValueError
            break
        except ValueError:
            print('Erro! Digite uma das seguintes opções: ')
    print()
    return opcao


def menu_dados(dados, nome):
    #[telefone, morada, CC, data_de_nascimento, sintomas]
    #[tosse, temperatura, dores, cefaleias, fraqueza, dificuldade_respiratoria]
    #['Joel'] [987654321, 'Rua 123', 87654321, datetime.datetime(2001, 11, 14, 0, 0), ['s', 's', 's', 's', 's', 's']]
    #dados = {'Joel': [987654321, 'Rua 123', 87654321, datetime.datetime(2001, 11, 14, 0, 0), ['s', 's', 's', 's', 's', 's']]}
    dado = dados[nome]
    print(f'''Nome: {nome}
Tel: {dado[0]}
Morada: {dado[1]}
CC: {dado[2]}
Data Nasc: {dado[3]}
Sintomas:
- Tosse: {dado[4][0]}
- Febre: {dado[4][1]}
- Dores: {dado[4][2]}
- Cefaleias: {dado[4][3]}
- Fraqueza: {dado[4][4]}
- Dif. respiratória: {dado[4][5]}
Probabilidade Final: {dado[5]:.2f}%
Estado do doente: {dado[6]}''')
    print() 


def menu_consultar_por_doente(dados):
    while True:
        print('-'*9,'CONSULTAR POR DOENTE','-'*9)
        while True:
            nome = str(input('Insira o nome do doente a consultar: ')).title().strip()
            continuar = trycatch_dados(dados, nome)
            if continuar == 0:
                break
            else:
                return
        menu_dados(dados, nome)
        continuar = trycatch_s_n('Deseja consultar outro doente? (s/n) ')
        print()
        if continuar == 'n':
            break


def menu_consultar_por_estado(dados):
    print('-'*7,'CONSULTAR POR ESTADO', '-'*7)
    print('Insira um estado válido para o doente: ')
    while True:
        try:
            estado_do_doente = str(input('Sem Risco; Baixo Risco; Medio Risco; Alto Risco: ')).strip().title()
            if estado_do_doente not in ('Sem Risco', 'Baixo Risco', 'Medio Risco', 'Alto Risco'):
                raise ValueError
            break
        except ValueError:
            print('Erro! Digite um estado dos seguintes estados: ')
    for c in dados: 
        nome = c # vai buscar a chave do diionário 
        if dados[nome][6] == estado_do_doente: # local onde está armazenado o estado do doente
            menu_dados(dados, nome)


def menu_todos_os_doentes(dados):
    print('-'*7,'TODOS OS DOENTES', '-'*7)
    for c in dados:
        nome = c
        menu_dados(dados, nome)


def menu_guardar_dados(dados):
    print('-'*7,'GUARDAR DADOS', '-'*7)
    print('Deseja mesmo guardar os seus dados?(s/n) ')
    guardar = trycatch_s_n('Esta operação irá fazer overwrite a anteriores gravações: ')
    if guardar == 's':
        menu_guardar(dados)
        print('Dados guardados com sucesso!')
    else:
        print('Operação cancelada')
    print()


def menu_guardar(dados):
    with open('dados_pacientes.json', 'w') as dp:
         json.dump(dados, dp)


def menu_carregar_dados(dados):
    print('-'*7,'CARREGAR DADOS', '-'*7)
    dados_json = json.load(open("dados_pacientes.json", 'r'))
    temp_dados = dados_json # armazena numa variávelá parte para não substitutir o que está lá dentro
    for c in temp_dados:
        nome = c
        dados[nome] = temp_dados[nome]
    print('Dados carregados com sucesso!')
    print()
    return dados


def menu_simulacao_UCI():
    print('-'*7,'SIMULAÇÃO DA OCUPAÇÃO UCI', '-'*7)
    try:
        dias = int(input('Introduza o nº de dias da simulação (182 por omissão): ').strip())
    except ValueError:
        dias = 182
    infetados = modsim.State(total_infetados=0, total_curados=0)
    resultados_infetados = modsim.TimeSeries()
    resultados_curados = modsim.TimeSeries()


    def aumento_de_infetados(dias):
        if dias < 60:
            infetados.total_infetados += 4
        elif dias < 100:
            infetados.total_infetados += 3
        else:
            infetados.total_infetados += 2
    
    def aumento_de_curados(dias):
        if dias <60:
            infetados.total_infetados -= 2
            infetados.total_curados += 2
        elif dias < 100:
            infetados.total_infetados -= 3
            infetados.total_curados += 3
        else:
            infetados.total_infetados -= 3
            infetados.total_curados += 3


    def avancaHora(dias):
        if dias < 60:
            if modsim.flip(1):
                aumento_de_infetados(dias)
            if modsim.flip(0.1):
                aumento_de_curados(dias)
        elif dias < 100:
            if modsim.flip(0.6):
                aumento_de_infetados(dias)
            if modsim.flip(0.5) and infetados.total_infetados > 0: # para evitar que haja infetados negativos
                aumento_de_curados(dias)
        else:
            if modsim.flip(0.2):
                aumento_de_infetados(dias)
            if modsim.flip(0.8) and infetados.total_infetados > 0: # para evitar que haja infetados negativos
                aumento_de_curados(dias)


    def correrSimulacao(tempo):
        for dias in range(tempo):
            avancaHora(dias)
            resultados_infetados[dias] = infetados.total_infetados
            resultados_curados[dias] = infetados.total_curados


    def desenhar_infetados():
        modsim.plot(resultados_infetados, label="Simulação")
        modsim.decorate(title='Infetados', xlabel='dias', ylabel='Nº de infetados')
        modsim.plt.show()
    
    
    def desenhar_curados(): #supodo que todos os pacientes que ficam sem covid foram curados
        modsim.plot(resultados_curados, label="Simulação")
        modsim.decorate(title='Curados', xlabel='dias', ylabel='Nº de curados')
        modsim.plt.show()
    
    
    correrSimulacao(dias)
    desenhar_infetados()
    desenhar_curados()


def menu_sair(dados):
    guardar = trycatch_s_n('Pretende guardar os dados antes de sair? (s/n) ')
    if guardar == 's':
        menu_guardar(dados)
    print('FIM!!')


def menu_modificar_sintomas(dados):
    while True:
        print('-'*10,'MODIFICAR SINTOMAS',('-'*10))
        while True:
            nome = str(input('Insira o nome: ')).title().strip()
            continuar = trycatch_dados(dados, nome)
            if continuar == 0:
                break    
            else:
                return
        sintomas = menu_sintomas()
        sintomas,  prob_sintomas = sintomas[:6], sintomas[6] # os sintomas em si só vão até á posição 5 da lista,
        dados[nome][4] = sintomas                            # o outro valor é os 75% que faltam da probabilidade (sintomas).
        prob_etaria = dados[nome][7]
        dados[nome][5] = (prob_etaria + prob_sintomas)*100   
        dados[nome][6] = prob_total_relativa(dados[nome][5])
        continuar = trycatch_s_n('Modificar outro doente? (s/n) ')
        if continuar in 'n':
            break
    print()
    return dados


try:
    dados
except NameError:
    dados = dict()
try:
    while True:
        opcao = menu_principal()
        if opcao == 0:
            menu_sair(dados)
            break
        if opcao == 1:
            dados = menu_novo_doente(dados)
        if opcao == 2:
            menu_modificar_sintomas(dados)
        if opcao == 3:
            menu_testar_doente(dados)
        if opcao == 4:
            menu_remover_doente(dados)
        if opcao == 5:
            while True:
                opcao = menu_consultar_doentes()
                if opcao == 1:
                    menu_consultar_por_doente(dados)
                if opcao == 2:
                    menu_consultar_por_estado(dados)
                if opcao == 3:
                    menu_todos_os_doentes(dados)
                if opcao == 0:
                    break
        if opcao == 6:
            menu_guardar_dados(dados)
        if opcao == 7:
            dados = menu_carregar_dados(dados)
        if opcao == 8:
            menu_simulacao_UCI()
except KeyboardInterrupt:
    print('FIM!!')

# %%

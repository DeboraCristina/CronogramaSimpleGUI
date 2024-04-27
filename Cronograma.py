import json
from PySimpleGUI import TABLE_SELECT_MODE_NONE
from Calendario import *

CRONOGRAMA_JSON = '/home/debby/Ambientes_de_Desenvolvimento/PyCharm/Cronograma/cronograma.json'


def get_semana(inicio_semana: int) -> list:
    dia_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab', 'Dom']
    return dia_semana[inicio_semana:] + dia_semana[:inicio_semana]


def carregar_lista_em_dicionario(semana, valores) -> dict:
    dicionario = {'Seg': '', 'Ter': '', 'Qua': '', 'Qui': '', 'Sex': '', 'Sab': '', 'Dom': ''}
    for i in range(len(valores)):
        dicionario[semana[i]] = valores[i]
    return dicionario


def carregar_dicionario_em_lista(semana, dicionario) -> list:
    valores = ['', '', '', '', '', '', '']
    for i in range(len(dicionario)):
        valores[i] = dicionario[semana[i]]
    return valores


def carregar(semana) -> list:
    try:
        with open(CRONOGRAMA_JSON, 'r') as arquivo:
            dic = json.load(arquivo)
        return carregar_dicionario_em_lista(semana, dic)
    except FileNotFoundError:
        dicionario = {'Seg': '', 'Ter': '', 'Qua': '', 'Qui': '', 'Sex': '', 'Sab': '', 'Dom': ''}
        with open(CRONOGRAMA_JSON, 'w') as arquivo:
            json.dump(dicionario, arquivo)
        print('\033[1;91mArquivo json não encontrado\033[0m')
        return ['', '', '', '', '', '', '']


def salvar(semana, valores: list):
    try:
        dicionario = carregar_lista_em_dicionario(semana, valores)
        with open(CRONOGRAMA_JSON, 'w') as arquivo:
            json.dump(dicionario, arquivo)
        return "Salvo com sucesso!"
    except Exception as e:
        return "Falha ao salvar " + str(e)


def carregar_valores_inputs(win: Pg.Window, valores, semana):
    for i in range(len(semana)):
        key = str(semana[i]).lower()
        index = semana.index(semana[i])
        valor = valores[index] if index < len(valores) else ''
        win[key].update(value=valor)


def preencher_tabela(semana: list, valores: list):
    resultado = []
    for i in range(len(semana)):
        resultado.append([semana[i], valores[i]])
    return resultado


def main():
    Pg.theme('DarkBlue13')
    hoje = datetime.now()

    dia_mes = hoje.weekday()
    semana = get_semana(dia_mes)
    valores = carregar(semana)
    tasks = preencher_tabela(semana, valores)
    width = 640
    height = 450

    ultimo_dia_mes_atual = calendar.monthrange(hoje.year, hoje.month)[1]
    ano, mes = mes_anterior(hoje.year, hoje.month)
    ultimo_dia_mes_anterior = calendar.monthrange(ano, mes)[1]
    inicio_mes = (datetime(hoje.year, hoje.month, 1)).weekday()
    calendario = gen_calendario(hoje.day, ultimo_dia_mes_atual, ultimo_dia_mes_anterior, inicio_mes)

    semana_txt = []
    for dia in semana:
        semana_txt.append(Pg.Text(dia, size=5, text_color='#fff', background_color='#563e8f',
                                  justification='center'))
    calendario.insert(0, semana_txt)

    coluna_calendario = calendario
    t = 5
    coluna_semana_disciplinas = [
        [Pg.T('Seg', size=t, text_color='#fff', background_color='#563e8f', justification='center'),
         Pg.T('Ter', size=t, text_color='#fff', background_color='#563e8f', justification='center'),
         Pg.T('Qua', size=t, text_color='#fff', background_color='#563e8f', justification='center'),
         Pg.T('Qui', size=t, text_color='#fff', background_color='#563e8f', justification='center'),
         Pg.T('Sex', size=t, text_color='#fff', background_color='#563e8f', justification='center'), ],

        [Pg.T('', size=t, text_color='#fff', background_color='#232062', justification='center'),
         Pg.T('IN', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('', size=t, text_color='#fff', background_color='#232062', justification='center'),
         Pg.T('SEG', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('', size=t, text_color='#fff', background_color='#232062', justification='center'),],

        [Pg.T('LBD', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('PL', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('ENG', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('RED', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),
         Pg.T('TS', size=t, text_color='#fff', background_color='#8a3e8f', justification='center'),],
    ]

    coluna_cronograma = [
        [Pg.Table(key='tbl', headings=[' Dia ', '              Tarefa              '],
                  values=tasks, expand_x=True, expand_y=True,
                  alternating_row_color='#232062', justification='center', row_height=22, num_rows=7,
                  hide_vertical_scroll=True, row_colors=[(0, '#563e8f')], #select_mode=TABLE_SELECT_MODE_NONE,
                  enable_events=True)],
        [Pg.Text(key='msg'), Pg.Check(text='On Top', enable_events=True, key='keep', default=True)],
        [Pg.Button(key='salvar', button_text='Salvar', expand_x=True, size=(None, 20))]
    ]
    coluna_config = [
        [Pg.Text('Configurações')],
        [Pg.Column([[Pg.Text('Seg:')], [Pg.Text('Ter:')], [Pg.Text('Qua:')], [Pg.Text('Qui:')], [Pg.Text('Sex:')],
                    [Pg.Text('Sab:')], [Pg.Text('Dom:')]], expand_x=True, expand_y=True, element_justification='left'),
         Pg.Column([[Pg.Input(key='seg', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='ter', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='qua', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='qui', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='sex', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='sab', enable_events=True, size=(10, 1))],
                    [Pg.Input(key='dom', enable_events=True, size=(10, 1))]], expand_x=True, expand_y=True)],
        [Pg.Button(key='limpar', button_text='Limpar', expand_x=True, size=(None, 20))]
    ]
    layout = [
        [Pg.Column(coluna_calendario, justification='center'),
         Pg.Column(coluna_semana_disciplinas, justification='center')],
        [Pg.Column(coluna_cronograma, expand_y=True, key='col_A', element_justification='center',
                   expand_x=True),
         Pg.Column(coluna_config, key='col_B')]
    ]

    win = Pg.Window('Cronograma', keep_on_top=True, layout=layout, #resizable=True,
                    size=(width, height), finalize=True)
    table = win['tbl']
    win.set_min_size((width, height))
    carregar_valores_inputs(win, valores, semana)

    time = 0
    while True:
        event, values = win.read(timeout=1)

        if event == Pg.WIN_CLOSED:
            break

        if event in ['seg', 'ter', 'qua', 'qui', 'sex', 'sab', 'dom']:
            event = str(event)
            index_task = semana.index(event.capitalize())
            valores[index_task] = values[event]
            tasks = preencher_tabela(semana, valores)
            table.update(values=tasks)

        if event == 'keep':
            if values['keep']:
                win.keep_on_top_set()
            else:
                win.keep_on_top_clear()
        if event == 'salvar':
            time = 1500
            msg = salvar(semana, valores)
            win['msg'].update(value=msg)

        if event == 'limpar':
            valores = ['', '', '', '', '', '', '']
            carregar_valores_inputs(win, valores, semana)
            tasks = preencher_tabela(semana, valores)
            table.update(values=tasks)

        if time > 0:
            time -= 1
        if 10 >= time > 0:
            win['msg'].update(value='')

    win.close()


if __name__ == '__main__':
    main()

import PySimpleGUI as Pg
from datetime import datetime
import calendar


def mes_anterior(ano, mes_atual):
    mes = (mes_atual - 1)
    if mes == 0:
        ano -= 1
        mes = 12
    return ano, mes


def gen_calendario(dia_atual, ultimo_dia_mes_atual, ultimo_dia_mes_anterior, inicio_mes):
    meses_anterior = True
    primirio_dia = ultimo_dia_mes_anterior - (inicio_mes - 1)
    if inicio_mes == 0:
        primirio_dia = ultimo_dia_mes_anterior
    if inicio_mes == 7:
        primirio_dia = 1
        meses_anterior = False

    calendario = []
    dia = (primirio_dia - 1)
    valido = 0
    while True:
        semana = []
        if valido != 0:
            valido += 1
        for i in range(7):
            dia += 1
            if dia == (ultimo_dia_mes_anterior + 1) and meses_anterior:
                dia = 1
                meses_anterior = False
            if dia == (ultimo_dia_mes_atual + 1) and not meses_anterior:
                dia = 1
                valido += 1

            cor_texto, cor_fundo = '#fff', '#3e588f'
            if dia == dia_atual:
                cor_texto, cor_fundo = '#ff0', '#8a3e8f'
            if meses_anterior or valido != 0:
                cor_texto, cor_fundo = '#3c00cc', '#232062'

            dia_s = str(dia) if dia > 9 else f'0{str(dia)}'
            semana.append(Pg.Text(dia_s, size=5, text_color=cor_texto, background_color=cor_fundo,
                                  justification='center'))

        calendario.append(semana)

        if valido >= 3:
            break

    return calendario


def gen_layout():
    hoje = datetime.now()
    ultimo_dia_mes_atual = calendar.monthrange(hoje.year, hoje.month)[1]
    ano, mes = mes_anterior(hoje.year, hoje.month)
    ultimo_dia_mes_anterior = calendar.monthrange(ano, mes)[1]
    inicio_mes = (datetime(hoje.year, hoje.month, 1)).weekday()
    calendario = gen_calendario(hoje.day, ultimo_dia_mes_atual, ultimo_dia_mes_anterior, inicio_mes)

    column = calendario

    main_layout = [
        [Pg.Column(column)],
        [Pg.Text('Calendario')]
    ]

    return main_layout


def main():
    layout = gen_layout()

    window = Pg.Window('Calendario', layout, keep_on_top=True, resizable=True)
    while True:
        event, values = window.read()
        if event == Pg.WIN_CLOSED:
            break

    window.close()


if __name__ == '__main__':
    main()

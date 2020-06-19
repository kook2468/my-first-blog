# chart/views.py
from django.shortcuts import render
from .models import Passenger, Covid, Covid_confirmed, Covid_recovered, Covid_deaths
from django.db.models import Count, Q
import json  # ***json 임포트 추가***
import datetime
from django.http import JsonResponse  # for chart_data()
from django.core.serializers.json import DjangoJSONEncoder
import pandas as pd


def home(request):
    return render(request, 'home.html')


def covid_19(request):
    # 데이터 가져오기
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                     parse_dates=['Date'])
    # 분석 대상 국가에 해당하는 행만 선별
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    # 합계 열 생성
    df['Cases'] = df[['Confirmed', 'Recovered', 'Deaths']].sum(axis=1)
    # df['Cases'] = df[['Confirmed']].sum(axis=1)
    # 데이터 재구조화
    df = df.pivot(index='Date', columns='Country', values='Cases')
    # countries 리스트 생성
    countries = list(df.columns)
    # 기존 인덱스 열을 데이터 열로 변경
    covid = df.reset_index('Date')
    # covid 인덱스와 columns를 새로 지정
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    # 인구 대비 건수 계산 (건/백만명)
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.to_csv("covid19.csv", header=True, index=True)

    # DB에서 불러오기
    dataset = Covid.objects.values()

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    france_series_data = list()  # for series named 'Survived'
    germany_series_data = list()
    korea_series_data = list()  # for series named 'Not survived'
    us_series_data = list()
    uk_series_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append(entry['date'])  # for xAxis
        france_series_data.append(entry['france'])  # for series named 'Survived'
        germany_series_data.append(entry['germany'])
        korea_series_data.append(entry['korea'])  # for series named 'Not survived'
        us_series_data.append(entry['us'])
        uk_series_data.append(entry['uk'])

    france_series = {
        'name': 'France',
        'data': france_series_data,
        'color': 'green'
    }
    germany_series = {
        'name': 'Germany',
        'data': germany_series_data,
        'color': 'blue'
    }
    korea_series = {
        'name': 'Korea, South',
        'data': korea_series_data,
        'color': 'red'
    }
    us_series = {
        'name': 'US',
        'data': us_series_data,
        'color': 'orange'
    }
    uk_series = {
        'name': 'United Kingdom',
        'data': uk_series_data,
        'color': 'brown'
    }

    json_date = list()
    for d in categories:
        json_date.append(d.strftime('%e. %b'))

    chart = {
        # 'chart': {'type': 'column'},
        'chart': {
            'borderColor': '#ddd',
            'borderWidth': 3
        },
        'title': {'text': 'Covid-19 확진자,회복자,사망자 발생율'},
        'subtitle': {'text': 'Source: https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'},
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
        'xAxis': {
            'categories': json_date,
            'tickInterval': 14
        },
        'yAxis': {
            'title': {
                'text': '합계 건수'
            },
            'labels': {
                'format': '{value}/백만명'
            }
        },
        'series': [france_series, germany_series, korea_series, us_series, uk_series]
    }
    dump = json.dumps(chart)

    return render(request, 'covid_19.html', {'chart': dump})


def covid_confirmed(request):
    # 데이터 가져오기
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                     parse_dates=['Date'])
    # 분석 대상 국가에 해당하는 행만 선별
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    # 합계 열 생성
    df['Cases'] = df[['Confirmed']].sum(axis=1)

    # 데이터 재구조화
    df = df.pivot(index='Date', columns='Country', values='Cases')
    # countries 리스트 생성
    countries = list(df.columns)
    # 기존 인덱스 열을 데이터 열로 변경
    covid = df.reset_index('Date')
    # covid 인덱스와 columns를 새로 지정
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    # 인구 대비 건수 계산 (건/백만명)
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.to_csv("covid_confirmed.csv", header=True, index=True)

    # DB에서 불러오기
    dataset = Covid_confirmed.objects.values()

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    france_series_data = list()  # for series named 'Survived'
    germany_series_data = list()
    korea_series_data = list()  # for series named 'Not survived'
    us_series_data = list()
    uk_series_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append(entry['date'])  # for xAxis
        france_series_data.append(entry['france'])  # for series named 'Survived'
        germany_series_data.append(entry['germany'])
        korea_series_data.append(entry['korea'])  # for series named 'Not survived'
        us_series_data.append(entry['us'])
        uk_series_data.append(entry['uk'])

    france_series = {
        'name': 'France',
        'data': france_series_data,
        'color': 'green'
    }
    germany_series = {
        'name': 'Germany',
        'data': germany_series_data,
        'color': 'blue'
    }
    korea_series = {
        'name': 'Korea, South',
        'data': korea_series_data,
        'color': 'red'
    }
    us_series = {
        'name': 'US',
        'data': us_series_data,
        'color': 'orange'
    }
    uk_series = {
        'name': 'United Kingdom',
        'data': uk_series_data,
        'color': 'brown'
    }

    json_date = list()
    for d in categories:
        json_date.append(d.strftime('%e. %b'))

    chart = {
        # 'chart': {'type': 'column'},
        'chart': {
            'borderColor': '#ddd',
            'borderWidth': 3
        },
        'title': {'text': 'Covid-19 확진자 발생율'},
        'subtitle': {
            'text': 'Source: https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'},
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
        'xAxis': {
            'categories': json_date,
            'tickInterval': 14
        },
        'yAxis': {
            'title': {
                'text': '합계 건수'
            },
            'labels': {
                'format': '{value}/백만명'
            }
        },
        'series': [france_series, germany_series, korea_series, us_series, uk_series]
    }
    dump = json.dumps(chart)

    return render(request, 'covid_confirmed.html', {'chart': dump})


def covid_recovered(request):
    # 데이터 가져오기
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                     parse_dates=['Date'])
    # 분석 대상 국가에 해당하는 행만 선별
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    # 합계 열 생성
    df['Cases'] = df[['Recovered']].sum(axis=1)

    # 데이터 재구조화
    df = df.pivot(index='Date', columns='Country', values='Cases')
    # countries 리스트 생성
    countries = list(df.columns)
    # 기존 인덱스 열을 데이터 열로 변경
    covid = df.reset_index('Date')
    # covid 인덱스와 columns를 새로 지정
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    # 인구 대비 건수 계산 (건/백만명)
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.to_csv("covid_recovered.csv", header=True, index=True)

    # DB에서 불러오기
    dataset = Covid_recovered.objects.values()

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    france_series_data = list()  # for series named 'Survived'
    germany_series_data = list()
    korea_series_data = list()  # for series named 'Not survived'
    us_series_data = list()
    uk_series_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append(entry['date'])  # for xAxis
        france_series_data.append(entry['france'])  # for series named 'Survived'
        germany_series_data.append(entry['germany'])
        korea_series_data.append(entry['korea'])  # for series named 'Not survived'
        us_series_data.append(entry['us'])
        uk_series_data.append(entry['uk'])

    france_series = {
        'name': 'France',
        'data': france_series_data,
        'color': 'green'
    }
    germany_series = {
        'name': 'Germany',
        'data': germany_series_data,
        'color': 'blue'
    }
    korea_series = {
        'name': 'Korea, South',
        'data': korea_series_data,
        'color': 'red'
    }
    us_series = {
        'name': 'US',
        'data': us_series_data,
        'color': 'orange'
    }
    uk_series = {
        'name': 'United Kingdom',
        'data': uk_series_data,
        'color': 'brown'
    }

    json_date = list()
    for d in categories:
        json_date.append(d.strftime('%e. %b'))

    chart = {
        # 'chart': {'type': 'column'},
        'chart': {
            'borderColor': '#ddd',
            'borderWidth': 3
        },
        'title': {'text': 'Covid-19 회복자 발생율'},
        'subtitle': {
            'text': 'Source: https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'},
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
        'xAxis': {
            'categories': json_date,
            'tickInterval': 14
        },
        'yAxis': {
            'title': {
                'text': '합계 건수'
            },
            'labels': {
                'format': '{value}/백만명'
            }
        },
        'series': [france_series, germany_series, korea_series, us_series, uk_series]
    }
    dump = json.dumps(chart)

    return render(request, 'covid_recovered.html', {'chart': dump})


def covid_deaths(request):
    # 데이터 가져오기
    df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv',
                     parse_dates=['Date'])
    # 분석 대상 국가에 해당하는 행만 선별
    countries = ['Korea, South', 'Germany', 'United Kingdom', 'US', 'France']
    df = df[df['Country'].isin(countries)]

    # 합계 열 생성
    df['Cases'] = df[['Deaths']].sum(axis=1)

    # 데이터 재구조화
    df = df.pivot(index='Date', columns='Country', values='Cases')
    # countries 리스트 생성
    countries = list(df.columns)
    # 기존 인덱스 열을 데이터 열로 변경
    covid = df.reset_index('Date')
    # covid 인덱스와 columns를 새로 지정
    covid.set_index(['Date'], inplace=True)
    covid.columns = countries

    # 인구 대비 건수 계산 (건/백만명)
    populations = {'Korea, South': 51269185, 'Germany': 83783942, 'United Kingdom': 67886011, 'US': 331002651,
                   'France': 65273511}
    percapita = covid.copy()
    for country in list(percapita.columns):
        percapita[country] = percapita[country] / populations[country] * 1000000

    percapita.to_csv("covid_deaths.csv", header=True, index=True)

    # DB에서 불러오기
    dataset = Covid_deaths.objects.values()

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    france_series_data = list()  # for series named 'Survived'
    germany_series_data = list()
    korea_series_data = list()  # for series named 'Not survived'
    us_series_data = list()
    uk_series_data = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append(entry['date'])  # for xAxis
        france_series_data.append(entry['france'])  # for series named 'Survived'
        germany_series_data.append(entry['germany'])
        korea_series_data.append(entry['korea'])  # for series named 'Not survived'
        us_series_data.append(entry['us'])
        uk_series_data.append(entry['uk'])

    france_series = {
        'name': 'France',
        'data': france_series_data,
        'color': 'green'
    }
    germany_series = {
        'name': 'Germany',
        'data': germany_series_data,
        'color': 'blue'
    }
    korea_series = {
        'name': 'Korea, South',
        'data': korea_series_data,
        'color': 'red'
    }
    us_series = {
        'name': 'US',
        'data': us_series_data,
        'color': 'orange'
    }
    uk_series = {
        'name': 'United Kingdom',
        'data': uk_series_data,
        'color': 'brown'
    }

    json_date = list()
    for d in categories:
        json_date.append(d.strftime('%e. %b'))

    chart = {
        # 'chart': {'type': 'column'},
        'chart': {
            'borderColor': '#ddd',
            'borderWidth': 3
        },
        'title': {'text': 'Covid-19 회복자 발생율'},
        'subtitle': {
            'text': 'Source: https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv'},
        'legend': {
            'layout': 'vertical',
            'align': 'right',
            'verticalAlign': 'middle'
        },
        'xAxis': {
            'categories': json_date,
            'tickInterval': 14
        },
        'yAxis': {
            'title': {
                'text': '합계 건수'
            },
            'labels': {
                'format': '{value}/백만명'
            }
        },
        'series': [france_series, germany_series, korea_series, us_series, uk_series]
    }
    dump = json.dumps(chart)

    return render(request, 'covid_deaths.html', {'chart': dump})


def world_population(request):
    return render(request, 'world_population.html')

def ticket_class_view_1(request):  # 방법 1
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(
            survived_count=Count('ticket_class',
                                 filter=Q(survived=True)),
            not_survived_count=Count('ticket_class',
                                     filter=Q(survived=False))) \
        .order_by('ticket_class')
    return render(request, 'ticket_class_1.html', {'dataset': dataset})



def ticket_class_view_2(request):  # 방법 2
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비
    categories = list()  # for xAxis
    survived_series = list()  # for series named 'Survived'
    not_survived_series = list()  # for series named 'Not survived'
    survival_rate = list()

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series.append(entry['not_survived_count'])  # for series named 'Not survived'3
        survival_rate.append(entry['survived_count'] / (entry['survived_count'] + entry['not_survived_count']) * 100)


    # json.dumps() 함수로 리스트 3종을 JSON 데이터 형식으로 반환
    return render(request, 'ticket_class_2.html', {
        'categories': json.dumps(categories),
        'survived_series': json.dumps(survived_series),
        'not_survived_series': json.dumps(not_survived_series),
        'survival_rate': json.dumps(survival_rate)
    })


def ticket_class_view_3(request):  # 방법 3
    dataset = Passenger.objects \
        .values('ticket_class') \
        .annotate(survived_count=Count('ticket_class', filter=Q(survived=True)),
                  not_survived_count=Count('ticket_class', filter=Q(survived=False))) \
        .order_by('ticket_class')

    # 빈 리스트 3종 준비 (series 이름 뒤에 '_data' 추가)
    categories = list()  # for xAxis
    survived_series_data = list()  # for series named 'Survived'
    not_survived_series_data = list()  # for series named 'Not survived'

    # 리스트 3종에 형식화된 값을 등록
    for entry in dataset:
        categories.append('%s Class' % entry['ticket_class'])  # for xAxis
        survived_series_data.append(entry['survived_count'])  # for series named 'Survived'
        not_survived_series_data.append(entry['not_survived_count'])  # for series named 'Not survived'

    survived_series = {
        'name': 'Survived',
        'data': survived_series_data,
        'color': 'green'
    }
    not_survived_series = {
        'name': 'Not Survived',
        'data': not_survived_series_data,
        'color': 'red'
    }

    chart = {
        'chart': {'type': 'column'},
        'title': {'text': 'Titanic Survivors by Ticket Class'},
        'xAxis': {'categories': categories},
        'series': [survived_series, not_survived_series]
    }
    dump = json.dumps(chart)

    return render(request, 'ticket_class_3.html', {'chart': dump})


def json_example(request):  # 접속 경로 'json-example/'에 대응하는 뷰
    return render(request, 'json_example.html')


def chart_data(request):  # 접속 경로 'json-example/data/'에 대응하는 뷰
    dataset = Passenger.objects \
        .values('embarked') \
        .exclude(embarked='') \
        .annotate(total=Count('id')) \
        .order_by('-total')
    #  [
    #    {'embarked': 'S', 'total': 914}
    #    {'embarked': 'C', 'total': 270},
    #    {'embarked': 'Q', 'total': 123},
    #  ]

    # # 탑승_항구 상수 정의
    # CHERBOURG = 'C'
    # QUEENSTOWN = 'Q'
    # SOUTHAMPTON = 'S'
    # PORT_CHOICES = (
    #     (CHERBOURG, 'Cherbourg'),
    #     (QUEENSTOWN, 'Queenstown'),
    #     (SOUTHAMPTON, 'Southampton'),
    # )
    port_display_name = dict()
    for port_tuple in Passenger.PORT_CHOICES:
        port_display_name[port_tuple[0]] = port_tuple[1]
    # port_display_name = {'C': 'Cherbourg', 'Q': 'Queenstown', 'S': 'Southampton'}

    chart = {
        'chart': {'type': 'pie'},
        'title': {'text': 'Number of Titanic Passengers by Embarkation Port'},
        'series': [{
            'name': 'Embarkation Port',
            'data': list(map(
                lambda row: {'name': port_display_name[row['embarked']], 'y': row['total']},
                # row 라는 매개변수를 받아 딕셔너리의 형태로 저장을 하겠다.
                # map(람다함수, dataset) →설명: map(함수, 리스트) → 리스트에서 원소를 하나씩 꺼내서 함수를 적용시킨 다음 그 결과를 새로운 리스트에 담아줌
                dataset))
            # 'data': [ {'name': 'Southampton', 'y': 914},
            #           {'name': 'Cherbourg', 'y': 270},
            #           {'name': 'Queenstown', 'y': 123}]
        }]
    }
    # [list(map(lambda))](https://wikidocs.net/64)

    return JsonResponse(chart)

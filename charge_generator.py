import numpy as np
from scipy.stats import burr12, t, weibull_min, gamma
import matplotlib.pyplot as plt
import json, codecs
from hurst import random_walk

def web_charge(tempoDeSerie: int, numberOfCharges: int = 1, init_time: float = 0) -> None:
    """
    Geração carga web considerando a modelagem On-Off
    \nParâmetros:
    tempoDeSerie: Tempo de duracao da carga em segundos
    numberOfCharges: número de cargas a serem geradas
    """

    for k in range(numberOfCharges):
        sequanciaDeMensagens = list()
        tempoEntreMensagens = list()
        tempo = 0
        while tempo <= tempoDeSerie:
            numeroDeObjetosPrincipais = int(np.random.lognormal(0.473844, 0.688471))
            tamanhoObjetosPrincipais = numeroDeObjetosPrincipais*[0]
            j = 0
            for i in weibull_min.rvs(0.814944, scale=28242.8, size=numeroDeObjetosPrincipais):
                tamanhoObjetosPrincipais[j] = int(i)
                j += 1
            sequanciaDeMensagens += tamanhoObjetosPrincipais
            tempoEntreMensagens += numeroDeObjetosPrincipais*[0.0]
            # print(numeroDeObjetosPrincipais, tamanhoObjetosPrincipais)
            numeroObjetosSecundarios = int(np.random.exponential(31.92))
            tamanhoObjetosSecundarios = numeroObjetosSecundarios * [0]
            j = 0
            for i in np.random.lognormal(9.17979, 1.24646, size=numeroObjetosSecundarios):
                tamanhoObjetosSecundarios[j] = int(i)
                j += 1
            sequanciaDeMensagens += tamanhoObjetosSecundarios
            tempoEntreObjetosSecundarios = gamma.rvs(0.16, scale=5.375, size=numeroObjetosSecundarios)
            for i in tempoEntreObjetosSecundarios:
                tempo += i
            tempoEntreMensagens += tempoEntreObjetosSecundarios.tolist()
            toff = np.random.lognormal(-0.495204, 2.7731)
            # if (tempo + toff) < tempoDeSerie:
            tempoEntreMensagens.append(toff)
            sequanciaDeMensagens.append(0)
            tempo += toff
            # print('numeroObjetosSecundarios', numeroObjetosSecundarios, '\ntamanhoObjetosSecundarios', tamanhoObjetosSecundarios, '\ntempoEntreObjetosSecundarios', tempoEntreObjetosSecundarios, '\ntoff', toff)

        app = {
            "init_time": init_time,
            "server_port": 80,
            "packet_size": sequanciaDeMensagens,
            "time_between_packets": tempoEntreMensagens,
            "duration": int(tempo)
        }
        file_path = "./Charges/web_charge{}.json".format(k)
        json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)

    #     series = random_walk(tempoDeSerie, proba=0.3, cumprod=True)
    #     a = min(series)
    #     for idx, _ in enumerate(series):
    #         series[idx] -= a
    #         series[idx] *= 1000
    #     app = {
    #         "init_time": np.random.uniform(high=86400),
    #         "server_port": 82,
    #         "series": series
    #     }
    #     listOfCharges.append(app)

    # file_path = "./Charges/web_charge.json"
    # json.dump(listOfCharges, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)

def video_stream_charge(tempoVideo: int, video_code: int, numeroDeCargas: int = 1, init_time: list = [0.0]) -> None:
    """ 
    Geração de carga de trabalho de Vídeo Sob Demanda (VoD)
    \nParêmetros:
    tempoVideo: Tempo esperado de vídeo. Se numeroDeCargas não for especificado
    uma carga de tamanho tempoVideo será gerado. Do contrário tempoVideo é usado
    como valor médio de uma distribuição normal com desvio padrão = 5 (s)\n
    video_code: Taxa de codificação de vídeo (bits/s)
    numeroDeCargas: Numero de cargas a serem geradas
    """
    # Time_downloading gerado atraves da distribuicao Burr tipo 12
    # timeInterRequests gerado atraves da distribuicao Normal
    # Tempo de cada segmento de 2 segundos de acordo com [1]
    # Desvio de tempo medio de 5 segundos
    segmentTime = 2

    # if numeroDeCargas == 1:
    #     tempoVideoList.append(tempoVideo)
    # else:
    #     tempoVideoList = np.random.normal(tempoVideo, tempoVideoMedioDev, numeroDeCargas).tolist()
    for k in range(numeroDeCargas):
        numberOfSegments = int(tempoVideo/segmentTime)

        time_downloading = burr12.rvs(scale=1.469, d=1.915, c=3.014, size=numberOfSegments+1).tolist()
        for i in range(len(time_downloading)):
            time_downloading[i] = int(video_code*time_downloading[i])

        timeInterRequests = [0.0] + t.rvs(loc=1.938, scale=0.245, df=2.086, size=numberOfSegments).tolist()
        for i in range(len(timeInterRequests)):
            if timeInterRequests[i] < 0:
                # Nao pode haver tempo entre segmentos negativos
                timeInterRequests[i] = t.rvs(loc=1.938, scale=0.245, df=2.086)
                # Fica no loop até achar um número nao negativo
                while timeInterRequests[i] < 0:
                    timeInterRequests[i] = t.rvs(loc=1.938, scale=0.245, df=2.086)

        app = {
            "init_time": init_time[k],
            "server_port": 81,
            "packet_size": time_downloading,
            "time_between_packets": timeInterRequests,
            "duration": int(tempoVideo)
        }

        # app = {
        #     "init_time": np.random.uniform(high=86400),
        #     "server_port": 81,
        #     "segment_time": segmentTime,
        #     "video_codification": video_code,
        #     "video_time": 2*numberOfSegments,
        #     "time_between_segments": timeInterRequests,
        #     "time_downloading":time_downloading
        # }

        file_path = "./Charges/stream_charge{}.json".format(k)
        json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)


def voip_charge ( callDuration: int, numeroDeCargas: int = 1, tempo: list = [0.0] ) -> list:
    """
    Geração de carga de trabalho de Voz sobre IP (VoIP)
    \nParametros:
    callDuration: Duração de uma determinada ligação. Se numeroDeCargas
    não for especificado, callDuration será a média de uma distribuição de Pareto
    tipo 2.
    numeroDeCargas: Numero de cargas a serem geradas
    """

    # Tempo entre geração de pacotes modelado como uma distribuição 
    # normal com média 0.02 e desvio 0.0038 segundos
    time_between_packets = 0.02
    time_between_packets_dev = 0.0038

    # call_duration_list = list()
    # if numeroDeCargas != 1:
    #     call_duration_list = np.random.pareto(2.5, numeroDeCargas) + 0.5
    #     # call_duration_list = np.random.pareto(3.0, numeroDeCargas)
    #     call_duration_list = [callDuration*x for x in call_duration_list]
    # else:
    #     call_duration_list.append(callDuration)

    # listOfCharges = list()
    for j in range(numeroDeCargas):

        numberOfPackets = int( callDuration / time_between_packets )
        sequenceOfPackets = [0.0] + np.random.normal(time_between_packets, time_between_packets_dev, numberOfPackets).tolist()
        # sequenceOfPackets = sequenceOfPackets.tolist()

        # Tempo de inicialização uniformemente distribuído ao longo do dia
        app = {
            "init_time": tempo[j],
            "server_port": 80,
            "packet_size": 20,
            "time_between_packets": sequenceOfPackets,
            "call_duration": callDuration
        }

        # listOfCharges.append(app)

        file_path = "./Charges/voip_charge{}.json".format(552+j)
        json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)
    # return listOfCharges


def iot_charge(tempoTotal: int, tamanhoDeMensagem: int, numeroDeDispositivos: int) -> list:
    """
    Modelagem segue uma distribuição periódica de mensagens com período inicial de geração 
    segundo uma distribuição uniforme [0:1]. Em [4] recomenda-se uma quantidade de nós acima
    de 10000 para diminuir o erro dos tempos entre duas mensagens.
    Parâmetros: 
    tempoTotal: tempo em segundos no qual os "dispositivos" realizam transmissões.
    numeroDeDispositivos: número de dispositivos que "compõem" a rede.
    tamanhoDeMensagem: tamanho em bytes das mensagens que compõe o fluxo.
    """

    tempoEntreMensagens = sorted(np.random.uniform(size=numeroDeDispositivos).tolist())
    # Mantem a periodicidade das transmissões
    tempoEntreMensagens = tempoEntreMensagens*tempoTotal

    # Fazer os ajustes de tempo
    i = 0
    while i < tempoTotal:
        j = 0
        while j < numeroDeDispositivos:
            tempoEntreMensagens[ i*numeroDeDispositivos + j ] += i
            j+=1
        i+=1

    app = {
        "init_time": 0.0,
        "server_port": 79,
        "packet_size": tamanhoDeMensagem,
        "time_to_send": tempoEntreMensagens,
    }

    file_path = "./Charges/IOT_charge.json"
    json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), indent=4)
    return app

if __name__ == "__main__":
    # voip_charge(20)

    # Tempo médio de vídeo de 4 minutos e 20 segundos = 260
    # https://www.minimatters.com/youtube-best-video-length/
    # n_stream_load = 40
    # init_time = np.random.uniform(0, 86400-260, n_stream_load)
    # video_stream_charge(260, 2058000, n_stream_load, init_time)

    # 
    n_voip_load = 2
    init_time_voip = np.random.uniform(0, 86400-144, n_voip_load)
    voip_charge(181, n_voip_load, init_time_voip)

    # web_charge(86400, 7)
    # iot_charge(5, 50, 3)

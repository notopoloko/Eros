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
        tempo = 0.0
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

        # Ajusta o tempo de carga
        pseudoTime = 0.0
        for i in range(len(tempoEntreMensagens)):
            pseudoTime += tempoEntreMensagens[i]
            if pseudoTime >= tempoDeSerie:
                # Time to cut
                tempoEntreMensagens = tempoEntreMensagens[:i+1]
                sequanciaDeMensagens = sequanciaDeMensagens[:i+1]
                tempo = pseudoTime
                break

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


def voip_charge ( callDuration: int, numeroDeCargas: int = 1, tempo: list = [0.0], voipCodec: int = 0 ) -> None:
    """
    Geração de carga de trabalho de Voz sobre IP (VoIP)
    \nParametros:
    callDuration: Duração de uma determinada ligação. Se numeroDeCargas
    não for especificado, callDuration será a média de uma distribuição de Pareto
    tipo 2.
    numeroDeCargas: Numero de cargas a serem geradas
    tempo: Tempo das cargas
    voipCodec: 
        0 -> G.729 8 kbps
        1 -> G.729 6.4 kbps
        2 -> G.711
        3 -> SILK
        4 -> iSAC
    """
    cbrMessageSize = [20, 16, 214]
    cbrDevNormalDistribution = [0.0038, 0.0038, 0.0047]

    vbrMeanNormalDistribution = [0.02, 0.03]
    vbrDevNormalDistribution = [0.0070, 0.0022]
    vbrARMAParams = [[0.281, -0.332, -0.600],[0.117, -0.190, -0.631]]
    
    if voipCodec == 0 or voipCodec == 1 or voipCodec == 2:
        # G.729 ou G.711
        time_between_packets = 0.02
        time_between_packets_dev = cbrDevNormalDistribution[voipCodec]
        messageSize = cbrMessageSize[voipCodec]

        for j in range(numeroDeCargas):
            numberOfPackets = int( callDuration / time_between_packets )
            sequenceOfPackets = np.random.normal(time_between_packets, time_between_packets_dev, numberOfPackets).tolist()

            app = {
                "init_time": tempo[j],
                "server_port": 5060,
                "packet_size": messageSize,
                "time_between_packets": sequenceOfPackets,
                "call_duration": callDuration
            }
            file_path = "./Charges/voip_charge{}.json".format(j)
            json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)
        return
    elif voipCodec == 3 or voipCodec == 4:
        # SILK ou iSAC
        time_between_packets = vbrMeanNormalDistribution[voipCodec - 3]
        time_between_packets_dev = vbrDevNormalDistribution[voipCodec - 3]

        for j in range(numeroDeCargas):
            numberOfPackets = int( callDuration / time_between_packets )
            sequenceOfPackets = np.random.normal(time_between_packets, time_between_packets_dev, numberOfPackets).tolist()

            # Gera o tamanho das mensagens
            messageSize = [0] * numberOfPackets
            whiteNoise = [0.0] + np.random.normal(0, 22, numberOfPackets).tolist()
            loopBack = [0.0]*3
            for i in range(numberOfPackets):
                loopBack[0] = loopBack[1]
                loopBack[1] = loopBack[2]
                loopBack[2] = 159 + whiteNoise[i + 1] + vbrARMAParams[voipCodec-3][0] * loopBack[1] + vbrARMAParams[voipCodec-3][1] * loopBack[0] + vbrARMAParams[voipCodec-3][2] * whiteNoise[i]
                messageSize[i] = int(loopBack[2])

            app = {
                "init_time": tempo[j],
                "server_port": 5060,
                "packet_size": messageSize,
                "time_between_packets": sequenceOfPackets,
                "call_duration": callDuration
            }
            file_path = "./Charges/voip_charge{}.json".format(j)
            json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)


def iot_charge(tempoTotal: int, tamanhoDeMensagem: int, numeroDeDispositivos: int, periodoDasMesagens: int, numeroDeCargas: int = 1) -> None:
    """
    Modelagem segue uma distribuição periódica de mensagens com período inicial de geração 
    segundo uma distribuição uniforme [0:T]. Em [4] recomenda-se uma quantidade de nós acima
    de 10000 para diminuir o erro dos tempos entre duas mensagens.
    Parâmetros: 
    tempoTotal: tempo em segundos no qual os "dispositivos" realizam transmissões.
    numeroDeDispositivos: número de dispositivos que "compõem" a rede.
    tamanhoDeMensagem: tamanho em bytes das mensagens que compõe o fluxo.
    """
    for j in range(numeroDeCargas):
        tempoEntreMensagens = sorted(np.random.uniform(high=periodoDasMesagens, size=numeroDeDispositivos).tolist())
    
        # Calcula a diferenca de tempo entre duas mensagens
        for i in range(1, len(tempoEntreMensagens) - 1):
            tempoEntreMensagens[i] = tempoEntreMensagens[i+1] - tempoEntreMensagens[i]
        tempoEntreMensagens[-1] = periodoDasMesagens - tempoEntreMensagens[-1]

        # Torna o processo cíclico
        totalTime = 0
        for i in tempoEntreMensagens:
            totalTime += i
        tempoEntreMensagens[-1] += periodoDasMesagens + tempoEntreMensagens[0] - totalTime

        # Mantem a periodicidade das transmissões
        if int(tempoTotal/periodoDasMesagens) == 0:
            tempoEntreMensagens = tempoEntreMensagens * 1
        else:
            tempoEntreMensagens = [0.0] + tempoEntreMensagens * int(tempoTotal/periodoDasMesagens)

        # Faz um corte no tempo exato
        pseudoTempo = 0
        for i in range(len(tempoEntreMensagens)):
            pseudoTempo += tempoEntreMensagens[i]
            if pseudoTempo > tempoTotal:
                tempoEntreMensagens = tempoEntreMensagens[:i]
                break

        app = {
            "init_time": 0.0,
            "server_port": 79,
            "packet_size": tamanhoDeMensagem,
            "time_between_packets": tempoEntreMensagens,
        }

        file_path = "./Charges/IOT_charge{}.json".format(j)
        json.dump(app, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), indent=4)

# if __name__ == "__main__":
    # voip_charge(20)

    # Tempo médio de vídeo de 4 minutos e 20 segundos = 260
    # https://www.minimatters.com/youtube-best-video-length/
    # n_stream_load = 40
    # init_time = np.random.uniform(0, 86400-260, n_stream_load)
    # video_stream_charge(260, 2058000, n_stream_load, init_time)

    # 
    # n_voip_load = 2
    # init_time_voip = np.random.uniform(0, 86400-144, n_voip_load)
    # voip_charge(181, n_voip_load, init_time_voip)

    # web_charge(86400, 7)

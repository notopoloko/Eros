import numpy as np
from scipy.stats import burr12, t, weibull_min
import matplotlib.pyplot as plt
import json, codecs
from hurst import random_walk

def web_charge(tempoDeSerie, numberOfCharges=1):

    # number_of_main_objects = int(np.random.lognormal(0.473844, 0.688471)) + 1

    # main_object_size = weibull_min.rvs(0.814944, loc=0, scale=28242.8, size=number_of_main_objects)

    # main_object_size = [int(x) for x in main_object_size]

    # number_of_inline_objects = int(np.random.exponential(31.9291))

    # inline_object_size = (np.random.lognormal(9.17979, 1.24646, number_of_inline_objects))
    # inline_object_size = [int(x) for x in inline_object_size]

    # time_reading = (np.random.lognormal(-0.495204, 2.7731, number_of_requests)*39.7).tolist()

    # app = {
    #     "server_port": 82,
    #     "main_object_size": main_object_size,
    #     "number_of_main_objects": number_of_main_objects,
    #     "inline_object_size": inline_object_size,
    #     "number_of_inline_objects": number_of_inline_objects,
    #     "time_reading": time_reading
    # }
    listOfCharges = list()

    for i in range(numberOfCharges):
        series = random_walk(tempoDeSerie, proba=0.3)
        a = min(series)
        for idx, val in enumerate(series):
            series[idx] -= a
        app = {
            "init_time": 0.0,
            "server_port": 82,
            "series": series
        }
        listOfCharges.append(app)

    file_path = "./Charges/web_charge.json"
    json.dump(listOfCharges, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)

def video_stream_charge(tempoVideo, video_code, numeroDeCargas = 1):
    # time_downloading gerado atraves da distribuicao Burr tipo 12
    # timeInterRequests gerado atraves da distribuicao Normal
    # Tempo de cada segmento de 2 segundos de acordo com [1]
    # Desvio de tempo medio de 5 segundos
    segmentTime = 2
    tempoVideoMedioDev = 5
    tempoVideoList = list()
    listOfCharges = list()

    if numeroDeCargas == 1:
        tempoVideoList.append(tempoVideo)
    else:
        tempoVideoList = np.random.normal(tempoVideo, tempoVideoMedioDev, numeroDeCargas).tolist()

    for i in range(numeroDeCargas):
        numberOfSegments = int(tempoVideoList[i]/segmentTime)

        time_downloading = burr12.rvs(scale=1.469, d=1.915, c=3.014, size=numberOfSegments+1).tolist()

        timeInterRequests = t.rvs(loc=1.932, scale=0.245, df=2.086, size=numberOfSegments).tolist()

        app = {
            "init_time": 0.0,
            "server_port": 81,
            "segment_time": segmentTime,
            "video_codification": video_code,
            "video_time": 2*numberOfSegments,
            "time_between_segments": timeInterRequests,
            "time_downloading":time_downloading
        }
        listOfCharges.append(app)

    file_path = "./Charges/stream_charge.json"
    json.dump(listOfCharges, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)


def voip_charge( call_duration, numeroDeCargas = 1 ):
    time_between_packets = 0.02
    time_between_packets_dev = 0.0038

    call_duration_list = list()
    if numeroDeCargas != 1:
        call_duration_list = np.random.pareto(2.5, numeroDeCargas) + 0.5
        # call_duration_list = np.random.pareto(3.0, numeroDeCargas)
        call_duration_list = [call_duration*x for x in call_duration_list]
    else:
        call_duration_list.append(call_duration)

    # modelagem para tempo entre mais de uma ligacao (descartado)
    # inter_call_interval = np.random.exponential(0.84, numberOfCalls)
    # inter_call_interval = [1.125*x for x in inter_call_interval]
    # for i in range(1, len(inter_call_interval)):
    #     inter_call_interval[i] = inter_call_interval[i] + inter_call_interval[i-1]

    listOfCharges = list()
    for j in range(numeroDeCargas):

        numberOfPackets = int( call_duration_list[j] / time_between_packets )
        sequenceOfPackets = np.random.normal(time_between_packets, time_between_packets_dev, numberOfPackets)

        # for i in range(1, numberOfPackets):
        #     sequenceOfPackets[i] = sequenceOfPackets[i] + sequenceOfPackets[i-1]
        sequenceOfPackets = sequenceOfPackets.tolist()

        # modelagem de taxa media de geracao (descartado)
        # averageRate = [0]*(int(sequenceOfPackets[len(sequenceOfPackets) - 1]) + 1)
        # for i in sequenceOfPackets:
        #     averageRate[int(i)]+=160
        # f = open('averageRate.txt', 'w')
        # f.write(str(averageRate))
        # f.close()

        app = {
            "init_timw":0.0,
            "server_port": 80,
            "packet_size": 20,
            "time_between_packets": sequenceOfPackets,
            "call_duration": call_duration_list[j]
        }

        listOfCharges.append(app)

    # separators=(',', ':')

    file_path = "./Charges/voip_charge.json"
    json.dump(listOfCharges, codecs.open(file_path, 'w', encoding='utf-8'), indent=4)


def iot_charge(tamanhoMedioDePacote, numberOfCharges, tempoEntreMensagem):

    assert tempoEntreMensagem < 1440 and tempoEntreMensagem > 0

    numeroDeMensagens = 1440//tempoEntreMensagem

    chargeList = list()

    while numberOfCharges != 0:
        time_to_send = np.random.normal(tempoEntreMensagem, tempoEntreMensagem/18, numeroDeMensagens).tolist()

        app = {
            "init_time": 0.0,
            "server_port": 79,
            "packet_size": tamanhoMedioDePacote,
            "time_to_send": time_to_send,
        }
        chargeList.append(app)
        numberOfCharges -= 1

    file_path = "./Charges/IOT_charge.json"
    json.dump(chargeList, codecs.open(file_path, 'w', encoding='utf-8'), separators=(',', ':'), indent=4)

if __name__ == "__main__":
    voip_charge(20)
    video_stream_charge(50, 3000000)
    web_charge(10)
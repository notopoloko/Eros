import json

import matplotlib
import matplotlib.pyplot as plt
from scipy.signal import lfilter
import pandas as pd
from statistics import mean, stdev
from statsmodels.graphics.tsaplots import plot_acf
from hurst import compute_Hc

def video_stuff():
    time_between_segments = []
    time_downloading = []
    video_codecs = 0

    try:
        with open('./Charges/stream_charge.json') as json_file:  
            data = json.load(json_file)
            time_between_segments = data[0]['time_between_segments']
            # Mudar esse nome
            time_downloading = data[0]['time_downloading']
            video_codecs = data[0]['video_codification']
            time_between_segments = data[0]['time_between_segments']
            json_file.close()
        # fig, ax = plt.subplot(1, 2, 2)
        # ax.plot(segmentTime)
        m = mean(time_downloading)
        s = stdev(time_downloading)

        # Normaliza a série
        for i in range(len(time_downloading)):
            time_downloading[i] = (time_downloading[i]-m)/s
        
        time_downloading = lfilter([1,0.7,0.5,0.4,0.3,0.25], [1], time_downloading)

        # Restaura série original'
        for i in range(len(time_downloading)):
            time_downloading[i] = time_downloading[i]*s + m

        plt.subplot(1, 3, 1)
        plt.plot(time_downloading)
        plt.title('ON time sintético')
        plt.xlabel('Número do segmento')
        plt.ylabel('ON time')

        plt.subplot(1, 3, 2)
        plt.plot(time_between_segments)
        plt.title('IR time sintético')
        plt.xlabel('Número do segmento')
        plt.ylabel('IR time')

        # Calcula os valores de autocorrelacao
        numberOfAutoCorrValues = 5
        autoCorrValues = numberOfAutoCorrValues*[0.0]
        s = pd.Series(time_downloading)
        for i in range(numberOfAutoCorrValues):
            autoCorrValues[i] = s.autocorr(lag = i + 1)
        print(autoCorrValues)

        plt.subplot(1, 3, 3)
        plt.plot([1] + autoCorrValues)
        plt.title('Autocorrelação de Pearson')
        plt.xlabel('Defasagem')
        plt.ylabel('autocorrelação')
        # plot_acf(time_downloading)
        plt.show()
        
        # print(len(time_between_segments), len(time_downloading[:150]))
        # c, p = pearsonr(time_downloading[:150], time_between_segments)
        # print(c,p)

        
    except IOError:
        print('Não há arquivo "stream_charge.json" no diretorio')

def plot_agr_load():
    series_total = 86400 * [0]
    series_stream = 86400 * [0]
    series_web = 86400 * [0]
    series_voip = 86400 * [0]
    # Streaming
    for i in range(40):
        try:
            with open('./Charges/stream_charge{}.json'.format(i)) as json_file:  
                data = json.load(json_file)
                init_time = data['init_time']
                message_size_list = data['packet_size']
                time_between_message = data['time_between_packets']
                for k, j in zip(message_size_list, time_between_message):
                    try:
                        series_stream[ int(init_time+j) ] += k
                        init_time += j
                    except IndexError:
                        print('Diferenca entre tamanho de listas')

        except IOError:
            print('No file named "./Charges/stream_charge{}.json"'.format(i))

    H, c, data = compute_Hc(series_stream, kind='change', simplified=False)
    print("Streaming de vídeo => H={:.4f}, c={:.4f}".format(H,c))
    
    plt.subplot(2,2,1)
    plt.plot(series_stream, color='darkred')
    plt.title('Streaming de vídeo sob demanda')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Trafego agregado (bytes)')

    # WEB
    for i in range(85):
        try:
            with open('./Charges/web_charge{}.json'.format(i)) as json_file:  
                data = json.load(json_file)
                init_time = data['init_time']
                message_size_list = data['packet_size']
                time_between_message = data['time_between_packets']
                for k, j in zip(message_size_list, time_between_message):
                    try:
                        if init_time+j > 86400:
                            break
                        series_web[ int(init_time+j) ] += k
                        init_time += j
                    except IndexError:
                        print('Diferenca entre tamanho de listas')

        except IOError:
            print('No file named "./Charges/stream_charge{}.json"'.format(i))

    plt.subplot(2,2,2)
    plt.plot(series_web, color='darkred')
    plt.title('WEB')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Trafego agregado (bytes)')

    H, c, data = compute_Hc(series_web, kind='change', simplified=False)
    print("WEB => H={:.4f}, c={:.4f}".format(H,c))

    # VoIP
    for i in range(554):
        try:
            with open('./Charges/voip_charge{}.json'.format(i)) as json_file:  
                data = json.load(json_file)
                init_time = data['init_time']
                message_size = data['packet_size']
                time_between_message = data['time_between_packets']
                for k in time_between_message:
                    try:
                        if init_time+k > 86400:
                            break
                        series_voip[ int(init_time+k) ] += message_size
                        init_time += k
                    except IndexError:
                        print('Diferenca entre tamanho de listas')

        except IOError:
            print('No file named "./Charges/stream_charge{}.json"'.format(i))

    H, c, data = compute_Hc(series_voip, kind='change', simplified=False)
    print("VoIP => H={:.4f}, c={:.4f}".format(H,c))

    plt.subplot(2,2,3)
    plt.plot(series_voip, color='darkred')
    plt.title('VoIP')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Trafego agregado (bytes)')

    z = 0
    for i,j,k in zip(series_stream, series_web, series_voip):
        series_total[z] += i + j + k
        z += 1

    H, c, data = compute_Hc(series_total, kind='change', simplified=False)
    print("Total => H={:.4f}, c={:.4f}".format(H,c))

    plt.subplot(2,2,4)
    plt.plot(series_total, color='darkred')
    plt.title('Tráfego Agregado')
    plt.xlabel('Tempo (segundos)')
    plt.ylabel('Trafego agregado (bytes)')
    plt.subplots_adjust(hspace=0.3)

    plt.show()
    # print(sum(series_total))

def sum_variable_message_size(jsonFile: str) -> int:
    sum = 0

    try:
        with open(jsonFile) as json_file:  
            data = json.load(json_file)
            for i in data['packet_size']:
                sum += i
            json_file.close()
    except IOError:
        print('No file named: ', jsonFile)

    return sum

def sum_fixed_size(json_file: str) -> int:
    sum = 0

    try:
        with open(json_file) as json_file:  
            data = json.load(json_file)
            packet_size = data['packet_size']
            sum = packet_size * len(data['time_between_packets'])
            json_file.close()
    except IOError:
        print('No file named: ', json_file)

    return sum

if __name__ == "__main__":
    # total = 0
    # for i in range(554):
    #     # total += sum_variable_message_size('./Charges/web_charge{}.json'.format(i))
    #     # total += sum_variable_message_size('./Charges/stream_charge{}.json'.format(i))
    #     total += sum_fixed_size('./Charges/voip_charge{}.json'.format(i))
    # print(total)

    # plot_agr_load()
    with open('./Charges/stream_charge0.json') as fp:
        data = json.load(fp)
        print(mean(data['packet_size']))
import json
from threading import Semaphore

sem = Semaphore()

def video_stream_analyser(escala, chargeNumber = 0):
    time_between_segments = []
    # time_downloading = []
    try:
        with open('./Charges/stream_charge{}.json'.format(chargeNumber)) as json_file:  
            data = json.load(json_file)
            time_between_segments = data['time_between_packets']
            packet_size = data['packet_size']
    except IOError:
        print('Não há arquivo "stream_charge{}.json" no diretorio'.format(chargeNumber))
        return
    
    getSummedCharge(time_between_segments)

    time_between_segments = [int(x*escala) for x in time_between_segments]
    # time_downloading = [int((x + 0.5)*escala) for x in time_downloading]

    averageRate = [0]*(time_between_segments[len(time_between_segments) - 1] + 1)
    for i in range(len(time_between_segments)):
        averageRate[ int( time_between_segments[i] ) ] += packet_size[i]

    # f = open('averageRateVideoStream.txt', 'w')
    # f.write(str(averageRate))
    # f.close()
    return averageRate

# TODO
def video_stream_total_analyser(pointsToPlot, placeToPlot, numeroDeCargas: int, initTime: int, endTime:int):
    time_between_segments = []
    initTime = 0
    totalVideo = 0
    for j in range(numeroDeCargas):
        try:
            with open('./Charges/stream_charge{}.json'.format(j)) as videoChargeJsonFile:
                charge = json.load(videoChargeJsonFile)
                videoChargeJsonFile.close()
            # for charge in data:
                time_between_segments = charge['time_between_packets']
                getSummedCharge(time_between_segments)
                init_time = charge['init_time']
                # Mudar esse nome
                packet_size = charge['packet_size']

                for t, pkt in zip(time_between_segments, packet_size):
                    if t + init_time >= len(pointsToPlot):
                        break
                    # Possível condicao de corrida
                    sem.acquire()
                    pointsToPlot[int(t + init_time)] += pkt
                    sem.release()
                    totalVideo += pkt
            placeToPlot.setText(str(int(totalVideo)))

        except IOError:
            print('Não há arquivo stream_charge{}.json no diretório'.format(j))
            return

def voip_analyser(escala, chargeNumber=0):
    packet_size = 0
    sequenceOfPackets = []

    try:
        with open('./Charges/voip_charge{}.json'.format(chargeNumber)) as voipJsonFile:
            data = json.load(voipJsonFile)
            packet_size = data['packet_size']
            sequenceOfPackets = data['time_between_packets']
            voipJsonFile.close()

        for i in range(1, len(sequenceOfPackets)):
            sequenceOfPackets[i] = sequenceOfPackets[i] + sequenceOfPackets[i-1]
    except IOError:
        print('Não há arquivo voip_charge{}.json no diretório'.format(chargeNumber))
        return

    averageRate = [0]*( int (sequenceOfPackets[ len(sequenceOfPackets) - 1 ] * escala ) + 1 )

    if isinstance(packet_size, int):
        for i in sequenceOfPackets:
            averageRate[ int( i*escala ) ] += packet_size
    elif isinstance(packet_size, list):
        for i in range(len(sequenceOfPackets)):
            averageRate[int( sequenceOfPackets[i]*escala )] += packet_size[i]

    # f = open('averageRateVoip.txt', 'w')
    # f.write(str(averageRate))
    # f.close()
    return averageRate

# TODO: change to minutes scale
def voip_total_analyser(pointsToPlot, placeToPlot, numeroDeCargas: int, initTime: int, endTime: int):
    packet_size = 0
    initTime = 0
    totalVoip = 0
    for i in range(numeroDeCargas):
        try:
            with open('./Charges/voip_charge{}.json'.format(i)) as voipJsonChargeFile:
                charge = json.load(voipJsonChargeFile)
                voipJsonChargeFile.close()
                packet_size = charge['packet_size']
                sequenceOfPackets = charge['time_between_packets']
                initTime = charge['init_time']
                getSummedCharge(sequenceOfPackets)
                if isinstance(packet_size, int):
                    # tamanho das mensagens é fixo
                    for val in sequenceOfPackets:
                        index = int(val + initTime)
                        if index < len(pointsToPlot) and index >= initTime and index <= endTime:
                            sem.acquire()
                            pointsToPlot[index] += packet_size
                            sem.release()
                            totalVoip += packet_size
                elif isinstance(packet_size, list):
                    # Tamanho das mensagens eh variavel
                    for i in range(len(sequenceOfPackets)):
                        index = int(sequenceOfPackets[i] + initTime)
                        if index < len(pointsToPlot) and index >= initTime and index <= endTime:
                            sem.acquire()
                            pointsToPlot[index-int(initTime)] += packet_size[i]
                            sem.release()
                            totalVoip += packet_size[i]
        except IOError:
            print('Não há arquivo voip_charge{}.json'.format(i))
            return

    placeToPlot.setText( str(totalVoip) )

# Tráfego gerado em segundos
# Deve garantir que as cargas estejam corretas antes de chamar a funcao
def web_analyser(escala, chargeNumber = 0):
    try:
        with open('./Charges/web_charge{}.json'.format(chargeNumber)) as webJsonFile:
            data = json.load(webJsonFile)
            # Agrega o tráfego dentro de um segundo
            # ou na escala escolhida
            packetSize = data['packet_size']
            timeOfMessage = data['time_between_packets']

            for i in range(len(timeOfMessage) - 1):
                timeOfMessage[i + 1] = timeOfMessage[i] + timeOfMessage[i + 1]

            vectorSize = data['duration']

            pointsToPlot = [0]*(vectorSize + 1)
            pseudoTime = 0
            for i, j in zip(packetSize, timeOfMessage):
                pointsToPlot[pseudoTime] += i
                if j - pseudoTime >= 1:
                    pseudoTime = int(j)

            webJsonFile.close()
        return pointsToPlot
    except IOError:
        print('Não há arquivo web_charge{}.json no diretório'.format(chargeNumber))

# TODO
def web_total_analyser(pointsToPlot, placeToPlot, numeroDeCargas: int, initTime: int, endTime: int):
    totalWeb = 0
    for i in range(numeroDeCargas):
        try:
            with open('./Charges/web_charge{}.json'.format(i)) as webJsonFile:
                charge = json.load(webJsonFile)
                webJsonFile.close()
                time_between_packets = charge['time_between_packets']
                getSummedCharge(time_between_packets)
                points = charge['packet_size']
                init_time = int(charge['init_time'])

                for time, messageSize in zip(time_between_packets, points):
                    index = int(time + init_time)
                    if time < len(pointsToPlot) and index >= initTime and index <= endTime:
                        # Evitar condições de corrida
                        sem.acquire()
                        pointsToPlot[ int(index) ] += messageSize
                        sem.release()
                        totalWeb += messageSize
        except IOError:
            print('Não há arquivo web_charge{}.json no diretório'.format(i))

    placeToPlot.setText(str(int(totalWeb)))

# Trafego gerado em minutos
def IOT_analyser( escala, chargeNumber = 0 ):
    packet_size = 0
    time_to_send = None
    try:
        with open('./Charges/IOT_charge{}.json'.format(chargeNumber)) as iotJsonFile:
            charge = json.load(iotJsonFile)
            packet_size = charge['packet_size']
            time_to_send = charge['time_between_packets']
            iotJsonFile.close()
    except IOError:
        print('Não há arquivo IOT_charge{}.json no diretório'.format(chargeNumber))
        return

    # for i in range(1, len(time_to_send)):
    #     time_to_send[i] = time_to_send[i] + time_to_send[i-1]

    getSummedCharge(time_to_send)

    # for idx, val in enumerate(time_to_send, 1):
    #     time_to_send[idx] += time_to_send[idx-1]

    pointsToPlot = [0]*(int(time_to_send[-1] * escala) + 1)
    for i in time_to_send:
        pointsToPlot[int(i * escala)] += packet_size
    # newList.append(int(time_to_send[0]*escala))
    # for i in range(1, len(time_to_send)):
    #     newList.append(int(time_to_send[i]*escala))
    return pointsToPlot

# TODO
def IOT_total_analyser(pointsToPlot, placeToPlot, numeroDeCargas: int, initTime: int, endTime: int):
    totalIOT = 0
    messageSize = 0
    for i in range(numeroDeCargas):
        try:
            # initTime = 0
            with open('./Charges/IOT_charge{}.json'.format(i)) as iotJsonChargeFile:
                charge = json.load(iotJsonChargeFile)
                iotJsonChargeFile.close()

                time_to_send = charge['time_between_packets']
                messageSize = charge['packet_size']
                init_time = int(charge['init_time'])
                getSummedCharge(time_to_send)
                for val in time_to_send:
                    index = int(val + init_time)
                    if index < len(pointsToPlot) and index >= initTime and index <= endTime:
                        sem.acquire()
                        pointsToPlot[index] += messageSize
                        sem.release()
                        totalIOT += messageSize
        except IOError:
            print('Não há arquivo IOT_charge{}.json no diretório'.format(i))
            return

    placeToPlot.setText(str(totalIOT))

def getSummedCharge(time_to_send):
    i = 1
    size = len(time_to_send)
    while(i < size):
        time_to_send[i] += time_to_send[i-1]
        i+=1
    
import json

def video_stream_analyser(escala, chargeNumber = 0):
    time_between_segments = []
    # time_downloading = []
    video_codecs = 0

    try:
        with open('./Charges/stream_charge.json') as json_file:  
            data = json.load(json_file)
            time_between_segments = data[chargeNumber]['time_between_segments']
            # Mudar esse nome
            # time_downloading = data[chargeNumber]['time_downloading']
            video_codecs = data[chargeNumber]['video_codification']/1000
            segmentTime = data[chargeNumber]['segment_time']
    except IOError:
        print('Não há arquivo "stream_charge.json" no diretorio')
        return
    
    for i in range(1, len(time_between_segments)):
        time_between_segments[i] += time_between_segments[i-1]

    # last_item = int(max(time_downloading)*escala)

    time_between_segments = [int(x*escala) for x in time_between_segments]
    # time_downloading = [int((x + 0.5)*escala) for x in time_downloading]

    averageRate = [0]*(time_between_segments[len(time_between_segments) - 1] + 1)
    for i in range(len(time_between_segments)):
        averageRate[ int( time_between_segments[i] ) ] += video_codecs * segmentTime / escala

    # f = open('averageRateVideoStream.txt', 'w')
    # f.write(str(averageRate))
    # f.close()
    return averageRate

# TODO
def video_stream_total_analyser():
    pass

def voip_analyser(escala, chargeNumber=0):
    packet_size = 0
    sequenceOfPackets = []

    try:
        with open('./Charges/voip_charge.json') as voipJsonFile:
            data = json.load(voipJsonFile)
            packet_size = data[chargeNumber]['packet_size']
            sequenceOfPackets = data[chargeNumber]['time_between_packets']
            voipJsonFile.close()

        for i in range(1, len(sequenceOfPackets)):
            sequenceOfPackets[i] = sequenceOfPackets[i] + sequenceOfPackets[i-1]
    except IOError:
        print('Não há arquivo voip_charge.json no diretório')

    averageRate = [0]*( int (sequenceOfPackets[ len(sequenceOfPackets) - 1 ] * escala ) + 1 )

    for i in sequenceOfPackets:
        averageRate[ int( i*escala ) ] += packet_size

    # f = open('averageRateVoip.txt', 'w')
    # f.write(str(averageRate))
    # f.close()
    return averageRate

# TODO: change to minutes scale
def voip_total_analyser(pointsToPlot):
    try:
        charges = None
        packet_size = 0
        with open('./Charges/voip_charge.json') as voipJsonChargeFile:
            charges = json.load(voipJsonChargeFile)
            voipJsonChargeFile.close()
        for charge in charges:
            packet_size = charge['packet_size']
            sequenceOfPackets = charge['time_between_packets']
            getSummedCharge(sequenceOfPackets)
            for val in sequenceOfPackets:
                index = int(val / 60)
                if index < len(pointsToPlot):
                    pointsToPlot[index] +=packet_size
    except IOError:
        print('Não há arquivo voip_charge.json')
        return

# Tráfego gerado em segundos
def web_analyser(chargeNumber = 0):
    pointsToPlot = []
    try:
        with open('./Charges/web_charge.json') as webJsonFile:
            data = json.load(webJsonFile)
            pointsToPlot = data[chargeNumber]['series']
            webJsonFile.close()
        return pointsToPlot
    except IOError:
        print('Não há arquivo web_charge.json no diretório')

# TODO
def web_total_analyser(pointsToPlot):
    try:
        charges = None
        points = None
        with open('./Charges/web_charge.json') as webJsonFile:
            charges = json.load(webJsonFile)
            webJsonFile.close()
        for charge in charges:
            points = charge['series']
            for idx, val in enumerate(points):
                if (idx // 60) < len(pointsToPlot):
                    pointsToPlot[ idx // 60 ] += val
            
    except IOError:
        print('Não há arquivo web_charge.json no diretório')

# Trafego gerado em minutos
def IOT_analyser( escala, chargeNumber = 0 ):
    packet_size = 0
    time_to_send = None
    try:
        with open('./Charges/IOT_charge.json') as iotJsonFile:
            charge = json.load(iotJsonFile) [chargeNumber]
            packet_size = charge['packet_size']
            time_to_send = charge['time_to_send']
            iotJsonFile.close()
    except IOError:
        print('Não há arquivo IOT_charge.json no diretório')
        return

    # for i in range(1, len(time_to_send)):
    #     time_to_send[i] = time_to_send[i] + time_to_send[i-1]

    getSummedCharge(time_to_send)

    # for idx, val in enumerate(time_to_send, 1):
    #     time_to_send[idx] += time_to_send[idx-1]

    newList = list()
    newList.append(int(time_to_send[0]*escala))
    for i in range(1, len(time_to_send)):
        newList.append(int(time_to_send[i]*escala))
    return (newList, packet_size)

# TODO
def IOT_total_analyser(pointsToPlot):
    try:
        charges = None
        messageSize = 0
        with open('./Charges/IOT_charge.json') as iotJsonChargeFile:
            charges = json.load(iotJsonChargeFile)
            iotJsonChargeFile.close()

        for charge in charges:
            time_to_send = charge['time_to_send']
            messageSize = charge['packet_size']
            getSummedCharge(time_to_send)
            for val in time_to_send:
                index = int(val)
                if index < len(pointsToPlot):
                    pointsToPlot[index] += messageSize
    except IOError:
        print('Não há arquivo IOT_charge.json no diretório')
        return

def getSummedCharge(time_to_send):
    i = 1
    size = len(time_to_send)
    while(i < size):
        time_to_send[i] += time_to_send[i-1]
        i+=1
    
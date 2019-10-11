import _sha512
import json
import pickle
from charge_generator import *
from traffic_analyser import *

workload_generator = {"iot": iot_charge,
                      "voip": voip_charge,
                      "stream": video_stream_charge,
                      "web": web_charge
                      }

#Adjust parameters of applications and let the
desiredWorkload = {
       "iot": { "traffic_percentage": 0.1, "application_config": {"tamanhoMedioDePacote": 10, "tempoEntreMensagem": 1, "numberOfCharges":  1}},
      "voip": { "traffic_percentage": 0.1, "application_config": {"call_duration": 5, "numeroDeCargas": 1}},
    "stream": { "traffic_percentage": 0.3, "application_config": {"tempoVideo": 200, "video_code": 10, "numeroDeCargas": 1}},
       "web": { "traffic_percentage": 0.4, "application_config": {"tempoDeSerie": 200, "numberOfCharges": 1}}
}
import random
#command line interface
def main():
    global desiredWorkload
    sha512 = _sha512.sha512()

    #Adjust desiredWorkload percentages to sum to 1
    sumPercentages = 0
    for workload in desiredWorkload:
        sumPercentages += desiredWorkload[workload]["traffic_percentage"]
    for workload in desiredWorkload:
        desiredWorkload[workload]["traffic_percentage"] /= sumPercentages
    del sumPercentages

    trafficJson = {"input": desiredWorkload, "workload": {}, "packets_n_sizes_formatting": {}}

    #For each desired application traffic
    for workload in desiredWorkload:
        #Create a new entry if one doesn't exist yet
        if workload not in trafficJson["workload"]:
            trafficJson["workload"][workload] = {"applications": {}}

        #Create traffic associated with a given application
        output = workload_generator[workload](**desiredWorkload[workload]["application_config"])

        #Calculate hash for the application
        outputJson = json.dumps(output)
        sha512.update(outputJson.encode())
        outputSha  = sha512.digest().__repr__()

        #Use the hash to address it
        trafficJson["workload"][workload]["applications"][outputSha] = output
        del outputJson


        #Convert whatever format it came from the charge_generator to a universal format for traffic injectors

        last_output_universal_traffic_format = {}
        time_accumulator = 0

        if workload == "iot":
            for i in range(len(output[0]["time_to_send"])):
                # Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[output[0]["time_to_send"][i]] = int(output[0]["packet_size"] + 1)
                pass
            pass
        elif workload == "voip":
            last_output_universal_traffic_format[time_accumulator] = int(output[0]["packet_size"]+1)

            for i in range(1, len(output[0]["time_between_packets"])):
                # Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[time_accumulator] = int(output[0]["packet_size"]+1)
                time_accumulator += output[0]["time_between_packets"][i - 1]
                pass
            pass
        elif workload == "stream":
            #Deal with first element and then proceed to others
            last_output_universal_traffic_format[time_accumulator] = int((output[0]["time_downloading"][0] * (
                        output[0]["video_codification"] / 8)) + 1)  # time downloading * byte rate

            for i in range(1, len(output[0]["time_downloading"])):
                #Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[time_accumulator] = int((output[0]["time_downloading"][i]*(output[0]["video_codification"]/8))+1) #time downloading * byte rate
                time_accumulator += output[0]["time_between_segments"][i-1]
                pass
            pass
        elif workload == "web":
            for i in range(len(output[0]["series"])):
                #Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[i] = int(output[0]["series"][i]+1) #bytes to download
                pass
            pass
        else:
            print("Something went pretty darn wrong")
            return -1

        trafficJson["packets_n_sizes_formatting"][(outputSha, workload)] = last_output_universal_traffic_format

        #Measure how many bytes were transmitted per application
        trafficJson["workload"][workload]["applications"][outputSha][0]["totalBytes"] = sum(last_output_universal_traffic_format.values())
        trafficJson["workload"][workload]["applications"][outputSha][0]["duration"] = sorted(list(last_output_universal_traffic_format.keys()))[-1]

        del outputSha, output, time_accumulator, last_output_universal_traffic_format
    del i, sha512

    #Measure overall traffic percentages for both applications and traffic workloads
    trafficTotalBytes = 0
    trafficTotalDuration = 0
    for workload in desiredWorkload:
        workloadTotalBytes = 0
        workloadTotalDuration = 0
        for application in trafficJson["workload"][workload]["applications"]:
            traffic  = trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]
            duration = trafficJson["workload"][workload]["applications"][application][0]["duration"]
            workloadTotalBytes += traffic
            workloadTotalDuration += duration
        trafficTotalBytes += workloadTotalBytes
        trafficTotalDuration += workloadTotalDuration
        trafficJson["workload"][workload]["totalBytes"] = workloadTotalBytes
        trafficJson["workload"][workload]["duration"] = workloadTotalDuration
    del traffic

    maxDuration = 0
    for workload in desiredWorkload:
        for application in trafficJson["workload"][workload]["applications"]:
            trafficJson["workload"][workload]["applications"][application][0]["traffic_percentage"] = trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]/trafficTotalBytes
        trafficJson["workload"][workload]["trafficPercentage"] = trafficJson["workload"][workload]["totalBytes"]/trafficTotalBytes
        maxDuration = trafficJson["workload"][workload]["duration"] if trafficJson["workload"][workload]["duration"] > maxDuration else maxDuration

    # Find application/workload with biggest gap to the expected traffic
    biggestPercentageGap = (0, None)
    for workload in desiredWorkload:
        gap = desiredWorkload[workload]["traffic_percentage"] - trafficJson["workload"][workload][
            "trafficPercentage"]
        if gap > biggestPercentageGap[0]:
            biggestPercentageGap = (gap, workload)

    #Adjust overall traffic to fit specified percentages
    iterations = 0
    while(biggestPercentageGap[0] > 0.001):
        iterations += 1
        workload = biggestPercentageGap[1]

        #If the application duration is not similar to the one with the maximum duration, randomly select a package from the already existing and append it
        if trafficJson["workload"][workload]["duration"] < (maxDuration*0.9):
            application = list(trafficJson["workload"][workload]["applications"])[0]

            packets = sorted(list(trafficJson["packets_n_sizes_formatting"][(application, workload)].items()))
            packets_to_copy = [int(random.gauss(len(packets), len(packets)) %len(packets)) for _ in range(10)]

            lastPacket = packets[-1]
            totalBytes = 0
            duration = 0
            for packet in packets_to_copy:
                currPacket = packets[packet]
                prevPacket = packets[(packet-1) % len(packets)]
                newPacket = (lastPacket[0]+(currPacket[0]-prevPacket[0]), currPacket[1])
                trafficJson["packets_n_sizes_formatting"][(application, workload)][newPacket[0]] = newPacket[1]
                packets.append(newPacket)
                totalBytes += newPacket[1]
                duration = newPacket[0]
                print()
                pass

            del newPacket, lastPacket, prevPacket, packets_to_copy, packets, currPacket, packet

            # Add sent bytes and replace with the new number
            trafficJson["workload"][workload]["totalBytes"] += totalBytes
            trafficJson["workload"][workload]["duration"] += duration

            # Update the total traffic bytes
            trafficTotalBytes += totalBytes

            # Recalculate the percentages for each workflow after the changes
            for workload in desiredWorkload:
                trafficJson["workload"][workload]["trafficPercentage"] = trafficJson["workload"][workload]["totalBytes"] / trafficTotalBytes
                pass
            pass
            del duration, application, totalBytes
        #If the application duration is similar to the one with the maximum duration, adjust packet sizes
        else:
            #assuming a single application per workload type
            multiplication_factor = desiredWorkload[workload]["traffic_percentage"]/trafficJson["workload"][workload]["trafficPercentage"]
            application = list(trafficJson["workload"][workload]["applications"])[0]
            totalBytes = 0

            #Adjust the byte size of packages by a multiplication factor
            for time_to_send in trafficJson["packets_n_sizes_formatting"][(application, workload)]:
                trafficJson["packets_n_sizes_formatting"][(application, workload)][time_to_send] *= multiplication_factor
                trafficJson["packets_n_sizes_formatting"][(application, workload)][time_to_send] += 1
                trafficJson["packets_n_sizes_formatting"][(application, workload)][time_to_send] = int(trafficJson["packets_n_sizes_formatting"][(application,workload)][time_to_send])
                totalBytes += trafficJson["packets_n_sizes_formatting"][(application, workload)][time_to_send]

            #Remove application old sent bytes and replace with the new number
            trafficJson["workload"][workload]["totalBytes"] -= trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]
            trafficJson["workload"][workload]["totalBytes"] += totalBytes

            #Update the total traffic bytes
            #trafficJson["workload"][workload]["applications"][application][0]["totalBytes"] = totalBytes
            trafficTotalBytes -= trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]
            trafficTotalBytes += totalBytes

            #Recalculate the percentages for each workflow after the changes
            for workload in desiredWorkload:
                trafficJson["workload"][workload]["trafficPercentage"] = trafficJson["workload"][workload]["totalBytes"]/trafficTotalBytes
                pass

            del multiplication_factor, application, totalBytes, time_to_send
            pass

        # Find application/workload with biggest gap to the expected traffic
        biggestPercentageGap = (0, None)
        for workload in desiredWorkload:
            gap = desiredWorkload[workload]["traffic_percentage"] - trafficJson["workload"][workload]["trafficPercentage"]
            if gap > biggestPercentageGap[0]:
                biggestPercentageGap = (gap, workload)
        pass
    del workload


    #Sort packet_n_sizes_formatting before dumping
    unsorted_traffic = trafficJson["packets_n_sizes_formatting"]
    sorted_traffic = {}
    for key, traffic in unsorted_traffic.items():
        sorted_traffic[key[0]] = sorted(list(traffic.items()))

    trafficJson["packets_n_sizes_formatting_sorted"] = sorted_traffic

    #Dump everything to a pickle
    with open("trafficJson.pickle", "wb") as fd:
        pickle.dump(trafficJson, fd)

    #And only the sorted and formatted traffic for the JSON
    with open("trafficJson.json", "w") as fd:
        json.dump(trafficJson["packets_n_sizes_formatting_sorted"], fd)

    print()
    pass

#call main
import sys
main()
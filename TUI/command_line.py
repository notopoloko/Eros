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

#command line interface
def main(argv):
    sha512 = _sha512.sha512()
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

            trafficJson["packets_n_sizes_formatting"][outputSha] = last_output_universal_traffic_format
            pass
        elif workload == "voip":
            last_output_universal_traffic_format[time_accumulator] = int(output[0]["packet_size"]+1)

            for i in range(1, len(output[0]["time_between_packets"])):
                # Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[time_accumulator] = int(output[0]["packet_size"]+1)
                time_accumulator += output[0]["time_between_packets"][i - 1]
                pass

            trafficJson["packets_n_sizes_formatting"][outputSha] = last_output_universal_traffic_format
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

            trafficJson["packets_n_sizes_formatting"][outputSha] = last_output_universal_traffic_format
            pass
        elif workload == "web":
            for i in range(len(output[0]["series"])):
                #Determine size of packet and time offset for when it should be transmitted
                last_output_universal_traffic_format[i] = int(output[0]["series"][i]+1) #bytes to download
                pass

            trafficJson["packets_n_sizes_formatting"][outputSha] = last_output_universal_traffic_format
            pass
        else:
            print("Something went pretty darn wrong")

        #Measure how many bytes were transmitted per application
        trafficJson["workload"][workload]["applications"][outputSha][0]["totalBytes"] = sum(last_output_universal_traffic_format.values())
        trafficJson["workload"][workload]["applications"][outputSha][0]["duration"] = sorted(list(last_output_universal_traffic_format.keys()))[-1]

        del outputSha, output, time_accumulator, last_output_universal_traffic_format

    #Measure overall traffic percentages for both applications and traffic workloads
    trafficTotalBytes = 0
    for workload in desiredWorkload:
        workloadTotalBytes = 0
        for application in trafficJson["workload"][workload]["applications"]:
            traffic = trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]
            workloadTotalBytes += traffic
            trafficTotalBytes += traffic
        trafficJson["workload"][workload]["totalBytes"] = workloadTotalBytes

    for workload in desiredWorkload:
        for application in trafficJson["workload"][workload]["applications"]:
            trafficJson["workload"][workload]["applications"][application][0]["traffic_percentage"] = trafficJson["workload"][workload]["applications"][application][0]["totalBytes"]/trafficTotalBytes
        trafficJson["workload"][workload]["trafficPercentage"] = trafficJson["workload"][workload]["totalBytes"]/trafficTotalBytes

    #Sort packet_n_sizes_formatting before dumping
    unsorted_traffic = trafficJson["packets_n_sizes_formatting"]
    sorted_traffic = {}
    for app, traffic in unsorted_traffic.items():
        sorted_traffic[app] = sorted(list(traffic.items()))

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
main(sys.argv)
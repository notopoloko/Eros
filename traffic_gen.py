import os
import sys
import numpy 
import numpy.random as random
import matplotlib.pyplot as plt
import json

sys.path.append(os.path.dirname(__name__))

########################################## Distribution functions ##############################################


def ParetoDistribution(**kwargs): #num samples, shape, mode
	random.seed(supportedDistributions["Pareto"]["seed"])
	a = kwargs["a"]
	m = kwargs["m"]
	size = kwargs["size"]
	hist_partitions = kwargs["hist_partitions"]

	samples = (random.pareto(a=a, size=size) + 1) * m

	count, hist_bins = numpy.histogram(samples, hist_partitions, density=True)
	fit = a*m**a / hist_bins**(a+1)
	hist_fitted = [max(count)*fitt/max(fit) for fitt in fit]	
	return samples, hist_bins, hist_fitted, hist_partitions


def PoissonDistribution(**kwargs): #num samples, shape, mode
	random.seed(supportedDistributions["Poisson"]["seed"])
	lambd = kwargs["lambd"]
	size = kwargs["size"]
	hist_partitions = kwargs["hist_partitions"]

	samples = random.poisson(lam=lambd, size=size)

	count, hist_bins = numpy.histogram(samples, hist_partitions, density=True)
	fit = hist_bins
	hist_fitted = [max(count)*fitt/max(fit) for fitt in fit]	
	return samples, hist_bins, hist_fitted, hist_partitions

def generateTraffic(userTrafficWorkload):
	distribution = supportedDistributions[userTrafficWorkload["distribution"]]
	distribution["seed"] = userTrafficWorkload["seed"]
	results = distribution["generatorFunction"](userTrafficWorkload["arguments"])

	return results[0]

########################################## End Distribution functions ##############################################
########################################## Global Variables ##############################################


supportedDistributions = {
	"Pareto"     : {"seed": 0, "generatorFunction": ParetoDistribution , "kwargs": {"size": 1000, "a"    :   3, "m"              : 2, "hist_partitions": 30} },
	"Poisson"    : {"seed": 0, "generatorFunction": PoissonDistribution, "kwargs": {"size": 1000, "lambd": 1.0, "hist_partitions": 30} },
	#"Uniform"    : {"seed": 0, "generatorFunction": random.uniform     },
	#"Gaussian"   : {"seed": 0, "generatorFunction": random.normal      },
	#"Exponential": {"seed": 0, "generatorFunction": random.exponential }
}

userTrafficWorkloads = {}
userGeneratedTrafficWorkloads = {}


########################################## Global Variables ##############################################
########################################## Prepare distribution images ##############################################


for distribution in list(supportedDistributions.keys()):
	distributionImagePath = "static/"+distribution+".jpg"
	if not os.path.exists(distributionImagePath):

		random.seed(supportedDistributions[distribution]["seed"])
		samples, hist_bins, hist_fitted, hist_partitions = supportedDistributions[distribution]["generatorFunction"](supportedDistributions[distribution]["kwargs"])
		plt.hist(samples, hist_partitions, density=True)
		plt.plot(hist_bins, hist_fitted, linewidth=2, color='r')
		plt.savefig(distributionImagePath)
		plt.close()


########################################## End Prepare distribution images ##############################################






########################################## Web server ##############################################


from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def hello_world():
    return render_template('index.html', availableDistributions = list(supportedDistributions.keys()), userTrafficWorkloads = userTrafficWorkloads)


@app.route("/distribution")
@app.route("/distribution/")
@app.route("/distribution/<distribution_name>")
def distribution(distribution_name=""):
	if distribution_name in list(supportedDistributions.keys()):
		return render_template("distribution.html", distribution_image_path="static/"+distribution_name+".jpg")
	else:
		return "", 200


@app.route("/addTrafficWorkload/", methods=["POST"])
def addTrafficWorkload():
	val = request.get_data()
	trafficWorkloadParameters = json.loads(val)

	userTrafficWorkloads[len(userTrafficWorkloads)] = trafficWorkloadParameters
	return "", 200


@app.route("/generateTrafficWorkload/")
def generateTrafficWorkload():
	#Save inputs for later
	userGeneratedTrafficWorkloads["input"]             = userTrafficWorkloads
	userGeneratedTrafficWorkloads["workloadTraffic"]   = {}
	userGeneratedTrafficWorkloads["aggregatedTraffic"] = {}

	#Generate all individual traffic workloads and then fuse
	for workload in userTrafficWorkloads:
		userGeneratedTrafficWorkloads["workloadTraffic"][workload]  = generateTraffic(userTrafficWorkloads[workload])

		for transmissionTime, bytesTransmitted in userGeneratedTrafficWorkloads["workloadTraffic"][workload]:
			if transmissionTime not in userGeneratedTrafficWorkloads["aggregatedTraffic"]:
				userGeneratedTrafficWorkloads["aggregatedTraffic"][transmissionTime] = bytesTransmitted
			userGeneratedTrafficWorkloads["aggregatedTraffic"][transmissionTime] += bytesTransmitted

	return json.dumps(userGeneratedTrafficWorkloads, indent=4), 200



app.run()


########################################## End Web server ##############################################

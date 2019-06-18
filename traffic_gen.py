import os
import sys
import numpy 
import numpy.random as random
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(__name__))

########################################## Distribution functions ##############################################

def ParetoDistribution(size=1000, a=3, m=2, hist_partitions=30): #num samples, shape, mode
	random.seed(supportedDistributions["Pareto"]["seed"])
	samples = (random.pareto(a=a, size=1000) + 1) * m

	count, hist_bins = numpy.histogram(samples, hist_partitions, density=True)
	fit = a*m**a / hist_bins**(a+1)
	hist_fitted = [max(count)*fitt/max(fit) for fitt in fit]	
	return samples, hist_bins, hist_fitted, hist_partitions

def PoissonDistribution(size=1000, lambd=1.0, hist_partitions=30): #num samples, shape, mode
	random.seed(supportedDistributions["Poisson"]["seed"])
	samples = random.poisson(lam=lambd, size=1000)

	count, hist_bins = numpy.histogram(samples, hist_partitions, density=True)
	fit = hist_bins
	hist_fitted = [max(count)*fitt/max(fit) for fitt in fit]	
	return samples, hist_bins, hist_fitted, hist_partitions

########################################## End Distribution functions ##############################################

supportedDistributions = {
	"Pareto"     : {"seed": 0, "generatorFunction": ParetoDistribution },
	"Poisson"    : {"seed": 0, "generatorFunction": PoissonDistribution},
	#"Uniform"    : {"seed": 0, "generatorFunction": random.uniform     },
	#"Gaussian"   : {"seed": 0, "generatorFunction": random.normal      },
	#"Exponential": {"seed": 0, "generatorFunction": random.exponential }
}


########################################## Prepare distribution images ##############################################
for distribution in list(supportedDistributions.keys()):
	distributionImagePath = "static/"+distribution+".jpg"
	if not os.path.exists(distributionImagePath):

		random.seed(supportedDistributions[distribution]["seed"])
		samples, hist_bins, hist_fitted, hist_partitions = supportedDistributions[distribution]["generatorFunction"](size=1000)
		plt.hist(samples, hist_partitions, density=True)
		plt.plot(hist_bins, hist_fitted, linewidth=2, color='r')
		plt.savefig(distributionImagePath)
		plt.close()


########################################## End Prepare distribution images ##############################################






########################################## Web server ##############################################
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route("/distribution/")
@app.route("/distribution/<distribution_name>")
def distribution(distribution_name=""):
	if distribution_name in list(supportedDistributions.keys()):
		return render_template("distribution.html", distribution_image_path="static/"+distribution_name+".jpg")
	else:
		return ("",200)

app.run()
########################################## End Web server ##############################################

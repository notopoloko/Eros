import numpy
import scipy
import matplotlib.pyplot as plt
import statistics
import scipy.stats as stats
import scipy.signal as signal

#Number of time samples
lengths = 10000

#List of time samples
x_axis = numpy.array(list(range(lengths)))
x_axis_prob = numpy.arange(0,1,1/lengths)

#Mean and standard deviation of a normal distribution that will be adjusted for covariance matching
mean = 0
stddev = 1
randomNumbers = numpy.random.normal(loc=mean, scale=stddev, size=lengths)
plt.plot(x_axis, randomNumbers)
plt.show()
plt.clf()
#stdd = statistics.stdev(randomNumbers)

#Generate a lognormal distribution to compute covariance multipliers
mu = 1
sigma =0.5
#correlationMultipliers = numpy.random.lognormal(mu, sigma, 10000)
#plt.plot(x_axis, correlationMultipliers)
#avg = statistics.mean(correlationMultipliers)
#correlationMultipliers /= avg
#avg = statistics.mean(correlationMultipliers)

#Calculate probability density function of the lognormal distribution
pdf = (numpy.exp(-(numpy.log(x_axis) - mu)**2 / (2 * x_axis**2))
       / (x_axis * sigma * numpy.sqrt(2 * numpy.pi)))

#Set first member to 1, as described in the paper
pdf[0] = 1

#for i in range(1, lengths, 2):
#    pdf[i] = -pdf[i]
plt.plot(x_axis[:100], pdf[:100])
plt.show()
plt.clf()

#Multiply covariance factors and the normal distribution
randomNumbersFFT = numpy.fft.fft(randomNumbers)
randomNumbersFFTfreq = numpy.fft.fftfreq(randomNumbersFFT.shape[-1])
plt.plot(randomNumbersFFTfreq,randomNumbersFFT.real, randomNumbersFFTfreq, randomNumbersFFT.imag)
plt.show()
plt.clf()

pdfFFT = numpy.fft.fft(pdf)
a = numpy.zeros(lengths)
a[0] = 1
adjustedCorrelationFFT = signal.lfilter( a, pdf[:100], randomNumbersFFT)
#adjustedCorrelationFFT = randomNumbersFFT * pdfFFT
plt.plot(randomNumbersFFTfreq,adjustedCorrelationFFT)
plt.show()
plt.clf()
#adjustedCorrelationFFT = randomNumbersFFT * pdf

#Inverse fourier transform of the random numbers already adjusted for covariance
adjustedRandomNumbers = numpy.real(numpy.fft.ifft(adjustedCorrelationFFT))
plt.plot(x_axis,adjustedRandomNumbers)
plt.show()
plt.clf()

#Compute average and standard deviation
averageAdjusted = statistics.mean(adjustedRandomNumbers)
adjustedRandomNumbers *= 2/averageAdjusted
averageAdjusted = statistics.mean(adjustedRandomNumbers)

plt.plot(x_axis,adjustedRandomNumbers)
plt.show()
plt.clf()

stddevAdjusted = statistics.stdev(adjustedRandomNumbers)
covarianceAdjusted = numpy.cov([adjustedRandomNumbers.tolist()])

#Compute probability density function of the adjusted series
pdfAdjusted = stats.norm.pdf(adjustedRandomNumbers)

plt.plot(x_axis_prob,pdfAdjusted)

plt.show()
plt.clf()

plt.hist(adjustedRandomNumbers)

plt.show()
plt.clf()
print()
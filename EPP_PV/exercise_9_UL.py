#Import the ROOT libraries
import ROOT

####Open the rootfile and get the workspace

#Set some of the parameters constant, to speed it up
#### Set constant all parameters but the number of background events

nuisanceParams = ROOT.RooArgSet(ws.var("N_bkg"))

#Configure the model, we need both the S+B and the B only models
#### Construct the signal+background model, set into it the workspace and the PDF


poi = ROOT.RooArgSet(ws.var("N_sig"))
sbModel.SetParametersOfInterest(poi)
sbModel.SetNuisanceParameters(nuisanceParams)

### Create a background only model by cloning the previous one and setting the POI to zero

#First example is with a frequentist approach
fc = ROOT.RooStats.FrequentistCalculator(ws.data("unbinneddata"), bModel, sbModel)
fc.SetToys(1000,1000)

#Configure ToyMC Sampler of the frequentist calculator
toymcs = fc.GetTestStatSampler()

#Use profile likelihood as test statistics 
profll = ROOT.RooStats.ProfileLikelihoodTestStat(sbModel.GetPdf())
#for CLs (bounded intervals) use one-sided profile likelihood
profll.SetOneSided(1)

#set the test statistic to use for toys
toymcs.SetTestStatistic(profll)

#Create hypotest inverter passing the desired calculator 
calc = ROOT.RooStats.HypoTestInverter(fc)

#set confidence level (e.g. 95% upper limits)
calc.SetConfidenceLevel(0.95)

#use CLs
calc.UseCLs(1)

#reduce the noise
calc.SetVerbose(0)

npoints = 15 #Number of points to scan
# min and max for the scan (better to choose smaller intervals)
poimin = poi.find("N_sig").getMin()
poimax = poi.find("N_sig").getMax()

print("Doing a fixed scan  in interval : ", poimin, " , ", poimax)
calc.SetFixedScan(npoints,poimin,poimax);

result = calc.GetInterval() #This is a HypoTestInveter class object
upperLimit = result.UpperLimit()

#Example using the BayesianCalculator

#Now we also need to specify a prior in the ModelConfig
#To be quicker, we'll use the PDF factory facility of RooWorkspace
#Careful! For simplicity, we are using a flat prior, but this doesn't mean it's the best choice!
priorPOI = ws.factory("Uniform::prior(N_sig)")
sbModel.SetPriorPdf(priorPOI)

#We also need priors for the nuisance parameters so that they can be integrated. These can come from many sources
ws.factory("Gaussian::prior_Nbkg(N_bkg,100,100)")
bayesmodel = ws.factory("PROD::bayesmodel(totpdf,prior_Nbkg)") # pdf*priorNuisance

#Construct the bayesian calculator
bc = ROOT.RooStats.BayesianCalculator(ws.data("unbinneddata"), bayesmodel,poi,priorPOI,nuisanceParams)
bc.SetConfidenceLevel(0.95)
bc.SetLeftSideTailFraction(0.) # for upper limit

bcInterval = bc.GetInterval()

#Now let's print the result of the two methods
#First the CLs
print("################")
print("The observed CLs upper limit is: ", upperLimit)

#Compute expected limit
print("Expected upper limits, using the B (alternate) model : ")
print(" expected limit (median) ", result.GetExpectedUpperLimit(0))
print(" expected limit (-1 sig) ", result.GetExpectedUpperLimit(-1))
print(" expected limit (+1 sig) ", result.GetExpectedUpperLimit(1))
print("################")

#Now let's see what the bayesian limit is
print("Bayesian upper limit on N_sig = ", bcInterval.UpperLimit())

#Plot now the result of the scan 

#First the CLs
freq_plot = ROOT.RooStats.HypoTestInverterPlot("HTI_Result_Plot","Frequentist scan result for N_sig",result)
#Then the Bayesian posterior
bc_plot = bc.GetPosteriorPlot()

#Plot in a new canvas with style
dataCanvas = ROOT.TCanvas("dataCanvas")
dataCanvas.Divide(2,1)
dataCanvas.SetLogy(0)
dataCanvas.cd(1)
freq_plot.Draw("2CL")
dataCanvas.cd(2)
bc_plot.Draw()
dataCanvas.SaveAs("exercise_9_UL.png")
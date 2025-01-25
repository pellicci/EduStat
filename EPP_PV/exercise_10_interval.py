
import ROOT

#####Open the rootfile and get the workspace from the invariant mass fit

#You can set constant parameters that are known
#If you leave them floating, the fit procedure will determine their uncertainty
#For now, set constant the majority of them, for timing purposes (and reasons we'll see soon...)
ws.var("meanJpsi").setConstant(1)
ws.var("sigmaJpsi").setConstant(1)
ws.var("alphaJpsi").setConstant(1)
ws.var("nJpsi").setConstant(1)
ws.var("NJpsi").setConstant(1)
#ws.var("meanpsi2S").setConstant(1)
ws.var("Nbkg").setConstant(1)
ws.var("a1").setConstant(1)
ws.var("a2").setConstant(1)
ws.var("a3").setConstant(1)

#Let the model know what is the parameter of interest
cross_psi = ws.var("cross_psi")
cross_psi.setRange(4., 16.)  #this is mostly for plotting reasons
poi = ROOT.RooArgSet(cross_psi)

#Configure the model
#### Configure the ModelConfig object, set the workspace, the PDF, and the parameters of interest

#Set confidence level
confidenceLevel = 0.68

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("data"), model)
plc.SetParameters(poi)
plc.SetConfidenceLevel(confidenceLevel)

#Get the interval
pl_Interval = plc.GetInterval()

#Now let's determine the Bayesian probability interval
#We could use the standard Bayesian Calculator, but this would be very slow for the integration
#So we profit of the Markov-Chain MC capabilities of RooStats to speed things up
mcmc = ROOT.RooStats.MCMCCalculator(ws.data("data") , model)
mcmc.SetConfidenceLevel(confidenceLevel)
mcmc.SetNumIters(30000)           #Metropolis-Hastings algorithm iterations
mcmc.SetNumBurnInSteps(100)       #first N steps to be ignored as burn-in
mcmc.SetLeftSideTailFraction(0.5) #for central interval

MCMC_interval = mcmc.GetInterval()

#Let's make a plot
dataCanvas = ROOT.TCanvas("dataCanvas")
dataCanvas.Divide(2,1)

dataCanvas.cd(1)
plot_Interval = ROOT.RooStats.LikelihoodIntervalPlot(pl_Interval)
plot_Interval.SetTitle("Profile Likelihood Ratio")
plot_Interval.SetMaximum(3.)
plot_Interval.Draw()

dataCanvas.cd(2)
#### Do the same as above for the Markov Chain, using the MCMCIntervalPlot class (same interface)

dataCanvas.SaveAs("exercise_10.png")

#Now print the interval for mH for the two methods
print("PLC interval is [", pl_Interval.LowerLimit(cross_psi), ", ", pl_Interval.UpperLimit(cross_psi), "]")

#### Do the same as above to print the MC bayesian limit


#PyROOT sometimes fails cleaning memory, this helps
del mcmc

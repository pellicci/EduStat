#import the root libraries in python
import ROOT

#Create a gaussian signal PDF
mass = ROOT.RooRealVar("mass","The invariant mass",100.,150.,"GeV/c^2")
#### Now create similar variables for the mean of the Gaussian (say centered at 125 GeV) and the width (around 2 GeV)
#### Give them a meaningful range, they will need to vary in the fit

mean = ROOT.RooRealVar("mean","The mean of the gaussian",125.,110.,140.)
width =  ROOT.RooRealVar("width","The width of the gaussian",2.,0.001,5.)

#Construct the gaussian PDF
gaussPDF = ROOT.RooGaussian("gaussPDF","The gaussian function",mass,mean,width)

#for this simple exercise, we'll generate a dataset
data = gaussPDF.generate({mass},1000)

#### Fit the gaussian to the data
#### See the fitTo function in https://root.cern/doc/v630/classRooAbsPdf.html

#plot the data and the fit result, then save it
massplot = mass.frame()  #This is a RooPlot object
data.plotOn(massplot)
gaussPDF.plotOn(massplot)

canvas = ROOT.TCanvas()
canvas.cd()
massplot.Draw()
canvas.SaveAs("exercise_0.png")

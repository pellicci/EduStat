#import the root libraries in python
import ROOT

#Create a gaussian signal PDF
mass = ROOT.RooRealVar("mass","The invariant mass",100.,150.,"GeV/c^2")
mean = ROOT.RooRealVar("mean","The mean of the gaussian",125.,110.,140.)
width =  ROOT.RooRealVar("width","The width of the gaussian",2.,0.001,5.)

gaussPDF = ROOT.RooGaussian("gaussPDF","The gaussian function",mass,mean,width)

#### Now create a background PDF using an exponential
#### First define a tau parameter. Give it an initial value of -0.05, and a range around -5 and -0.000001
#### Then define the background PDF using a RooExponential. Call it expoPDF

#The total PDF will be the sum of the Gaussian and the exponential PDFs, with a parameter that expresses the relative normalization (and can be fitted)
frac = ROOT.RooRealVar("frac","Fraction of signal",0.5,0.,1.)
totPDF = ROOT.RooAddPdf("totPDF","The total PDF",[gaussPDF,expoPDF],[frac])

#### Generate a 1000 events dataset with this combined PDF

#### Fit the total PDF on the dataset you generated

#Now we can plot the result. RooFit allows to easily plot both the total PDF and some of the components
massplot = mass.frame()
data.plotOn(massplot)
totPDF.plotOn(massplot)
totPDF.plotOn(massplot, Components="expoPDF", LineStyle="--", LineColor="kRed")

canvas = ROOT.TCanvas()
canvas.cd()
massplot.Draw()
canvas.SaveAs("exercise_1.png")

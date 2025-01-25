import ROOT

mass = ROOT.RooRealVar("mass","The invariant mass",100.,150.,"GeV/c^2")

#Create a gaussian signal PDF
#Signal is the convolution of a BW times a gaussian resolution function

#### Define a RooBreitWigner called BWsig with the following parameters:
mpole = ROOT.RooRealVar("mpole","Pole position",125.,110.,140.)
BWwidth = ROOT.RooRealVar("BWwidth","Width of the Breit-Wigner",1.,0.0001,5.)

#### Define a Gaussian function called gaussPDF with the following parameters:
meanGauss = ROOT.RooRealVar("meanGauss","The mean of the gaussian",0.5,0.0001,2.)
widthGauss = ROOT.RooRealVar("widthGauss","The width of the gaussian",1.,0.001,5.)

#### Set constant the Gaussian width

#Here we define the total signal PDF using the convolution of the two functions
totSigPDF = ROOT.RooNumConvPdf("totSigPDF","Total signal PDF",mass,gaussPDF,BWsig)

#Background PDF: exponential background
#### Copy the exponential function from the previous exercise

#### Copy the definition of signal and background number of events from the previous exercise

#### Define the total PDF as the sum of the signal and background function (similar to previous exercise)

#### Generate 1000 events with the total PDF

#### fit the total PDF to the data

#### Create a RooPlot object, plot the data and the total PDF on it (also plot the background component)

#### Save everything into a workspace

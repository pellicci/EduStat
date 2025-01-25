import ROOT

mass = ROOT.RooRealVar("mass","The invariant mass",100.,150.)

#Signal PDF
mean1 = ROOT.RooRealVar("mean1","Mean of first signal gaussian",125.,110.,140.)
sigma1 = ROOT.RooRealVar("sigma1","Sigma of first signal gaussian",1.,0.001,4.)
#### Create a Gaussian for the first signal component using the parameters above. Call it SigGauss1

#Background PDF
a0 = ROOT.RooRealVar("a0","a0",-1.,-3.,3.)
a1 = ROOT.RooRealVar("a1","a1",0.5,-3.,3.)
BkgPDF = ROOT.RooChebychev("BkgPDF","BkgPDF",mass,[a0,a1])

#Total first PDF
#### Create a total PDF called totPDF1 with the signal and background functions above. Signal has a fraction (call it frac1) of 60%. 

#Build the second signal PDF
sigma2 = ROOT.RooRealVar("sigma2","Sigma of second signal gaussian",2.,0.001,4.)
#### Create a second signal PDF SigGauss2. This differs from the first only because of the width defined above, and everything else is shared

#Total second PDF
#### Build a total PDF for the second sample, using the same background function as sample one. Here, the signal fraction (frac2) is 40%

#Generate the two samples
#### Generate the samples from the two PDFs. Call them data1 and data2. First sample is 1000 events, the second one is 2000

#Define the two categories of the sample
SigCat = ROOT.RooCategory("SigCat","Signal categories")
SigCat.defineType("Signal1")
SigCat.defineType("Signal2")

combinedData = ROOT.RooDataSet("combinedData","The combined data", {mass}, Import={"Signal1": data1, "Signal2" :data2}, Index=SigCat )

#Construct the simultaneous PDF
simPdf = ROOT.RooSimultaneous("simPdf","The total simultaneous PDF",SigCat)
simPdf.addPdf(totPDF1,"Signal1")
simPdf.addPdf(totPDF2,"Signal2")

#Do the fitting
#### Fit the simultaneous PDF to the combined data

#Do the plotting

#Separately for the two categories
massframe1 = mass.frame()
combinedData.plotOn(massframe1, Cut="SigCat==SigCat::Signal1")
simPdf.plotOn(massframe1, Slice=[SigCat,"Signal1"], ProjWData=(SigCat,combinedData) )
simPdf.plotOn(massframe1, Slice=[SigCat,"Signal1"], ProjWData=(SigCat,combinedData), Components="BkgPDF", LineStyle="--" )

massframe2 = mass.frame()
##### Do the same as above for the other category

canvas = ROOT.TCanvas()
canvas.Divide(2,1)
canvas.cd(1)
massframe1.Draw()
canvas.cd(2)
massframe2.Draw()
canvas.SaveAs("exercise_4.png")

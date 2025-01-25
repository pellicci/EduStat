
import ROOT

#### Define a invariant mass variable between 60 and 120 GeV

#Here's the data
_fileIn = ROOT.TFile("exercise_6.root")
_fileIn.cd()

data = _fileIn.Get("totPDFData")

#Signal PDF
#### Create a signal PDF parametrized with a Breit-Wigner (called BWsig) with a pole at 90 GeV and a width of 2 GeV. Both parameters should be free to float

#Background PDF
a0 = ROOT.RooRealVar("a0","a0",-1.,-3.,3.)
a1 = ROOT.RooRealVar("a1","a1",0.5,-3.,3.)
a2 = ROOT.RooRealVar("a2","a2",-0.1,-3.,3.)
a3 = ROOT.RooRealVar("a3","a3",0.1,-3.,3.)
#### Create a background PDF parametrized with a Chebychev polynomial. Start with order 1 (straight line). Call it BkgPDF


Nsig = ROOT.RooRealVar("Nsig","Number of signal events",200.,0.001,1000.)
Nbkg = ROOT.RooRealVar("Nbkg","Number of background events",300.,0.001,1000.)

#### Create a total PDF with all the information above

fit_result = totPDF.fitTo(data,Extended=True,Save=1)

print("minNll = ", fit_result.minNll())

#### Calculate the delta log likelihood between the first and the second order, then second and third, etc.
#### Stop when deltalogL < 3.85 (95% of a chi2 with 1 degree of freedom)

#### Plot the data, and both the total and the background only PDF

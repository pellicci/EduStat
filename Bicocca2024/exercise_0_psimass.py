
import ROOT

#Supress the opening of many Canvas's
ROOT.gROOT.SetBatch(True)   

#Get the input file
fInput = ROOT.TFile("DataSet_jpsi_mass_lowstat.root")
dataset = fInput.Get("data")

#The observable
mass = ROOT.RooRealVar("mass","#mu^{+}#mu^{-} invariant mass",2.,6.,"GeV")

#The Jpsi signal parametrization: we'll use a Crystal Ball
meanJpsi = ROOT.RooRealVar("meanJpsi","The mean of the Jpsi Crystal Ball",3.1,2.8,3.2)
sigmaJpsi = ROOT.RooRealVar("sigmaJpsi","The width of the Jpsi Crystal Ball",0.3,0.0001,1.)
alphaJpsi = ROOT.RooRealVar("alphaJpsi","The alpha of the Jpsi Crystal Ball",1.5,-5.,5.)
nJpsi = ROOT.RooRealVar("nJpsi","The alpha of the Jpsi Crystal Ball",1.5,0.5,5.)

CBJpsi = ROOT.RooCBShape("CBJpsi","The Jpsi Crystall Ball",mass,meanJpsi,sigmaJpsi,alphaJpsi,nJpsi)

#The psi(2S) signal parametrization: width will be similar to Jpsi, but with shifted mass
meanpsi2S = ROOT.RooRealVar("meanpsi2S","The mean of the psi(2S) Crystal Ball",3.7,3.65,3.75)
CBpsi2S = ROOT.RooCBShape("CBpsi2S","The psi(2S) Crystal Ball",mass,meanpsi2S,sigmaJpsi,alphaJpsi,nJpsi)

#Background parametrization: just a polynomial
a1 = ROOT.RooRealVar("a1","The a1 of background",-0.7,-2.,2.)
a2 = ROOT.RooRealVar("a2","The a2 of background",0.3,-2.,2.)
a3 = ROOT.RooRealVar("a3","The a3 of background",-0.03,-2.,2.)
backgroundPDF = ROOT.RooChebychev("backgroundPDF","The background PDF",mass,ROOT.RooArgList(a1,a2,a3))

#Define the yields
NJpsi = ROOT.RooRealVar("NJpsi","The Jpsi events",1500.,0.1,10000.)
Nbkg = ROOT.RooRealVar("Nbkg","The bkg events",5000.,0.1,50000.)

#Now define the number of psi events
Npsi = ROOT.RooRealVar("Npsi","The psi(2S) events",500.,0.1,10000.)

#Compose the total PDF
totPDF = ROOT.RooAddPdf("totPDF","The total PDF",ROOT.RooArgList(CBJpsi,CBpsi2S,backgroundPDF),ROOT.RooArgList(NJpsi,Npsi,Nbkg))

#Do the actual fit
totPDF.fitTo(dataset, ROOT.RooFit.Extended(1))

#Print values of the parameters (that now reflect fitted values and errors)
print("##############")
meanpsi2S.Print()
NJpsi.Print()
Npsi.Print()
print("##############")

#Now plot the data and the fit result
xframe = mass.frame()
dataset.plotOn(xframe)
totPDF.plotOn(xframe)

#One can also plot the single components of the total PDF, like the background component
totPDF.plotOn(xframe, ROOT.RooFit.Components("backgroundPDF"), ROOT.RooFit.LineStyle(ROOT.kDashed), ROOT.RooFit.LineColor(ROOT.kRed))

#Draw the results
c1 = ROOT.TCanvas()
xframe.Draw()
c1.SaveAs("exercise_0_fitmass.png")

#Now save the data and the PDF into a Workspace, for later use for statistical analysis
ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(dataset)
getattr(ws,'import')(totPDF)

fOutput = ROOT.TFile("Workspace_mumufit.root","RECREATE")
ws.Write()
fOutput.Write()
fOutput.Close()

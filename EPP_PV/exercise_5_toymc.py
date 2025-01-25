import ROOT

mass = ROOT.RooRealVar("mass","The invariant mass",7.,14.,"GeV")

#Signal PDF
#### Create a Gaussian signal using the parameters below, call it SigGauss1
mean1 = ROOT.RooRealVar("mean1","Mean of first signal gaussian",9.4,8.,11.)
sigma1 = ROOT.RooRealVar("sigma1","Sigma of first signal gaussian",0.1,0.001,2.)
SigGauss1 = ROOT.RooGaussian("SigGauss1","First signal gaussian",mass,mean1,sigma1)

#### Now create a second Gaussian signal (SigGauss2) with a mean centered at 10.5 GeV and a width of 0.2 GeV

#### Now combine them into a total PDF with a relative fraction of the first of 40%


#Background PDF
a0 = ROOT.RooRealVar("a0","a0",-0.3,-0.8,0.8)
a1 = ROOT.RooRealVar("a1","a1",-0.1,-0.8,0.8)

#### Construct a Chebychev polynomial for background using the parameters above, call it BkgPDF


#Total PDF
Nsig = ROOT.RooRealVar("Nsig","Number of signal events",900.,0.1,3000.)
Nbkg = ROOT.RooRealVar("Nbkg","Number of background events",100.,0.1,3000.)

#### Create a total PDF for sig+bkg with the number of events above for each

#Construct the Toy-MC machinery
mcstudy = ROOT.RooMCStudy(totPDF, {mass}, Silence=True, Extended=True, FitOptions=dict(Save=True, PrintEvalErrors=0))
mcstudy.generateAndFit(1000)

#Plot the distributions of the fitted parameter, the error and the pull
sigma1val_frame = mcstudy.plotParam(sigma1, Bins=40)
sigma1err_frame = mcstudy.plotError(sigma1, Bins=40)
sigma1pull_frame = mcstudy.plotPull(sigma1, Bins=40, FitGauss=True)

#Plot distribution of minimized likelihood
NLLframe = mcstudy.plotNLL(Bins=40)

#Actually plot

#### Create a canva, divide it in 4, and plot the four frames into them

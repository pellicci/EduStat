

#Get the histograms that describe the different contributions to the signal and background
M4l4l_Inclusive_H125Unblinded   = fInput.Get("M4l4l_Inclusive_H125Unblinded")

#Transform the histograms into PDFs. First you have to create a RooDataHist object (a fancy histogram), then create the PDF
h125hist = ROOT.RooDataHist("h125hist","h125hist",[m4l],M4l4l_Inclusive_H125Unblinded)
pdfh125  = ROOT.RooHistPdf("pdfh125","pdfh125",{m4l},h125hist)

#Expected number of signal events, based on SM expectations
#Instead of the number of events, we can fit for the cross section with a simple transformation
eff_h125 = ROOT.RooRealVar("eff_h125","The Higgs reco+id efficiency",0.35,0.00001,1.)
lumi = ROOT.RooRealVar("lumi","The CMS luminosity",24800.,0.00001,50000.,"pb-1")
br_hzz = ROOT.RooRealVar("br_hzz","H->ZZ->4l BR",0.02*0.062*0.062)
cross_h125 = ROOT.RooRealVar("cross_h125","The h125 xsec",3.,0.,100.,"pb")

#Number of events for each background contribution. The initial value is the expectation from theory+simulation
NggZZ = ROOT.RooRealVar("NggZZ","NggZZ",68.4,0.1,200.)
NqqZZ = ROOT.RooRealVar("NqqZZ","NqqZZ",317.8,0.1,500.)
NZX   = ROOT.RooRealVar("NZX","NZX",22.9,0.1,200.)


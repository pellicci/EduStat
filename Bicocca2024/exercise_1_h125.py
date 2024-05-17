
import ROOT

#Supress the opening of many Canvas's
ROOT.gROOT.SetBatch(True)   

#Define the observable
m4l = ROOT.RooRealVar("m4l","m4l",75.,400.)

#import the data
fInput = ROOT.TFile("h4l_shapes.root")
fInput.cd()

unbinned_4l = fInput.Get("unbinned_m4l")

#Get the histograms that describe the different contributions
M4l4l_Inclusive_H125Unblinded   = fInput.Get("M4l4l_Inclusive_H125Unblinded")
M4l4l_Inclusive_ggZZUnblinded   = fInput.Get("M4l4l_Inclusive_ggZZUnblinded")
M4l4l_Inclusive_qqZZUnblinded   = fInput.Get("M4l4l_Inclusive_qqZZUnblinded")
M4l_ZX_SS_4l_InclusiveUnblinded = fInput.Get("M4l_ZX_SS_4l_InclusiveUnblinded")

#Transform the histograms into PDFs
h125hist = ROOT.RooDataHist("h125hist","h125hist",ROOT.RooArgList(m4l),M4l4l_Inclusive_H125Unblinded)
pdfh125  = ROOT.RooHistPdf("pdfh125","pdfh125",ROOT.RooArgSet(m4l),h125hist)

ggZZhist = ROOT.RooDataHist("ggZZhist","ggZZhist",ROOT.RooArgList(m4l),M4l4l_Inclusive_ggZZUnblinded)
pdfggZZ  = ROOT.RooHistPdf("pdfggZZ","pdfggZZ",ROOT.RooArgSet(m4l),ggZZhist)

qqZZhist = ROOT.RooDataHist("qqZZhist","qqZZhist",ROOT.RooArgList(m4l),M4l4l_Inclusive_qqZZUnblinded)
pdfqqZZ  = ROOT.RooHistPdf("pdfqqZZ","pdfqqZZ",ROOT.RooArgSet(m4l),qqZZhist)

ZXhist = ROOT.RooDataHist("ZXhist","ZXhist",ROOT.RooArgList(m4l),M4l_ZX_SS_4l_InclusiveUnblinded)
pdfZX  = ROOT.RooHistPdf("pdfZX","pdfZX",ROOT.RooArgSet(m4l),ZXhist)

#Number of events for each contribution
Nh125 = ROOT.RooRealVar("Nh125","Nh125",19.15,0.0,100.)
NggZZ = ROOT.RooRealVar("NggZZ","NggZZ",61.63,0.1,200.)
NqqZZ = ROOT.RooRealVar("NqqZZ","NqqZZ",286.29,0.1,500.)
NZX   = ROOT.RooRealVar("NZX","NZX",22.91,0.1,200.)

#Compose the total PDF
totpdf = ROOT.RooAddPdf("totpdf","totpdf",ROOT.RooArgList(pdfh125,pdfggZZ,pdfqqZZ,pdfZX),ROOT.RooArgList(Nh125,NggZZ,NqqZZ,NZX))

#Do the fit to data
totpdf.fitTo(unbinned_4l,ROOT.RooFit.Extended(1))

#Plot the result
canvas = ROOT.TCanvas()
canvas.cd()
m4lplot = m4l.frame(75)
unbinned_4l.plotOn(m4lplot)
totpdf.plotOn(m4lplot)

#One can also plot the single components of the total PDF, like the background component
totpdf.plotOn(m4lplot, ROOT.RooFit.Components("pdfqqZZ,pdfggZZ,pdfZX"), ROOT.RooFit.FillColor(ROOT.kGreen),ROOT.RooFit.DrawOption("F"))
totpdf.plotOn(m4lplot, ROOT.RooFit.Components("pdfqqZZ,pdfggZZ"), ROOT.RooFit.FillColor(ROOT.kCyan),ROOT.RooFit.DrawOption("F"))

unbinned_4l.plotOn(m4lplot)

m4lplot.Draw()
canvas.SaveAs("m4lfit.gif")

#Now save the data and the PDF into a Workspace, for later use for statistical analysis
ws = ROOT.RooWorkspace("ws")
getattr(ws,'import')(unbinned_4l)
getattr(ws,'import')(totpdf)

fOutput = ROOT.TFile("Workspace_m4l.root","RECREATE")
ws.Write()
fOutput.Write()
fOutput.Close()

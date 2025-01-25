import ROOT

fInput = ROOT.TFile("exercise_2.root")
fInput.cd()

workspace = fInput.Get("myworkspace")

mass = workspace.var("mass")
totPDF = workspace.pdf("totPDF")

data = workspace.data("totPDFData")

#### Create a new RooPlot, plot the data and the PDF, draw it into a canva, and save it

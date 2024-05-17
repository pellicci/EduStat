
import ROOT

#Open the rootfile and get the workspace from the exercise_0
fInput = ROOT.TFile("Workspace_m4l.root")
ws = fInput.Get("ws")
ws.Print()

#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("totpdf")

#Here we explicitly set the value of the parameters for the null hypothesis
#We want no signal contribution, so Nh125 = 0
Nh125 = ws.var("Nh125")
poi = ROOT.RooArgSet(Nh125)
nullParams = poi.snapshot()
nullParams.setRealValue("Nh125",0.)

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("unbinned_m4l"), model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)

#We get a HypoTestResult out of the calculator, and we can query it.
htr = plc.GetHypoTest()

print("-------------------------------------------------")
print("The p-value for the null is ", htr.NullPValue())
print("Corresponding to a signifcance of ", htr.Significance())
print("-------------------------------------------------")

#PyROOT sometimes fails cleaning memory, this helps
del plc
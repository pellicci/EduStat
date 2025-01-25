import ROOT

#Open the rootfile and get the workspace
fInput = ROOT.TFile("Zmumugamma_ws.root")
ws = fInput.Get("myworkspace")
ws.Print()

#You can set constant parameters that are known
#If you leave them floating, the fit procedure will determine their uncertainty
ws.var("mZpole").setConstant(1)

#Set the RooModelConfig and let it know what the content of the workspace is about
model = ROOT.RooStats.ModelConfig()
model.SetWorkspace(ws)
model.SetPdf("sigbkgPDF")

#Here we explicitly set the value of the parameters for the null hypothesis
#We want no signal contribution, so cross_psi = 0
cross_Zmmg = ws.var("cross_Zmmg")
poi = ROOT.RooArgSet(cross_Zmmg)
nullParams = poi.snapshot()
nullParams.setRealValue("cross_Zmmg",0.)

#Build the profile likelihood calculator
plc = ROOT.RooStats.ProfileLikelihoodCalculator(ws.data("data"), model)
plc.SetParameters(poi)
plc.SetNullParameters(nullParams)

#We get a HypoTestResult out of the calculator, and we can query it.
htr = plc.GetHypoTest()

print("-------------------------------------------------")
print("The p-value for the null is ", htr.NullPValue())
print("Corresponding to a signifcance of ", htr.Significance())
print("-------------------------------------------------")

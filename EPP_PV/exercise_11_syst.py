

#### Copy (most of) the previous exercise, and add a systematic constrain modifier to the signal efficiency, as below

#Create a modifier to account for signal efficiency uncertainty
ws.factory("Gaussian::effConstrain(gSigEff[1.],ratioSigEff[1.,0.,3],0.1)")   #Gaussian with 10% uncertainty
ws.factory("SUM::totPDF_withscaling( prod(cross_psi,lumi_psi,eff_psi,ratioSigEff)*CBpsi2S , NJpsi*CBJpsi, Nbkg*backgroundPDF )") #Recreate the total PDF with the scaling
ws.factory("PROD::totPDF_withconstrain(totPDF_withscaling, effConstrain)")

print("##################################")
print("Now printing the workspace with the additional constraints")
print("##################################")
print(ws.Print())


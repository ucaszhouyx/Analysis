#include "tree.h"
	void add(){
 TFile *f= new TFile("data_0.root","update");
 double mBC_smear;
 double tag_mBC_0;
 TTree *tree =(TTree*)f->Get("tree");
 TBranch *newb = tree->Branch("mBC_smear",&mBC_smear,"mBC_smear/D"); 
  tree->SetBranchAddress("tag_mBC_0", &tag_mBC_0);
 Long64_t nentries = tree ->GetEntries();
 for(Long64_t i=0; i< nentries; i++){
	 tree->GetEntry(i);///!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	 mBC_smear = tag_mBC_0;
	 newb->Fill();
	 
	 
	 
	 
	 
	 }

tree->Write("",TObject::kOverwrite);


	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	}


from experta import * 
import pandas as pd
import os
import json

advise_map={}
answer={}

def preprocess():
    global advise_map
    with open("recomendacion/advises.json",'r') as f:
        advise_map = json.load(f)
 
def get_details(indicator, label):
    return advise_map[indicator][label]

def get_details_extra(indicator, range ,label):
    return advise_map[indicator][range][label]

class Expert(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        print("")
        print("Welcome! this service will give you some advices to improve your free cash flow.")
        print("Please complete the following info:")
        print("")
        yield Fact(action='find_state')

    @Rule(Fact(action='find_state'), NOT(Fact(cr=W())), salience = 1)
    def current_ratio(self):
        self.declare(Fact(cr=float(input('Current Ratio:'))))
    
    @Rule(Fact(action='find_state'), NOT(Fact(rg=W())),salience = 1)
    def revenue_growth(self):
        self.declare(Fact(rg=float(input('Revenue Growth:'))))
    
    @Rule(Fact(action='find_state'), NOT(Fact(da=W())),salience = 1)
    def debt_to_assets(self):
        self.declare(Fact(da=float(input('Total debt to total assets:'))))

    @Rule(Fact(action='find_state'), NOT(Fact(fd=W())),salience = 1)
    def cash_flow_to_debt(self):
        self.declare(Fact(fd=float(input('Free cash flow to total debt:'))))

    @Rule(Fact(action='find_state'), NOT(Fact(om=W())),salience = 1)
    def operating_margin(self):
        self.declare(Fact(om=float(input('Operating Margin:'))))

    @Rule(Fact(action='find_state'), NOT(Fact(ra=W())),salience = 1)
    def return_on_assets(self):
        self.declare(Fact(ra=float(input('Return on Assets:'))))

    @Rule(Fact(action='find_state'), NOT(Fact(ap=W())),salience = 1)
    def accounts_turnover(self):
        self.declare(Fact(ap=float(input('Accounts Payable Turnover:'))))

    @Rule(Fact(action='find_state'), NOT(Fact(se=W())),salience = 1)
    def sales_per_employee(self):
        self.declare(Fact(se=float(input('Sales per Employee:'))))        

    @Rule(Fact(action='find_state'), NOT(Fact(at=W())),salience = 1)
    def asset_turnover(self):
        self.declare(Fact(at=float(input('Asset Turnover:'))))     

    # para cada iteración se le asignará una etiqueta a la característica para evaluarla
    # para la liquidez
    
    # @Rule(Fact(action='find_state'),Fact(cr<80.0))
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr < 80.0)))
    def liquidez_1(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'problematico')))

    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 80.0) & P(lambda cr: cr < 100.0)))
    def liquidez_2(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'mejorable')))
    
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 100.0) & P(lambda cr: cr < 150.0)))
    def liquidez_3(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'moderado'))) 
    
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 150.0) & P(lambda cr: cr < 200.0)))
    def liquidez_4(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 200.0)))
    def liquidez_5(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'excelente')))
        
    @Rule(Fact(action='find_state'),Fact(liquidez=MATCH.liquidez),salience = -998)
    def situation1(self, liquidez):
        print("LIQUIDEZ:")
        print("The description of the advise is given below :\n")
        print(liquidez)
        
    # para el crecimiento
    
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg<(-20.0))))
    def crecimiento_1(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'problematico')))
    
    #@Rule(Fact(action='find_state'),Fact(-20.0<rg and rg<-5.0))
    @Rule(Fact(action='find_state'), Fact(rg=P(lambda rg: rg > -20.0) & P(lambda rg: rg < -5.0)))
    def crecimiento_2(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'mejorable')))
        
    @Rule(Fact(action='find_state'), Fact(rg=P(lambda rg: rg > -5.0) & P(lambda rg: rg < 5.0)))
    def crecimiento_3(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg > 5.0) & P(lambda rg: rg < 20.0)))
    def crecimiento_4(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg > 20.0)))
    def crecimiento_5(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'excelente')))   
        
    @Rule(Fact(action='find_state'),Fact(crecimiento=MATCH.crecimiento),salience = -998)
    def situation2(self, crecimiento):
        print("CRECIMIENTO:")
        print("The description of the advise is given below :\n")
        print(crecimiento) 
        
    # para el apalancamiento
    
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.8) & P(lambda da: da < 1.0)))
    def apalancamiento_1(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.7) & P(lambda da: da < 0.8)))
    def apalancamiento_2(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.5) & P(lambda da: da < 0.7)))
    def apalancamiento_3(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.4) & P(lambda da: da < 0.5)))
    def apalancamiento_4(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.3) & P(lambda da: da < 0.4)))
    def apalancamiento_5(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'excelente')))
        
    #-------------------------------------------------------------------------------------------------
    
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da >= 0.0) & P(lambda da: da < 0.05)))
    def apalancamiento_6(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.05) & P(lambda da: da < 0.1)))
    def apalancamiento_7(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.1) & P(lambda da: da < 0.15)))
    def apalancamiento_8(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.15) & P(lambda da: da < 0.3)))
    def apalancamiento_9(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(apalancamiento=MATCH.apalancamiento),salience = -998)
    def situation3(self, apalancamiento):
        print("APALANCAMIENTO")
        print("The description of the advise is given below :\n")
        print(apalancamiento)

    # para el solvencia
    
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 3.0)))
    def solvencia_1(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.7) & P(lambda fd: fd < 3.0)))
    def solvencia_2(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.4) & P(lambda fd: fd < 1.7)))
    def solvencia_3(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.1) & P(lambda fd: fd < 1.4)))
    def solvencia_4(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.8) & P(lambda fd: fd < 1.1)))
    def solvencia_5(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'excelente')))
        
    #-------------------------------------------------------------------------------------------------
    
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.0) & P(lambda fd: fd < 0.2)))
    def solvencia_6(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.2) & P(lambda fd: fd < 0.4)))
    def solvencia_7(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.4) & P(lambda fd: fd < 0.6)))
    def solvencia_8(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.6) & P(lambda fd: fd < 0.8)))
    def solvencia_9(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(solvencia=MATCH.solvencia),salience = -998)
    def situation4(self, solvencia):
        print("SOLVENCIA:")
        print("The description of the advise is given below :\n")
        print(solvencia)

    # para la rentabilidad
    
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om < 15.0)))
    def rentabilidad_1(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 15.0) & P(lambda om: om < 25.0)))
    def rentabilidad_2(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 25.0) & P(lambda om: om < 40.0)))
    def rentabilidad_3(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 40.0) & P(lambda om: om < 50.0)))
    def rentabilidad_4(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 50.0)))
    def rentabilidad_5(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'excelente')))
        
    @Rule(Fact(action='find_state'),Fact(rentabilidad=MATCH.rentabilidad),salience = -998)
    def situation5(self, rentabilidad):
        print("RENTABILIDAD:")
        print("The description of the advise is given below :\n")
        print(rentabilidad)
        
    # para la eficiencia
    
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 0.0) & P(lambda se: se < 4500.0)))
    def rentabilidad_1(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'problematico')))
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 4500.0) & P(lambda se: se < 9000.0)))
    def rentabilidad_2(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'mejorable')))
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 9000.0) & P(lambda se: se < 12000.0)))
    def rentabilidad_3(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'moderado')))
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 12000.0) & P(lambda se: se < 15000.0)))
    def rentabilidad_4(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'sobresaliente')))
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 15000.0)))
    def rentabilidad_5(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'excelente')))
        
    @Rule(Fact(action='find_state'),Fact(eficiencia=MATCH.eficiencia),salience = -998)
    def situation6(self, eficiencia):
        print("EFICIENCIA:")
        print("The description of the advise is given below :\n")
        print(eficiencia)
  
if __name__ == "__main__":
    preprocess()
    engine = Expert()
    engine.reset()   
    engine.run()

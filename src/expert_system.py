from experta import * 
import json
import os

advise_map={}

def preprocess():
    global advise_map
    with open(os.path.dirname(os.path.abspath(__file__)) + "/recomendacion/advises.json",'r') as f:
        advise_map = json.load(f)
 
def get_details(indicator, label):
    return advise_map[indicator][label]

def get_details_extra(indicator, range ,label):
    return advise_map[indicator][range][label]

class Expert(KnowledgeEngine):
    def set_facts(self, params: dict):
        """
        Maps incoming facts into the system data structures
        Remark: It calls "reset" method at the beginning to delete old Facts.
        """
        self.reset()

        self.declare(Fact(cr=params["current_ratio"]))
        self.declare(Fact(rg=params["revenue_growth_year_over_year"]))
        self.declare(Fact(da=params["total_debt_to_total_assets"]))
        self.declare(Fact(fd=params["free_cash_flow_to_total_debt"]))
        self.declare(Fact(om=params["operating_margin"]))
        self.declare(Fact(ra=params["return_on_assets"]))
        self.declare(Fact(ap=params["accounts_ayable_turnover"]))
        self.declare(Fact(se=params["sales_per_employee"]))
        self.declare(Fact(at=params["asset_turnover"]))


    @DefFacts()
    def _initial_action(self):
        self.answer = dict()
        print("")
        print("Welcome! this service will give you some advices to improve your free cash flow.")
        print("Please complete the following info:")
        print("")
        yield Fact(action='find_state')

    # para cada iteración se le asignará una etiqueta a la característica para evaluarla
    # para la liquidez
    
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr < 80.0)))
    def liquidez_1(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'problematico')))
        self.answer['liquidez']=get_details('liquidez', 'problematico')

    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 80.0) & P(lambda cr: cr < 100.0)))
    def liquidez_2(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'mejorable')))
        self.answer['liquidez']=get_details('liquidez', 'mejorable')
    
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 100.0) & P(lambda cr: cr < 150.0)))
    def liquidez_3(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'moderado')))
        self.answer['liquidez']=get_details('liquidez', 'moderado') 
        
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 150.0) & P(lambda cr: cr < 200.0)))
    def liquidez_4(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'sobresaliente')))
        self.answer['liquidez']=get_details('liquidez', 'sobresaliente') 
        
    @Rule(Fact(action='find_state'),Fact(cr=P(lambda cr: cr > 200.0)))
    def liquidez_5(self):
        self.declare(Fact(liquidez=get_details('liquidez', 'excelente')))
        self.answer['liquidez']=get_details('liquidez', 'excelente') 
        
    @Rule(Fact(action='find_state'),Fact(liquidez=MATCH.liquidez),salience = -998)
    def situation1(self, liquidez):
        print("LIQUIDEZ: OK")
        
    # para el crecimiento
    
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg<(-20.0))))
    def crecimiento_1(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'problematico')))
        self.answer['crecimiento']=get_details('crecimiento', 'problematico')

    @Rule(Fact(action='find_state'), Fact(rg=P(lambda rg: rg > -20.0) & P(lambda rg: rg < -5.0)))
    def crecimiento_2(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'mejorable')))
        self.answer['crecimiento']=get_details('crecimiento', 'mejorable')
        
    @Rule(Fact(action='find_state'), Fact(rg=P(lambda rg: rg > -5.0) & P(lambda rg: rg < 5.0)))
    def crecimiento_3(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'moderado')))
        self.answer['crecimiento']=get_details('crecimiento', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg > 5.0) & P(lambda rg: rg < 20.0)))
    def crecimiento_4(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'sobresaliente')))
        self.answer['crecimiento']=get_details('crecimiento', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(rg=P(lambda rg: rg > 20.0)))
    def crecimiento_5(self):
        self.declare(Fact(crecimiento=get_details('crecimiento', 'excelente')))   
        self.answer['crecimiento']=get_details('crecimiento', 'excelente')
        
    @Rule(Fact(action='find_state'),Fact(crecimiento=MATCH.crecimiento),salience = -998)
    def situation2(self, crecimiento):
        print("CRECIMIENTO: OK")
        
    # para el apalancamiento
    
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.8) & P(lambda da: da < 1.0)))
    def apalancamiento_1(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'problematico')))
        self.answer['apalancamiento']=get_details_extra('apalancamiento', '1', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.7) & P(lambda da: da < 0.8)))
    def apalancamiento_2(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'mejorable')))
        self.answer['apalancamiento']=get_details('apalancamiento', '1', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.5) & P(lambda da: da < 0.7)))
    def apalancamiento_3(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'moderado')))
        self.answer['apalancamiento']=get_details('apalancamiento', '1', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.4) & P(lambda da: da < 0.5)))
    def apalancamiento_4(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'sobresaliente')))
        self.answer['apalancamiento']=get_details('apalancamiento', '1', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.3) & P(lambda da: da < 0.4)))
    def apalancamiento_5(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '1', 'excelente')))
        self.answer['apalancamiento']=get_details('apalancamiento', '1', 'excelente')
        
    #-------------------------------------------------------------------------------------------------
    
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da >= 0.0) & P(lambda da: da < 0.05)))
    def apalancamiento_6(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'problematico')))
        self.answer['apalancamiento']=get_details_extra('apalancamiento', '2', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.05) & P(lambda da: da < 0.1)))
    def apalancamiento_7(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'mejorable')))
        self.answer['apalancamiento']=get_details_extra('apalancamiento', '2', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.1) & P(lambda da: da < 0.15)))
    def apalancamiento_8(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'moderado')))
        self.answer['apalancamiento']=get_details_extra('apalancamiento', '2', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(da=P(lambda da: da > 0.15) & P(lambda da: da < 0.3)))
    def apalancamiento_9(self):
        self.declare(Fact(apalancamiento=get_details_extra('apalancamiento', '2', 'sobresaliente')))
        self.answer['apalancamiento']=get_details_extra('apalancamiento', '2', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(apalancamiento=MATCH.apalancamiento),salience = -998)
    def situation3(self, apalancamiento):
        print("APALANCAMIENTO: OK")

    # para el solvencia
    
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 3.0)))
    def solvencia_1(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'problematico')))
        self.answer['solvencia']=get_details_extra('solvencia', '1', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.7) & P(lambda fd: fd < 3.0)))
    def solvencia_2(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'mejorable')))
        self.answer['solvencia']=get_details_extra('solvencia', '1', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.4) & P(lambda fd: fd < 1.7)))
    def solvencia_3(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'moderado')))
        self.answer['solvencia']=get_details_extra('solvencia', '1', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 1.1) & P(lambda fd: fd < 1.4)))
    def solvencia_4(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'sobresaliente')))
        self.answer['solvencia']=get_details_extra('solvencia', '1', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.8) & P(lambda fd: fd < 1.1)))
    def solvencia_5(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '1', 'excelente')))
        self.answer['solvencia']=get_details_extra('solvencia', '1', 'excelente')
        
    #-------------------------------------------------------------------------------------------------
    
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.0) & P(lambda fd: fd < 0.2)))
    def solvencia_6(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'problematico')))
        self.answer['solvencia']=get_details_extra('solvencia', '2', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.2) & P(lambda fd: fd < 0.4)))
    def solvencia_7(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'mejorable')))
        self.answer['solvencia']=get_details_extra('solvencia', '2', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.4) & P(lambda fd: fd < 0.6)))
    def solvencia_8(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'moderado')))
        self.answer['solvencia']=get_details_extra('solvencia', '2', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(fd=P(lambda fd: fd > 0.6) & P(lambda fd: fd < 0.8)))
    def solvencia_9(self):
        self.declare(Fact(solvencia=get_details_extra('solvencia', '2', 'sobresaliente')))
        self.answer['solvencia']=get_details_extra('solvencia', '2', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(solvencia=MATCH.solvencia),salience = -998)
    def situation4(self, solvencia):
        print("SOLVENCIA: OK")

    # para la rentabilidad
    
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om < 15.0)))
    def rentabilidad_1(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'problematico')))
        self.answer['rentabilidad']=get_details('rentabilidad', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 15.0) & P(lambda om: om < 25.0)))
    def rentabilidad_2(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'mejorable')))
        self.answer['rentabilidad']=get_details('rentabilidad', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 25.0) & P(lambda om: om < 40.0)))
    def rentabilidad_3(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'moderado')))
        self.answer['rentabilidad']=get_details('rentabilidad', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 40.0) & P(lambda om: om < 50.0)))
    def rentabilidad_4(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'sobresaliente')))
        self.answer['rentabilidad']=get_details('rentabilidad', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(om=P(lambda om: om > 50.0)))
    def rentabilidad_5(self):
        self.declare(Fact(rentabilidad=get_details('rentabilidad', 'excelente')))
        self.answer['rentabilidad']=get_details('rentabilidad', 'excelente')
        
    @Rule(Fact(action='find_state'),Fact(rentabilidad=MATCH.rentabilidad),salience = -998)
    def situation5(self, rentabilidad):
        print("RENTABILIDAD: OK")
        
    # para la eficiencia
    
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 0.0) & P(lambda se: se < 4500.0)))
    def eficiencia_1(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'problematico')))
        self.answer['eficiencia']=get_details('eficiencia', 'problematico')
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 4500.0) & P(lambda se: se < 9000.0)))
    def eficiencia_2(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'mejorable')))
        self.answer['eficiencia']=get_details('eficiencia', 'mejorable')
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 9000.0) & P(lambda se: se < 12000.0)))
    def eficiencia_3(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'moderado')))
        self.answer['eficiencia']=get_details('eficiencia', 'moderado')
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 12000.0) & P(lambda se: se < 15000.0)))
    def eficiencia_4(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'sobresaliente')))
        self.answer['eficiencia']=get_details('eficiencia', 'sobresaliente')
        
    @Rule(Fact(action='find_state'),Fact(se=P(lambda se: se > 15000.0)))
    def eficiencia_5(self):
        self.declare(Fact(eficiencia=get_details('eficiencia', 'excelente')))
        self.answer['eficiencia']=get_details('eficiencia', 'excelente')
        
    @Rule(Fact(action='find_state'),Fact(eficiencia=MATCH.eficiencia),salience = -998)
    def situation6(self, eficiencia):
        print("EFICIENCIA: OK")
  
if __name__ == "__main__":
    #For testing purposes only
    
    preprocess()
    params = {
        "free_cash_flow_to_total_debt":5.985886, 
        "accounts_ayable_turnover":0.545793, 
        "operating_margin":-84.875316, 
        "sales_per_employee": 566922.568600, 
        "asset_turnover":0.255633, 
        "total_debt_to_total_assets":0.000000, 
        "current_ratio":8.953141, 
        "revenue_growth_year_over_year":488.260427, 
        "return_on_assets":-23.377976
    }
    engine = Expert()
    engine.set_facts(params)
    engine.run()
    print(engine.answer)

from experta import * 
import pandas as pd
import os

rules = []
advise_map = {}
labels = []

def preprocess():
    global advise_map, labels
    indicadores= os.listdir('recomendacion/')
    labels = ['problematico','mejorable','moderado','sobresaliente','excelente']
    for indicador in indicadores:
        for label in labels:
            recomendation_file = open("recomendacion/" + indicador + "/"+ label+".txt")
            data = recomendation_file.read()
            advise_map[indicador[label]]=data            
 
def get_details(id_situation):
    return advise_map[id_situation]

class Expert(KnowledgeEngine):
    @DefFacts()
    def _initial_action(self):
        print("")
        print("Welcome! this service will give you some advices to improve your free cash flow.")
        print("Please complete the following info:")

        yield Fact(action='find_state')

        @Rule(Fact(action='find_state'), NOT(Fact(cr=W())),salience = 1)
        def current_ratio(self):
            self.declare(Fact(cr=input('Current Ratio:')))
        
        @Rule(Fact(action='find_state'), NOT(Fact(rg=W())),salience = 1)
        def revenue_growth(self):
            self.declare(Fact(rg=input('Revenue Growth:')))

        @Rule(Fact(action='find_state'), NOT(Fact(da=W())),salience = 1)
        def debt_to_assets(self):
            self.declare(Fact(da=input('Total debt to total assets:')))

        @Rule(Fact(action='find_state'), NOT(Fact(fd=W())),salience = 1)
        def cash_flow_to_debt(self):
            self.declare(Fact(fd=input('Free cash flow to total debt:')))

        @Rule(Fact(action='find_state'), NOT(Fact(om=W())),salience = 1)
        def operating_margin(self):
            self.declare(Fact(om=input('Operating Margin:')))

        @Rule(Fact(action='find_state'), NOT(Fact(ra=W())),salience = 1)
        def return_on_assets(self):
            self.declare(Fact(ra=input('Return on Assets:')))

        @Rule(Fact(action='find_state'), NOT(Fact(ap=W())),salience = 1)
        def accounts_turnover(self):
            self.declare(Fact(ap=input('Accounts Payable Turnover:')))

        @Rule(Fact(action='find_state'), NOT(Fact(se=W())),salience = 1)
        def sales_per_employee(self):
            self.declare(Fact(se=input('Sales per Employee:')))        

        @Rule(Fact(action='find_state'), NOT(Fact(at=W())),salience = 1)
        def asset_turnover(self):
            self.declare(Fact(at=input('Asset Turnover:')))     

        @Rule(Fact(action='find_state'), NOT(Fact(cluster=W())),salience = 1)
        def cluster(self):
            self.declare(Fact(cluster=input('Asset Turnover:')))  

        # para cada iteración se le asignará una etiqueta a la característica para evaluarla
        # para la liquidez
        
        @Rule(Fact(action='find_state'),Fact(cr<80.0))
        def liquidez_1(self):
            self.declare(Fact(liquidez=labels[0]))

        @Rule(Fact(action='find_state'),Fact(80.0<cr and cr<100.0))
        def liquidez_2(self):
            self.declare(Fact(liquidez=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(100.0<cr and cr<150.0))
        def liquidez_3(self):
            self.declare(Fact(liquidez=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(150.0<cr and cr<200.0))
        def liquidez_4(self):
            self.declare(Fact(liquidez=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(cr>200.0))
        def liquidez_5(self):
            self.declare(Fact(liquidez=labels[4]))   
            
        @Rule(Fact(action='find_state'),Fact(liquidez=MATCH.liquidez),salience = -998)
        def situation(self, liquidez):
            print("")
            id_situation = disease
            advise_details = get_details(id_situation)
            print("")
            print("The description of the advise is given below :\n")
            print(advise_details+"\n")
            
        # para el crecimiento
        
        @Rule(Fact(action='find_state'),Fact(rg<(-20.0)))
        def crecimiento_1(self):
            self.declare(Fact(crecimiento=labels[0]))

        @Rule(Fact(action='find_state'),Fact(-20.0<rg and rg<-5.0))
        def crecimiento_2(self):
            self.declare(Fact(crecimiento=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(-5.0<rg and rg<5.0))
        def crecimiento_3(self):
            self.declare(Fact(crecimiento=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(5.0<rg and rg<20.0))
        def crecimiento_4(self):
            self.declare(Fact(crecimiento=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(rg>20.0))
        def crecimiento_5(self):
            self.declare(Fact(crecimiento=labels[4]))    
            
        # para el apalancamiento
        
        @Rule(Fact(action='find_state'),Fact((0.8<da and da<1.0) or (0.0<da and da<0.05)))
        def apalancamiento_1(self):
            self.declare(Fact(apalancamiento=labels[0]))

        @Rule(Fact(action='find_state'),Fact((0.7<da and da<0.8) or (0.05<da and da<0.1)))
        def apalancamiento_2(self):
            self.declare(Fact(apalancamiento=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact((0.5<da and da<7.0) or (0.1<da and da<0.15)))
        def apalancamiento_3(self):
            self.declare(Fact(apalancamiento=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact((0.4<da and da<0.5) or (0.15<da and da<0.3)))
        def crecimiento_4(self):
            self.declare(Fact(apalancamiento=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(0.3<da and da<0.4))
        def apalancamiento_5(self):
            self.declare(Fact(apalancamiento=labels[4]))  

        # para el solvencia
        
        @Rule(Fact(action='find_state'),Fact((fd>0.3) or (0.0<fd and fd<0.2)))
        def solvencia_1(self):
            self.declare(Fact(solvencia=labels[0]))

        @Rule(Fact(action='find_state'),Fact((1.7<fd and fd<3.0) or (0.2<fd and fd<0.4)))
        def solvencia_2(self):
            self.declare(Fact(solvencia=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact((1.4<fd and fd<1.7) or (0.4<fd and fd<0.6)))
        def solvencia_3(self):
            self.declare(Fact(solvencia=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact((1.1<fd and fd<1.4) or (0.6<fd and fd<0.8)))
        def solvencia_4(self):
            self.declare(Fact(solvencia=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(8.0<fd and fd<1.1))
        def solvencia_5(self):
            self.declare(Fact(solvencia=labels[4]))  
            
        # para la rentabilidad
        
        @Rule(Fact(action='find_state'),Fact(om<15.0))
        def rentabilidad_1(self):
            self.declare(Fact(rentabilidad_a=labels[0]))

        @Rule(Fact(action='find_state'),Fact(15.0<om and om<25.0))
        def rentabilidad_2(self):
            self.declare(Fact(rentabilidad_a=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(25.0<om and om<40.0))
        def rentabilidad_3(self):
            self.declare(Fact(rentabilidad_a=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(40.0<om and om<50.0))
        def rentabilidad_4(self):
            self.declare(Fact(rentabilidad_a=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(50.0<om))
        def rentabilidad_5(self):
            self.declare(Fact(rentabilidad_a=labels[4]))  
            
        #-----------------------------------------------------------
        
        @Rule(Fact(action='find_state'),Fact(ra<5.0))
        def rentabilidad_6(self):
            self.declare(Fact(rentabilidad_b=labels[0]))

        @Rule(Fact(action='find_state'),Fact(5.0<ra and ra<10.0))
        def rentabilidad_7(self):
            self.declare(Fact(rentabilidad_b=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(10.0<ra and ra<20.0))
        def rentabilidad_8(self):
            self.declare(Fact(rentabilidad_b=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(20.0<ra and ra<25.0))
        def rentabilidad_9(self):
            self.declare(Fact(rentabilidad_b=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(25.0<ra))
        def rentabilidad_10(self):
            self.declare(Fact(rentabilidad_b=labels[4]))  
            
        # para la eficiencia
        
        @Rule(Fact(action='find_state'),Fact(0.0<ap and ap<15.0))
        def eficiencia_1(self):
            self.declare(Fact(eficiencia_a=labels[0]))

        @Rule(Fact(action='find_state'),Fact(15.0<ap and ap<30.0))
        def eficiencia_2(self):
            self.declare(Fact(eficiencia_a=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(30.0<ap and ap<60.0))
        def eficiencia_3(self):
            self.declare(Fact(eficiencia_a=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(60.0<ap and ap<100.0))
        def eficiencia_4(self):
            self.declare(Fact(eficiencia_a=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(100.0<ap))
        def eficiencia_5(self):
            self.declare(Fact(eficiencia_a=labels[4]))  
            
        #-----------------------------------------------------------
        
        @Rule(Fact(action='find_state'),Fact(0.0<se and se<4500.0))
        def eficiencia_6(self):
            self.declare(Fact(eficiencia_b=labels[0]))

        @Rule(Fact(action='find_state'),Fact(4500.0<se and se<9000.0))
        def eficiencia_7(self):
            self.declare(Fact(eficiencia_b=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(9000.0<se and se<12000.0))
        def eficiencia_8(self):
            self.declare(Fact(eficiencia_b=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(12000.0<se and se<15000.0))
        def eficiencia_9(self):
            self.declare(Fact(eficiencia_b=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(15000.0<se))
        def eficiencia_10(self):
            self.declare(Fact(eficiencia_b=labels[4]))  
            
        #-----------------------------------------------------------
        
        @Rule(Fact(action='find_state'),Fact(at<0.0 and at<0.25))
        def eficiencia_11(self):
            self.declare(Fact(eficiencia_c=labels[0]))

        @Rule(Fact(action='find_state'),Fact(0.25<at and at<0.8))
        def eficiencia_12(self):
            self.declare(Fact(eficiencia_c=labels[1]))
            
        @Rule(Fact(action='find_state'),Fact(0.8<at and at<2.0))
        def eficiencia_13(self):
            self.declare(Fact(eficiencia_c=labels[2]))
            
        @Rule(Fact(action='find_state'),Fact(2.0<at and at<2.5))
        def eficiencia_14(self):
            self.declare(Fact(eficiencia_c=labels[3]))
            
        @Rule(Fact(action='find_state'),Fact(2.5<at))
        def eficiencia_15(self):
            self.declare(Fact(eficiencia_c=labels[4])) 

if __name__ == "__main__":
    preprocess()
